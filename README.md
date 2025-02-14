# Stract API Test

## Como rodar

1. Clone o repositório.
2. Crie um ambiente virtual: `python3 -m venv venv`.
3. Ative o ambiente virtual.
4. Instale as dependências com: `pip install -r requirements.txt`.
5. Rode o servidor Flask: `python app.py`.

# Estrutura do projeto

Projeto/
│
├── app.py                       # Arquivo principal que contém o servidor Flask com as rotas
│
├── authentication.py            # Função para retornar os headers de autenticação da API
│
├── view.py                      # Funções para buscar dados e gerar os relatórios (fetch)
│
├── requirements.txt             # Arquivo com as dependências do projeto
│
├── insights_data.csv            # CSV contendo o banco de dados final
│
├── README.md                    # Documentação do projeto
│
├── challenge/
│   └── test-text.txt            # Arquivo para armazenar a resposta da API (dados brutos)
│   └── test.py                  # Script para obter o desafio   
│
└── install.bat                   # Script bash para instalar as dependências do projeto

# Servidor Flask para Relatórios de Anúncios

Este projeto tem como objetivo o desenvolvimento de um servidor local em Python utilizando Flask, que consome dados de uma API externa
e gera relatórios em tempo real. A API fornecida contém informações sobre plataformas de anúncios, contas e campos associados, além de 
dados de insights relativos aos anúncios. O servidor organiza e disponibiliza esses dados através de endpoints específicos para visualização
e download.

## Funcionalidades

- **Consumo de API**: O servidor se conecta a uma API externa para obter dados de plataformas de anúncios, contas e insights.
- **Relatórios em Tempo Real**: Geração de relatórios detalhados ou resumidos com informações sobre as campanhas publicitárias.
- **Acesso por Endpoints**: Os dados podem ser acessados através de vários endpoints no servidor Flask.

## Tecnologias Utilizadas

- **Flask**: Framework Python para desenvolvimento de aplicações web.
- **Requests**: Biblioteca para fazer requisições HTTP e obter dados da API externa.
- **JSON**: Para processar e manipular dados JSON recebidos da API.
- **Collections**: Para estruturar e organizar os dados de forma eficiente.

## Instalação

Para rodar este projeto localmente, clique no arquivo **install.bat** ou siga as instruções abaixo.

### Pré-requisitos

- Python 3.x
- Pip (gerenciador de pacotes Python)

### Como Instalar

1. Clone o repositório:

    ```bash
    git clone https://github.com/PEDR0-MEDEIR0S](https://github.com/PEDR0-MEDEIR0S/stract
    ```

2. Entre no diretório do projeto:

    ```bash
    cd projeto
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

## Como Rodar

Para iniciar o servidor local, execute o seguinte comando:

```bash
python app.py


