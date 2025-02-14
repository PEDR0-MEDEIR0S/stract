"""
Este arquivo tem o objetivo de compreender a dinâmica do projeto através das instruções passadas, direcionamentos e das sugestões
de como desenvolver o projeto.

Com base nisso, foi criado um script para se conectar com a API, testá-la e armazenar a resposta para facilitar a visualização
em tempo real.

O fluxo do script é o seguinte:
1. Conectar com a API usando um token de autorização.
2. Exibir a resposta da requisição no console.
3. Armazenar a resposta em um arquivo para facilitar a consulta e visualização posterior.

As bibliotecas utilizadas são:

- `requests`: Responsável por realizar a requisição HTTP para a API externa, utilizando o método `requests.get()` para obter os dados.
- `os`: Utilizada para manipulação de arquivos e diretórios, permitindo determinar o diretório onde o script está localizado e salvar 
a resposta da API no arquivo `test-text.txt`.

"""
import requests
import os


"""Acessa a URL com a autorização"""
url = "https://sidebar.stract.to/api"
token = "ProcessoSeletivoStract2025"
headers = {'Authorization': f'Bearer {token}'}

"""Obtém a resposta da API"""
response = requests.get(url, headers=headers)

"""Printa a resposta da requisição no console"""
print(response.text)

"""Determina o diretório atual do script e salva a resposta no arquivo dentro desse diretório"""
current_directory = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(current_directory, "test-text.txt")
with open(file_path, "w") as file:
    file.write(response.text)
