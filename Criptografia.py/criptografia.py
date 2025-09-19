# motor_criptografia.py
# Parte 3: Criptografia AES dos arquivos  
# Parte 5: Descriptografia dos arquivos

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import secrets

class MotorCriptografia:
    def __init__(self):
        self.backend_criptografia = default_backend()
    
    def gerar_sal_criptografico(self):
        """Gera um sal criptográfico aleatório de 32 bytes"""
        return secrets.token_bytes(32)
    
    def gerar_vetor_inicializacao(self):
        """Gera um vetor de inicialização aleatório de 16 bytes"""
        return secrets.token_bytes(16)
    
    def aplicar_preenchimento_pkcs7(self, dados_arquivo):
        """Aplica preenchimento PKCS7 aos dados"""
        tamanho_preenchimento = 16 - (len(dados_arquivo) % 16)
        return dados_arquivo + bytes([tamanho_preenchimento] * tamanho_preenchimento)
    
    def remover_preenchimento_pkcs7(self, dados_arquivo):
        """Remove preenchimento PKCS7 dos dados"""
        if len(dados_arquivo) == 0:
            return dados_arquivo
        tamanho_preenchimento = dados_arquivo[-1]
        return dados_arquivo[:-tamanho_preenchimento]
    
    def criptografar_arquivo(self, dados_arquivo, chave_criptografia):
        """Parte 3: Criptografia AES dos arquivos"""
        try:
            # Gerar vetor de inicialização aleatório
            vetor_inicializacao = self.gerar_vetor_inicializacao()
            
            # Criar cifrador AES em modo CBC
            cifrador = Cipher(
                algorithms.AES(chave_criptografia),
                modes.CBC(vetor_inicializacao),
                backend=self.backend_criptografia
            )
            criptografador = cifrador.encryptor()
            
            # Aplicar preenchimento PKCS7 (necessário para CBC)
            dados_com_preenchimento = self.aplicar_preenchimento_pkcs7(dados_arquivo)
            
            # Criptografar
            dados_criptografados = criptografador.update(dados_com_preenchimento) + criptografador.finalize()
            
            # Retornar vetor de inicialização + dados criptografados
            return vetor_inicializacao + dados_criptografados
            
        except Exception as erro:
            print(f"Erro durante criptografia: {str(erro)}")
            return None
    
    def descriptografar_arquivo(self, dados_criptografados, chave_criptografia):
        """Parte 5: Descriptografia dos arquivos"""
        try:
            # Verificar se há dados suficientes (pelo menos vetor de inicialização de 16 bytes)
            if len(dados_criptografados) < 16:
                raise ValueError("Dados insuficientes para descriptografia")
            
            # Extrair vetor de inicialização (primeiros 16 bytes)
            vetor_inicializacao = dados_criptografados[:16]
            dados_cifrados = dados_criptografados[16:]
            
            # Verificar se há dados para descriptografar
            if len(dados_cifrados) == 0:
                raise ValueError("Nenhum dado para descriptografar")
            
            # Criar cifrador para descriptografia
            cifrador = Cipher(
                algorithms.AES(chave_criptografia),
                modes.CBC(vetor_inicializacao),
                backend=self.backend_criptografia
            )
            descriptografador = cifrador.decryptor()
            
            # Descriptografar
            dados_com_preenchimento = descriptografador.update(dados_cifrados) + descriptografador.finalize()
            
            # Remover preenchimento PKCS7
            dados_originais = self.remover_preenchimento_pkcs7(dados_com_preenchimento)
            
            return dados_originais
            
        except Exception as erro:
            print(f"Erro durante descriptografia: {str(erro)}")
            return None
    
    def processar_criptografia_em_lote(self, lista_arquivos, chave_criptografia, gerenciador_arquivos):
        """Processa criptografia de múltiplos arquivos"""
        sucessos = 0
        erros = 0
        sal_usado = self.gerar_sal_criptografico()
        
        print(f"\nCriptografando {len(lista_arquivos)} arquivos...")
        
        for arquivo in lista_arquivos:
            print(f"Processando: {arquivo.name}")
            
            # Ler arquivo
            dados_arquivo = gerenciador_arquivos.ler_conteudo_arquivo(arquivo)
            if dados_arquivo is None:
                erros += 1
                continue
            
            # Criptografar arquivo
            dados_criptografados = self.criptografar_arquivo(dados_arquivo, chave_criptografia)
            
            if dados_criptografados:
                # Salvar na pasta de backup
                if gerenciador_arquivos.salvar_arquivo_criptografado(arquivo, dados_criptografados, sal_usado):
                    sucessos += 1
                else:
                    erros += 1
            else:
                erros += 1
        
        return sucessos, erros, sal_usado
    
    def processar_descriptografia_em_lote(self, pasta_criptografada, arquivos_criptografados, senha_usuario, gerenciador_senhas, gerenciador_arquivos):
        """Processa descriptografia de múltiplos arquivos"""
        sucessos = 0
        erros = 0
        
        # Criar pasta para arquivos descriptografados
        pasta_descriptografada = gerenciador_arquivos.criar_pasta_descriptografada(pasta_criptografada)
        
        print(f"\nDescriptografando {len(arquivos_criptografados)} arquivos...")
        
        for arquivo_criptografado in arquivos_criptografados:
            print(f"Processando: {arquivo_criptografado.name}")
            
            try:
                # Ler arquivo criptografado
                dados_arquivo = gerenciador_arquivos.ler_conteudo_arquivo(arquivo_criptografado)
                if dados_arquivo is None:
                    erros += 1
                    continue
                
                # Verificar se há dados suficientes (sal + vetor de inicialização mínimo)
                if len(dados_arquivo) < 48:  # 32 bytes sal + 16 bytes vetor de inicialização
                    print(f"Arquivo {arquivo_criptografado.name} corrompido ou muito pequeno")
                    erros += 1
                    continue
                
                # Extrair sal criptográfico (primeiros 32 bytes)
                sal_criptografico = dados_arquivo[:32]
                dados_criptografados = dados_arquivo[32:]
                
                # Derivar chave com sal
                chave_derivada = gerenciador_senhas.derivar_chave_da_senha(senha_usuario, sal_criptografico)
                
                # Descriptografar
                dados_originais = self.descriptografar_arquivo(dados_criptografados, chave_derivada)
                
                if dados_originais is not None:
                    # Salvar arquivo descriptografado
                    nome_original = arquivo_criptografado.stem  # Remove .enc
                    if gerenciador_arquivos.salvar_arquivo_descriptografado(
                        pasta_descriptografada, nome_original, dados_originais
                    ):
                        sucessos += 1
                    else:
                        erros += 1
                else:
                    erros += 1
                    
            except Exception as erro:
                print(f"Erro ao processar {arquivo_criptografado.name}: {str(erro)}")
                erros += 1
        
        return sucessos, erros, pasta_descriptografada
    
    def verificar_integridade_arquivo_criptografado(self, arquivo_criptografado):
        """Verifica se um arquivo criptografado tem estrutura válida"""
        try:
            with open(arquivo_criptografado, 'rb') as arquivo:
                dados = arquivo.read()
            
            # Verificar tamanho mínimo (sal + vetor de inicialização + pelo menos um bloco)
            if len(dados) < 48:  # 32 + 16 + 0
                return False, "Arquivo muito pequeno"
            
            # Verificar se o tamanho dos dados criptografados é múltiplo de 16
            dados_criptografados = dados[32:]  # Remove sal
            if (len(dados_criptografados) - 16) % 16 != 0:  # Remove vetor de inicialização, verifica blocos
                return False, "Tamanho inválido para AES"
            
            return True, "Arquivo válido"
            
        except Exception as erro:
            return False, f"Erro ao verificar: {str(erro)}"