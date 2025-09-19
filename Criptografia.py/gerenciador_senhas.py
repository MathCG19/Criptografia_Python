# gerenciador_senhas.py
# Parte 1: Entrada da senha do usuário

import getpass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

class GerenciadorSenhas:
    def __init__(self):
        self.backend_criptografia = default_backend()
    
    def entrada_senha(self):
        """Parte 1: Entrada da senha do usuário"""
        print("=== SISTEMA DE CRIPTOGRAFIA DE ARQUIVOS ===")
        print("Bem-vindo ao desafio de criptografia em Python!")
        print()
        
        while True:
            senha = getpass.getpass("Digite a senha para criptografia (mínimo 8 caracteres): ")
            if len(senha) < 8:
                print("Senha deve ter pelo menos 8 caracteres!")
                continue
            
            confirmacao_senha = getpass.getpass("Confirme a senha: ")
            if senha != confirmacao_senha:
                print("Senhas não coincidem! Tente novamente.")
                continue
                
            print("Senha configurada com sucesso!")
            return senha
    
    def solicitar_senha_descriptografia(self):
        """Solicita senha para descriptografia"""
        return getpass.getpass("Digite a senha para descriptografia: ")
    
    def derivar_chave_da_senha(self, senha, sal_criptografico):
        """Deriva uma chave a partir da senha usando PBKDF2"""
        derivador_chave = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # Chave de 256 bits para AES-256
            salt=sal_criptografico,
            iterations=100000,
            backend=self.backend_criptografia
        )
        return derivador_chave.derive(senha.encode())
    
    def validar_senha(self, senha):
        """Valida se a senha atende aos critérios básicos"""
        if len(senha) < 8:
            return False, "Senha deve ter pelo menos 8 caracteres"
        return True, "Senha válida"