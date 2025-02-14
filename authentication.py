"""
Este projeto tem como objetivo o desenvolvimento de um servidor local em Python utilizando Flask, que consome dados de 
uma API externa e gera relatórios em tempo real. A API fornecida contém informações sobre plataformas de anúncios, contas 
e campos associados, além de dados de insights relativos aos anúncios. O principal desafio aqui foi não apenas consumir a 
API de maneira eficiente, mas também transformar esses dados em relatórios estruturados que pudessem ser acessados facilmente 
por endpoints específicos.

Para se conectar com a API, foi disponibilizado um token de autenticação que deve ser utilizado em todas as requisições. 
Visando evitar redundância e centrralizar a lógica de autenticação, foi criada uma função para gerar os cabeçalhos de autorização 
sempre que necessário. Dessa forma, a autenticação pode ser facilmente gerenciada em um único ponto do código, garantindo a 
reutilização do token nas requisições.
"""
def get_api_headers(account_token=None):
    """
    Função que retorna os headers necessários para autenticação da API.
    O token de autorização é configurado dinamicamente a partir da conta.
    """
    if account_token is None:
        account_token = "ProcessoSeletivoStract2025"

    headers = {
        "Authorization": f"Bearer {account_token}",  
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Content-Type": "application/json"
    }
    return headers
