# Sistema de Criptografia para Proteção de Arquivos

Este projeto implementa um sistema completo de criptografia de arquivos usando **AES-256-CBC** em Python, desenvolvido como resposta ao desafio de criptografia proposto. O sistema oferece proteção para seus arquivos sensíveis.

## Demonstração

```bash
SISTEMA DE CRIPTOGRAFIA PARA PROTEÇÃO DE ARQUIVOS
════════════════════════════════════════════════════════════
Algoritmo: AES-256-CBC
Derivação de chave: PBKDF2 com SHA-256 (100.000 iterações)
Sal único para cada sessão
Vetor de inicialização único para cada arquivo
Preenchimento: PKCS7
```

## Funcionalidades

- **Criptografia AES-256-CBC**: Proteção de nível militar
- **Derivação segura de chaves**: PBKDF2 com SHA-256 (100.000 iterações)
- **Sal único**: Proteção contra ataques de dicionário
- **IV único por arquivo**: Cada arquivo tem criptografia única
- **Preenchimento PKCS7**: Padrão da indústria
- **Descriptografia completa**: Recuperação total dos arquivos originais
- **Organização automática**: Pastas separadas para backup e recuperação
- **Verificação de integridade**: Validação de arquivos criptografados

## Instalação Rápida

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Clonar o repositório

```bash
git clone https://github.com/seu-usuario/sistema-criptografia-arquivos.git
cd sistema-criptografia-arquivos
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar o sistema

```bash
python principal.py
```

## Arquitetura do Projeto

```
criptografia/
├── principal.py              # Arquivo principal (menu e coordenação)
├── gerenciador_senhas.py     # Gerenciador de senhas (Parte 1)
├── gerenciador_arquivos.py   # Gerenciador de arquivos (Partes 2 e 4)
├── motor_criptografia.py     # Motor de criptografia AES (Partes 3 e 5)
├── requirements.txt          # Dependências
├── README.md                 # Esta documentação
└── .gitignore               # Arquivos ignorados pelo Git
```

### Módulos e Responsabilidades

#### `gerenciador_senhas.py` - Parte 1: Entrada da Senha
- Coleta e validação de senhas seguras
- Derivação segura de chaves com PBKDF2
- Confirmação de senha para evitar erros
- Ocultação da senha durante digitação

#### `gerenciador_arquivos.py` - Partes 2 e 4: Gerenciamento de Arquivos
- Acesso e validação de pastas
- Criação automática de pastas de backup
- Leitura e escrita segura de arquivos
- Organização da estrutura de diretórios

#### `motor_criptografia.py` - Partes 3 e 5: Criptografia
- Implementação completa do AES-256-CBC
- Geração de sal e vetor de inicialização únicos
- Aplicação e remoção de preenchimento PKCS7
- Processamento em lote de arquivos

#### `principal.py` - Coordenação Geral
- Menu interativo intuitivo
- Coordenação entre todos os módulos
- Tratamento robusto de erros
- Interface do usuário em português

## Como Usar

### Criptografar Arquivos

1. Execute `python principal.py`
2. Escolha a opção **1** (Criptografar arquivos)
3. Digite uma senha forte (mínimo 8 caracteres)
4. Informe o caminho da pasta com seus arquivos
5. Os arquivos serão criptografados e salvos em `[pasta]_backup_criptografado/`

### Descriptografar Arquivos

1. Execute `python principal.py`
2. Escolha a opção **2** (Descriptografar arquivos)
3. Digite a mesma senha usada na criptografia
4. Informe o caminho da pasta com arquivos `.enc`
5. Os arquivos originais serão recuperados em `[pasta]_descriptografado/`

## Segurança

Este sistema implementa as melhores práticas de segurança:

| Componente | Especificação | Descrição |
|------------|---------------|-----------|
| **Algoritmo** | AES-256-CBC | Criptografia de nível militar |
| **Derivação** | PBKDF2-SHA256 | 100.000 iterações contra força bruta |
| **Sal** | 32 bytes aleatórios | Único por sessão, previne rainbow tables |
| **IV** | 16 bytes aleatórios | Único por arquivo, previne padrões |
| **Preenchimento** | PKCS7 | Padrão da indústria |

## Exemplo de Uso

```bash
$ python principal.py

MENU PRINCIPAL
════════════════════════════════════════════════════
1. Criptografar arquivos
2. Descriptografar arquivos
3. Mostrar ajuda
4. Sair do programa

Escolha uma opção (1-4): 1

=== INICIANDO CRIPTOGRAFIA ===
Digite a senha para criptografia (mínimo 8 caracteres): ********
Confirme a senha: ********
Senha configurada com sucesso!

Digite o caminho da pasta com arquivos para criptografar: ./meus_documentos
 Pasta encontrada: meus_documentos
 Arquivos encontrados: 3
  - documento.pdf
  - planilha.xlsx  
  - foto.jpg

 Pasta de backup criada: meus_documentos_backup_criptografado

Criptografando 3 arquivos...
Processando: documento.pdf
 Arquivo criptografado salvo: documento.enc
Processando: planilha.xlsx
 Arquivo criptografado salvo: planilha.enc
Processando: foto.jpg
 Arquivo criptografado salvo: foto.enc

 Criptografia concluída!
Sucessos: 3 | Erros: 0
Arquivos criptografados salvos em: meus_documentos_backup_criptografado
Guarde bem sua senha - ela será necessária para descriptografar!
```

## Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Avisos Importantes

- **NUNCA perca sua senha**: Sem ela, os arquivos são irrecuperáveis
- **Faça backup da senha**: Guarde em local seguro e separado
- **Teste antes de usar**: Sempre teste com arquivos não importantes primeiro
- **Não compartilhe senhas**: Use senhas únicas e fortes

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Autor

Desenvolvido para o desafio de criptografia em Python.

## Links Úteis

- [Documentação da Cryptography](https://cryptography.io/en/latest/)
- [NIST Guidelines](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf)
- [OWASP Cryptographic Storage](https://owasp.org/www-project-cheat-sheets/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
