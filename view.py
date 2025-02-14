# view.py
"""
Este projeto tem como objetivo o desenvolvimento de um servidor local em Python utilizando Flask, que consome dados de 
uma API externa e gera relatórios em tempo real. A API fornecida contém informações sobre plataformas de anúncios, contas 
e campos associados, além de dados de insights relativos aos anúncios. O principal desafio aqui foi não apenas consumir a 
API de maneira eficiente, mas também transformar esses dados em relatórios estruturados que pudessem ser acessados facilmente 
por endpoints específicos.

A primeira etapa foi conectar à API para obter os dados das plataformas, contas e campos disponíveis, e então coletar os insights
relacionados a cada anúncio veiculado nas plataformas. Para isso, utilizamos a biblioteca `requests` para fazer as requisições HTTP
necessárias e a biblioteca `json` para processar as respostas da API.

O desenvolvimento foi realizado de maneira gradual, seguindo uma sequência de etapas para garantir que tudo fosse feito de forma 
estruturada. As etapas foram as seguintes:

1. Descobrir quais são as plataformas disponíveis.
2. Descobrir quais são as contas e os campos de cada plataforma.
3. Identificar quais dados seriam utilizados na requisição para obter os dados do endpoint de insights.
4. Obter os dados do fetch do insights.
5. Organizar os dados em objetos estruturados para serem utilizados nos relatórios.

Este é o resumo de tudo o que foi feito neste arquivo.
"""
import requests 
import json
from authentication import get_api_headers
"""
A biblioteca `requests` é usada para enviar requisições HTTP para a API externa e obter dados de plataformas, contas e campos.
A biblioteca `json` é usada para formatar e manipular os dados JSON recebidos da API.
A função `get_api_headers` é importada para garantir que o token de autenticação necessário seja incluído nas requisições.
"""
def fetch_platforms():
    """
    Primeira requisição.
    Faz uma requisição à API para obter as plataformas disponíveis.
    Retorna uma lista com as plataformas se a requisição for bem-sucedida.
    Caso contrário, imprime uma mensagem de erro e retorna uma lista vazia.
    """
    url = "https://sidebar.stract.to/api/platforms"
    headers = get_api_headers()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        platforms_data = response.json()
        print("Plataformas disponíveis:", json.dumps(platforms_data, indent=4))
        return platforms_data.get('platforms', [])
    else:
        print(f"Erro ao obter plataformas: {response.status_code}")
        print("Resposta da API:", response.json())
        return []


def remove_pagination(data):
    """
    Foi percebido que existia uma chave e valor que não deveriam ser inseridos no objeto final, então deveria se descartado.
    Remove a chave 'pagination' de um objeto JSON ou dicionário, recursivamente.
    A função modifica o objeto de entrada diretamente.
    """
    if isinstance(data, dict):
        data.pop('pagination', None)
        for key, value in data.items():
            remove_pagination(value)
    elif isinstance(data, list):
        for item in data:
            remove_pagination(item)


def fetch_accounts_and_fields(platform):
    """
    Segunda requisição.
    Faz requisições à API para obter as contas e os campos com base nas plataformas específicas obtidas em fetch_platforms().
    Retorna um dicionário com as contas e campos da plataforma, ou None em caso de erro.
    """
    headers = get_api_headers()
    accounts_url = f"https://sidebar.stract.to/api/accounts?platform={platform}"
    accounts_response = requests.get(accounts_url, headers=headers)
    fields_url = f"https://sidebar.stract.to/api/fields?platform={platform}"
    fields_response = requests.get(fields_url, headers=headers)
    
    if accounts_response.status_code == 200 and fields_response.status_code == 200:
        accounts_data = accounts_response.json()
        fields_data = fields_response.json()
        remove_pagination(accounts_data)
        remove_pagination(fields_data)
        print(f"Contas para {platform}: {json.dumps(accounts_data, indent=4)}")
        print(f"Campos para {platform}: {json.dumps(fields_data, indent=4)}")
        platform_data = {
            "platform": platform,
            "accounts": {"accounts": accounts_data.get("accounts", [])},
            "fields": {"fields": fields_data.get("fields", [])}
        }
        return platform_data
    else:
        print(f"Erro ao obter dados para a plataforma {platform}")
        print("Resposta de contas:", accounts_response.json())
        print("Resposta de campos:", fields_response.json())
        return None


def fetch_insights(platform_data):
    """
    Terceira requisiação
    Coleta os insights dos field values para as contas de cada uma das plataformas com base em fetch_accounts_and_fields(platform).
    Organiza os dados de cada conta e retorna uma lista de dicionários com os resultados.
    """
    platform = platform_data['platform']
    accounts = platform_data['accounts']['accounts']
    fields = platform_data['fields']['fields']
    
    insights_data = []
    
    field_values = [field.get('value') for field in fields]
    
    for account in accounts:
        account_id = account.get('id')
        account_name = account.get('name')
        account_token = account.get('token')

        field_values_str = ','.join(field_values)
        insights_url = f"https://sidebar.stract.to/api/insights?platform={platform}&account={account_id}&token={account_token}&fields={field_values_str}"
        
        headers = get_api_headers()
        response = requests.get(insights_url, headers=headers)

        if response.status_code == 200:
            insights = response.json()
            for insight in insights.get('insights', []):
                row = {
                    "Platform": platform,
                    "Ad Name": account_name,
                    "clicks": insight.get('clicks', 'N/A'),
                    "impressions": insight.get('impressions', 'N/A'),
                    "spend": insight.get('spend', 'N/A'),
                    "cpc": insight.get('cpc', 'N/A'),
                    "ctr": insight.get('ctr', 'N/A')
                }
                insights_data.append(row)
        else:
            print(f"Erro ao obter insights para a conta {account_id} na plataforma {platform}: {response.status_code}")

    return insights_data


def main():
    """
    Função principal que orquestra o processo de obtenção das plataformas, contas, campos e insights.
    Organiza todos os dados em uma lista de dicionários e imprime o resultado.
    """
    platforms = fetch_platforms()
    all_insights_data = []
    
    for platform in platforms:
        platform_value = platform['value']
        print(f"Processando plataforma: {platform_value}")
        
        platform_data = fetch_accounts_and_fields(platform_value)
        
        if platform_data:
            insights_data = fetch_insights(platform_data)
            all_insights_data.extend(insights_data)
    
    print("Dados organizados para utilização:", all_insights_data)


if __name__ == "__main__":
    main()
