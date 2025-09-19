# gerenciador_arquivos.py  
# Parte 2: Acesso à pasta original e leitura dos arquivos
# Parte 4: Salvamento dos arquivos criptografados em outra pasta

import os
import shutil
from pathlib import Path

class GerenciadorArquivos:
    def __init__(self):
        self.pasta_origem = None
        self.pasta_backup = None
    
    def acessar_pasta_origem(self):
        """Parte 2: Acesso à pasta original e leitura dos arquivos"""
        print("\n=== ACESSO À PASTA DE ARQUIVOS ===")
        
        while True:
            caminho_pasta = input("Digite o caminho da pasta com arquivos para criptografar: ").strip()
            
            if not caminho_pasta:
                print("Por favor, digite um caminho válido!")
                continue
                
            pasta = Path(caminho_pasta)
            
            if not pasta.exists():
                print(f"Pasta não encontrada: {caminho_pasta}")
                continue
                
            if not pasta.is_dir():
                print(f"O caminho não é uma pasta: {caminho_pasta}")
                continue
                
            # Verificar se há arquivos na pasta
            todos_arquivos = list(pasta.glob('*'))
            arquivos_comuns = [arquivo for arquivo in todos_arquivos if arquivo.is_file()]
            
            if not arquivos_comuns:
                print(f"Nenhum arquivo encontrado na pasta: {caminho_pasta}")
                continue
                
            print(f"Pasta encontrada: {pasta}")
            print(f"Arquivos encontrados: {len(arquivos_comuns)}")
            for arquivo in arquivos_comuns:
                print(f"  - {arquivo.name}")
                
            self.pasta_origem = pasta
            return arquivos_comuns
    
    def acessar_pasta_criptografada(self):
        """Acessa pasta com arquivos criptografados para descriptografia"""
        print("\n=== ACESSO À PASTA COM ARQUIVOS CRIPTOGRAFADOS ===")
        
        while True:
            caminho_pasta = input("Digite o caminho da pasta com arquivos criptografados (.enc): ").strip()
            
            pasta = Path(caminho_pasta)
            if not pasta.exists() or not pasta.is_dir():
                print("Pasta não encontrada!")
                continue
                
            arquivos_criptografados = list(pasta.glob('*.enc'))
            if not arquivos_criptografados:
                print("Nenhum arquivo .enc encontrado na pasta!")
                continue
                
            print(f"Pasta encontrada: {pasta}")
            print(f"Arquivos criptografados encontrados: {len(arquivos_criptografados)}")
            for arquivo in arquivos_criptografados:
                print(f"  - {arquivo.name}")
                
            return pasta, arquivos_criptografados
    
    def criar_pasta_backup(self):
        """Parte 4: Criar pasta de backup para arquivos criptografados"""
        if not self.pasta_origem:
            raise ValueError("Pasta origem não foi definida!")
            
        pasta_backup = self.pasta_origem.parent / f"{self.pasta_origem.name}_backup_criptografado"
        
        # Remover pasta de backup anterior se existir
        if pasta_backup.exists():
            shutil.rmtree(pasta_backup)
            
        pasta_backup.mkdir(exist_ok=True)
        self.pasta_backup = pasta_backup
        print(f"Pasta de backup criada: {pasta_backup}")
        return pasta_backup
    
    def criar_pasta_descriptografada(self, pasta_origem):
        """Criar pasta para arquivos descriptografados"""
        pasta_descriptografada = pasta_origem.parent / f"{pasta_origem.name}_descriptografado"
        
        if pasta_descriptografada.exists():
            shutil.rmtree(pasta_descriptografada)
        pasta_descriptografada.mkdir()
        
        print(f"Pasta de descriptografia criada: {pasta_descriptografada}")
        return pasta_descriptografada
    
    def ler_conteudo_arquivo(self, caminho_arquivo):
        """Lê o conteúdo de um arquivo"""
        try:
            with open(caminho_arquivo, 'rb') as arquivo:
                return arquivo.read()
        except Exception as erro:
            print(f"Erro ao ler arquivo {caminho_arquivo.name}: {str(erro)}")
            return None
    
    def salvar_arquivo_criptografado(self, arquivo_original, dados_criptografados, sal_criptografico):
        """Parte 4: Salvamento dos arquivos criptografados"""
        if not self.pasta_backup:
            raise ValueError("Pasta de backup não foi criada!")
            
        nome_criptografado = f"{arquivo_original.stem}.enc"
        arquivo_backup = self.pasta_backup / nome_criptografado
        
        try:
            with open(arquivo_backup, 'wb') as arquivo:
                # Salvar sal (32 bytes) + dados criptografados
                arquivo.write(sal_criptografico + dados_criptografados)
            
            print(f"Arquivo criptografado salvo: {nome_criptografado}")
            return True
            
        except Exception as erro:
            print(f"Erro ao salvar arquivo criptografado: {str(erro)}")
            return False
    
    def salvar_arquivo_descriptografado(self, pasta_saida, nome_arquivo, dados_arquivo):
        """Salva arquivo descriptografado"""
        try:
            arquivo_saida = pasta_saida / nome_arquivo
            with open(arquivo_saida, 'wb') as arquivo:
                arquivo.write(dados_arquivo)
            
            print(f"Descriptografado: {nome_arquivo}")
            return True
            
        except Exception as erro:
            print(f"Erro ao salvar arquivo descriptografado: {str(erro)}")
            return False
    
    def obter_informacoes_pasta(self, pasta):
        """Obtém informações sobre uma pasta"""
        if not pasta.exists():
            return None
            
        todos_arquivos = list(pasta.glob('*'))
        arquivos_comuns = [arquivo for arquivo in todos_arquivos if arquivo.is_file()]
        
        return {
            'caminho': pasta,
            'total_arquivos': len(arquivos_comuns),
            'arquivos': arquivos_comuns
        }