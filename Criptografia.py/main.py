# main.py
# Arquivo principal - Menu e coordenação de todos os módulos

import sys
from pathlib import Path

# Importar nossos módulos
from gerenciador_senhas import GerenciadorSenhas
from gerenciador_arquivos import GerenciadorArquivos  
from criptografia import MotorCriptografia

class SistemaCriptografiaArquivos:
    def __init__(self):
        self.gerenciador_senhas = GerenciadorSenhas()
        self.gerenciador_arquivos = GerenciadorArquivos()
        self.criptografia = MotorCriptografia()
    
    def processar_criptografia_completa(self):
        """Processo principal de criptografia - coordena todas as partes"""
        print("\n=== INICIANDO CRIPTOGRAFIA ===")
        
        try:
            # Parte 1: Entrada da senha
            senha_usuario = self.gerenciador_senhas.entrada_senha()
            
            # Parte 2: Acessar pasta
            lista_arquivos = self.gerenciador_arquivos.acessar_pasta_origem()
            
            # Parte 4: Criar pasta de backup
            self.gerenciador_arquivos.criar_pasta_backup()
            
            # Gerar sal criptográfico para esta sessão
            sal_criptografico = self.criptografia.gerar_sal_criptografico()
            
            # Derivar chave da senha
            chave_derivada = self.gerenciador_senhas.derivar_chave_da_senha(senha_usuario, sal_criptografico)
            
            # Parte 3: Processar criptografia de todos os arquivos
            sucessos, erros, sal_usado = self.criptografia.processar_criptografia_em_lote(
                lista_arquivos, chave_derivada, self.gerenciador_arquivos
            )
            
            # Relatório final
            print(f"\nCriptografia concluída!")
            print(f"Sucessos: {sucessos} | Erros: {erros}")
            
            if sucessos > 0:
                print(f"Arquivos criptografados salvos em: {self.gerenciador_arquivos.pasta_backup}")
                print("Guarde bem sua senha - ela será necessária para descriptografar!")
            
            return sucessos > 0
            
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            return False
        except Exception as erro:
            print(f"Erro durante criptografia: {str(erro)}")
            return False
    
    def processar_descriptografia_completa(self):
        """Processo principal de descriptografia - coordena todas as partes"""
        print("\n=== INICIANDO DESCRIPTOGRAFIA ===")
        
        try:
            # Parte 5: Solicitar senha
            senha_usuario = self.gerenciador_senhas.solicitar_senha_descriptografia()
            
            # Acessar pasta com arquivos criptografados
            pasta_criptografada, arquivos_criptografados = self.gerenciador_arquivos.acessar_pasta_criptografada()
            
            # Processar descriptografia
            sucessos, erros, pasta_saida = self.criptografia.processar_descriptografia_em_lote(
                pasta_criptografada, arquivos_criptografados, senha_usuario, self.gerenciador_senhas, self.gerenciador_arquivos
            )
            
            # Relatório final
            print(f"\nDescriptografia concluída!")
            print(f"Sucessos: {sucessos} | Erros: {erros}")
            
            if sucessos > 0:
                print(f"Arquivos descriptografados salvos em: {pasta_saida}")
            elif erros > 0:
                print("Se todos os arquivos falharam, verifique se a senha está correta.")
            
            return sucessos > 0
            
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            return False
        except Exception as erro:
            print(f"Erro durante descriptografia: {str(erro)}")
            return False
    
    def verificar_bibliotecas_necessarias(self):
        """Verifica se todas as bibliotecas estão instaladas"""
        try:
            from cryptography.hazmat.primitives.ciphers import Cipher
            print("Biblioteca 'cryptography' encontrada!")
            return True
        except ImportError:
            print("Biblioteca 'cryptography' não encontrada!")
            print("Instale com: pip install cryptography")
            return False
    
    def mostrar_informacoes_do_sistema(self):
        """Mostra informações sobre o sistema"""
        print("\n" + "="*60)
        print("SISTEMA DE CRIPTOGRAFIA PARA PROTEÇÃO DE ARQUIVOS")
        print("="*60)
        print("Algoritmo: AES-256-CBC")
        print("Derivação de chave: PBKDF2 com SHA-256 (100.000 iterações)")
        print("Sal único para cada sessão")
        print("Vetor de inicialização único para cada arquivo")
        print("Preenchimento: PKCS7")
        print("-"*60)

def executar_programa_principal():
    """Função principal do programa"""
    sistema = SistemaCriptografiaArquivos()
    
    # Verificar bibliotecas necessárias
    if not sistema.verificar_bibliotecas_necessarias():
        sys.exit(1)
    
    # Mostrar informações do sistema
    sistema.mostrar_informacoes_do_sistema()
    
    while True:
        print("\n" + "="*50)
        print("MENU PRINCIPAL")
        print("="*50)
        print("1.Criptografar arquivos")
        print("2.Descriptografar arquivos") 
        print("3.Mostrar ajuda")
        print("4.Sair do programa")
        print("-"*50)
        
        try:
            opcao_escolhida = input("Escolha uma opção (1-4): ").strip()
            
            if opcao_escolhida == '1':
                sistema.processar_criptografia_completa()
                
            elif opcao_escolhida == '2':
                sistema.processar_descriptografia_completa()
                
            elif opcao_escolhida == '3':
                mostrar_tela_ajuda()
                
            elif opcao_escolhida == '4':
                print("Obrigado por usar o sistema! Até logo!")
                break
                
            else:
                print("Opção inválida! Escolha 1, 2, 3 ou 4.")
                
        except KeyboardInterrupt:
            print("\n\nPrograma interrompido pelo usuário. Até logo!")
            break
        except Exception as erro:
            print(f"Erro inesperado: {str(erro)}")

def mostrar_tela_ajuda():
    """Mostra ajuda e instruções de uso"""
    print("\n" + "="*60)
    print("AJUDA - COMO USAR O SISTEMA")
    print("="*60)
    print()
    print("CRIPTOGRAFAR ARQUIVOS:")
    print("   1. Escolha uma senha forte (mínimo 8 caracteres)")
    print("   2. Informe o caminho da pasta com os arquivos")
    print("   3. Os arquivos serão criptografados e salvos numa nova pasta")
    print("   4. IMPORTANTE: Guarde bem a senha!")
    print()
    print("DESCRIPTOGRAFAR ARQUIVOS:")
    print("   1. Digite a mesma senha usada na criptografia")
    print("   2. Informe o caminho da pasta com arquivos .enc")
    print("   3. Os arquivos originais serão recuperados")
    print()
    print("DICAS IMPORTANTES:")
    print("   • Use senhas fortes e únicas")
    print("   • Mantenha backup da senha em local seguro")
    print("   • Arquivos criptografados têm extensão .enc")
    print("   • Cada sessão gera arquivos únicos")
    print()
    print("SEGURANÇA:")
    print("   • AES-256: Criptografia de nível militar")
    print("   • Sem a senha correta, os arquivos são irrecuperáveis")
    print("   • Sal e vetor de inicialização únicos previnem ataques")
    print()
    print("ESTRUTURA DE PASTAS:")
    print("   • Pasta original: seus arquivos normais")
    print("   • Pasta backup: arquivos criptografados (.enc)")
    print("   • Pasta descriptografada: arquivos recuperados")

if __name__ == "__main__":
    executar_programa_principal()