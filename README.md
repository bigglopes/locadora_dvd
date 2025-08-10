# Sistema de Locação de DVDs

Este é um sistema para gerenciamento de uma locadora de DVDs, permitindo o cadastro de clientes, DVDs e controle de aluguéis.

## Funcionalidades

- Cadastro de clientes (nome, telefone, endereço)
- Cadastro de DVDs (nome, sinopse, ano de lançamento, ano de aquisição)
- Registro de aluguéis (data de aluguel, cliente, lista de DVDs alugados, data de devolução)
- Consulta de disponibilidade de DVDs
- Relatórios de aluguéis

## Estrutura do Projeto

- `models/`: Classes de modelo (Cliente, DVD, Aluguel)
- `controllers/`: Controladores para gerenciar as operações
- `views/`: Interfaces de usuário
- `database/`: Gerenciamento de dados
- `main.py`: Ponto de entrada da aplicação

## Como Executar

1. Certifique-se de ter o Python 3.8+ instalado
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute o programa: `python main.py`
4. Se deseja gear o binario gerar_exe.bat
5. O script simulate_data.py é utilizado para gerar dados de teste, ajudar a entender o funcionamento do aplicativo.
6. Execute o script: `python simulate_data.py`



