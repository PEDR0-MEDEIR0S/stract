# app.py
"""
Este projeto tem como objetivo o desenvolvimento de um servidor local em Python utilizando Flask, que consome dados de 
uma API externa e gera relatórios em tempo real. A API fornecida contém informações sobre plataformas de anúncios, contas 
e campos associados, além de dados de insights relativos aos anúncios. O principal desafio aqui foi não apenas consumir a 
API de maneira eficiente, mas também transformar esses dados em relatórios estruturados que pudessem ser acessados facilmente 
por endpoints específicos.

Após a criação dos objetos no arquivo view.py, faltava expor os dados, então para organizar o projeto, foi criado outro arquivo
que utiliza os dados e utiliza o flash/python para publicação dos dados localmente. 
Então foi pensando que deviria ser criado quatro tipos principais de relatórios:

1. `/geral`: Retorna um relatório com dados de todas as plataformas, como o nome da plataforma, o nome do utilizador e 
   métricas como cliques, impressões, gastos, CPC e CTR.
   
2. `/geral/resumo`: Fornece um resumo dos dados de todas as plataformas, agregando os dados por plataforma e somando 
   as métricas numéricas (cliques, impressões, gasto, etc.) e mostrando a média para CPC e CTR.
   
3. `/<plataforma>`: Retorna os dados dos anúncios específicos de cada uma plataforma solicitada.
   
4. `/<plataforma>/resumo`: Similar ao endpoint anterior, mas retorna um resumo dos dados agregados por plataforma.

Para obter os dados de cada das plataformas, o servidor utiliza funções auxiliares (`fetch_platforms`, `fetch_accounts_and_fields` 
e `fetch_insights`) para realizar as requisições à API externa e processar os dados conforme necessário. 
"""
from flask import Flask, Response
from view import fetch_platforms, fetch_accounts_and_fields, fetch_insights, main
from collections import defaultdict
"""
Bibliotecas Importadas:

1. **Flask**: Framework web utilizado para criar o servidor local e expor os endpoints da API.
   - `Flask`: Classe principal para criação da aplicação web.
   - `Response`: Usado para retornar respostas personalizadas, como os arquivos CSV gerados.

2. **view**: Arquivo local contendo funções auxiliares que fazem as requisições à API externa para buscar dados sobre as plataformas,
    contas e insights. As funções importadas deste arquivo são:
   - `fetch_platforms()`: Recupera as plataformas disponíveis na API.
   - `fetch_accounts_and_fields()`: Recupera as contas e os campos associados a cada uma das plataformas específicas.
   - `fetch_insights()`: Recupera os dados de insights de anúncios de uma plataforma ou conta específica.
   - `main()`: Função principal (presumivelmente usada para iniciar algum processo dentro do projeto, como a configuração ou inicialização 
    de algo).
   
3. **collections**:
   - `defaultdict`: Usado para criar um dicionário com valores padrão para casos em que uma chave não existe ainda. É especialmente útil 
    para o agrupamento e soma de dados nos relatórios.
"""
app = Flask(__name__)

@app.route('/')
def home():
    """
    Função responsável pela rota principal ('/'), que retorna informações pessoais do desenvolvedor, como nome, email, 
    LinkedIn e GitHub. Este endpoint serve como uma página inicial básica da aplicação.
    Retorna:
        - Informações pessoais do desenvolvedor em formato HTML.
    """
    return '''
    <h1>Informações Pessoais</h1>
    <p>Nome: Pedro Medeiros</p>
    <p>Email: contato@pedromedeiros.com.br</p>
    <p>LinkedIn: <a href="https://www.linkedin.com/in/-pedro-medeiros/">Perfil LinkedIn</a></p>
    <p>GitHub: <a href="https://github.com/PEDR0-MEDEIR0S">Perfil GitHub</a></p>
    '''


@app.route('/geral')
def geral():
    """
    Função que lida com a rota '/geral', gerando um relatório completo de todas as plataformas de anúncios. 
    Para cada plataforma, são obtidos os dados de contas e insights, e esses dados são formatados separado por vírgulas, 
    que é retornado como resposta. O relatório inclui informações como cliques, impressões, gasto, CPC e CTR.
    Retorna:
        - Um relatorio separado por vírgulas, gerado com os dados de todas as plataformas.
        - Caso não haja dados, retorna uma mensagem de erro "Sem dados disponíveis".
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

    if not all_insights_data:
        return "Sem dados disponíveis", 404

    headers = ['Platform', 'Ad Name', 'clicks', 'impressions', 'spend', 'cpc', 'ctr']
    csv_data = ",".join(headers) + "\n"
    
    for insight in all_insights_data:
        row = [
            insight.get("Platform", ""),
            insight.get("Ad Name", ""),
            str(insight.get("clicks", "")),
            str(insight.get("impressions", "")),
            str(insight.get("spend", "")),
            str(insight.get("cpc", "")),
            str(insight.get("ctr", ""))
        ]
        csv_data += ",".join(row) + "\n"
    
    return Response(csv_data, mimetype="text/plain")


@app.route('/geral/resumo')
def geral_resumo():
    """
    Função que lida com a rota '/geral/resumo', gerando um resumo agregado de dados de todas as plataformas. 
    Os dados são agrupados por plataforma e as métricas numéricas (como cliques, impressões e gasto) são somadas. 
    Além disso, a média de CPC e CTR é calculada.
    Retorna:
        - Um relatorio separado por vírgulas, gerado com os dados agregados por plataforma.
        - Caso não haja dados, retorna uma mensagem de erro "Sem dados disponíveis".
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

    if not all_insights_data:
        return "Sem dados disponíveis", 404
    
    platform_summary = defaultdict(lambda: {
        'clicks': 0,
        'impressions': 0,
        'spend': 0.0,
        'cpc': 0.0,
        'ctr': 0.0,
        'count': 0
    })


    def safe_float(value):
        """
        Foi percebido que alguns valores possuiam casas decimais então foi pensando em uma função para converter os dados
        caso fosse necessario somar.
        Função para garantir que um valor seja convertido para float, se possível.
        """
        try:
            return float(value) if value not in ['N/A', ''] else 0.0
        except ValueError:
            return 0.0

    for insight in all_insights_data:
        platform = insight.get("Platform", "")
        platform_summary[platform]['clicks'] += insight.get("clicks", 0)
        platform_summary[platform]['impressions'] += insight.get("impressions", 0)
        
        spend = insight.get("spend", "0.0")
        platform_summary[platform]['spend'] += safe_float(spend)
        
        cpc = insight.get("cpc", "0.0")
        ctr = insight.get("ctr", "0.0")
        
        platform_summary[platform]['cpc'] += safe_float(cpc)
        platform_summary[platform]['ctr'] += safe_float(ctr)
        
        platform_summary[platform]['count'] += 1

    headers = ['Platform', 'Ad Name', 'clicks', 'impressions', 'spend', 'cpc', 'ctr']
    csv_data = ",".join(headers) + "\n"

    for platform, data in platform_summary.items():
        avg_cpc = data['cpc'] / data['count'] if data['count'] > 0 else 0
        avg_ctr = data['ctr'] / data['count'] if data['count'] > 0 else 0

        def format_float(value):
            return f"{value:.2f}" if value != int(value) else str(int(value))
        
        row = [
            platform,
            str(data['count']),
            str(data['clicks']),
            str(data['impressions']),
            format_float(data['spend']),
            format_float(avg_cpc),
            format_float(avg_ctr)
        ]
        csv_data += ",".join(row) + "\n"

    return Response(csv_data, mimetype="text/plain")


@app.route('/<plataforma>')
def plataforma_data(plataforma):
    """
    Função que lida com a rota '/<plataforma>', onde o parâmetro `<plataforma>` representa o nome da plataforma 
    de anúncios solicitada. A função retorna um relatório de dados sobre os anúncios veiculados 
    na plataforma especificada.
    Retorna:
        - Um relatorio separado por vírgulas, com dados da plataforma solicitada.
        - Caso a plataforma não seja encontrada ou não tenha dados, retorna uma mensagem de erro apropriada.
    """
    platforms = fetch_platforms()
    
    platform_found = None
    for platform in platforms:

        if platform['text'].replace(" ", "_").lower() == plataforma.lower():
            platform_found = platform
            break
    
    if not platform_found:
        return f"Plataforma '{plataforma}' não encontrada.", 404
    
    platform_value = platform_found['value']
    print(f"Processando plataforma: {platform_value}")
    
    platform_data = fetch_accounts_and_fields(platform_value)
    
    if not platform_data:
        return f"Sem dados disponíveis para a plataforma {plataforma}.", 404

    all_insights_data = []
    insights_data = fetch_insights(platform_data)
    all_insights_data.extend(insights_data)

    if not all_insights_data:
        return f"Sem dados de insights para a plataforma {plataforma}.", 404
    
    headers = ['Platform', 'Ad Name', 'clicks', 'impressions', 'spend', 'cpc', 'ctr']
    csv_data = ",".join(headers) + "\n"
    
    for insight in all_insights_data:
        row = [
            insight.get("Platform", ""),
            insight.get("Ad Name", ""),
            str(insight.get("clicks", "")),
            str(insight.get("impressions", "")),
            str(insight.get("spend", "")),
            str(insight.get("cpc", "")),
            str(insight.get("ctr", ""))
        ]
        csv_data += ",".join(row) + "\n"
    
    return Response(csv_data, mimetype="text/plain")


@app.route('/<plataforma>/resumo')
def plataforma_resumo(plataforma):
    """
    Função que lida com a rota '/<plataforma>/resumo', onde o parâmetro `<plataforma>` representa o nome da plataforma 
    de anúncios solicitada. Retorna um resumo agregado dos dados de anúncios da plataforma especificada, somando os valores 
    de métricas como cliques, impressões, gasto, CPC e CTR, além de calcular as médias de CPC e CTR.
    Retorna:
        - Um relatorio separado por vírgulas, com os dados agregados por plataforma.
        - Caso a plataforma não seja encontrada ou não tenha dados, retorna uma mensagem de erro apropriada.
    """
    platforms = fetch_platforms()
    
    platform_found = None
    for platform in platforms:
        if platform['text'].replace(" ", "_").lower() == plataforma.lower():
            platform_found = platform
            break
    
    if not platform_found:
        return f"Plataforma '{plataforma}' não encontrada.", 404
    
    platform_value = platform_found['value']
    print(f"Processando plataforma: {platform_value}")
    
    platform_data = fetch_accounts_and_fields(platform_value)
    
    if not platform_data:
        return f"Sem dados disponíveis para a plataforma {plataforma}.", 404

    all_insights_data = []
    insights_data = fetch_insights(platform_data)
    all_insights_data.extend(insights_data)

    if not all_insights_data:
        return f"Sem dados de insights para a plataforma {plataforma}.", 404

    platform_summary = {
        'Platform': platform_value,
        'Ad Name': 'Total',
        'clicks': 0,
        'impressions': 0,
        'spend': 0.0,
        'cpc': 0.0,
        'ctr': 0.0
    }
    
    for insight in all_insights_data:
        platform_summary['clicks'] += int(insight.get("clicks", 0))
        platform_summary['impressions'] += int(insight.get("impressions", 0))
        spend = insight.get("spend", '0.0')
        platform_summary['spend'] += float(spend if spend != 'N/A' else 0.0)
        
        cpc = insight.get("cpc", '0.0')
        platform_summary['cpc'] += float(cpc if cpc != 'N/A' else 0.0)

        ctr = insight.get("ctr", '0.0')
        platform_summary['ctr'] += float(ctr if ctr != 'N/A' else 0.0)
    
    ad_count = len(all_insights_data)
    if ad_count > 0:
        platform_summary['cpc'] = round(platform_summary['cpc'] / ad_count, 3)
        platform_summary['ctr'] = round(platform_summary['ctr'] / ad_count, 3)
    
    headers = ['Platform', 'Ad Name', 'clicks', 'impressions', 'spend', 'cpc', 'ctr']
    csv_data = ",".join(headers) + "\n"
    
    row = [
        platform_summary['Platform'],
        platform_summary['Ad Name'],
        str(platform_summary['clicks']),
        str(platform_summary['impressions']),
        str(round(platform_summary['spend'], 2)),
        str(platform_summary['cpc']),
        str(platform_summary['ctr'])
    ]
    csv_data += ",".join(row) + "\n"
    
    return Response(csv_data, mimetype="text/plain")

app = Flask(__name__)

def display_available_links():
    """
    Função que exibe links disponíveis para acesso aos diferentes relatórios da aplicação. 
    Ela imprime os links no console, permitindo fácil acesso aos endpoints da aplicação para os utilizadores.
    Retorna:
        - Exibe os links no console para as rotas '/geral', '/geral/resumo' e para cada plataforma disponível.
    """
    print("\n--- Links disponíveis para acesso ---")
    platforms = fetch_platforms()
    
    base_url = "http://127.0.0.1:5000"
    
    print(f"Link geral: {base_url}/geral")

    print(f"Link geral: {base_url}/geral/resumo")
    
    for platform in platforms:
        platform_value = platform['value']
        platform_text = platform['text'].replace(" ", "_").lower()
        print(f"Link para a plataforma {platform['text']}: {base_url}/{platform_text}")
        print(f"Link para o resumo da plataforma {platform['text']}: {base_url}/{platform_text}/resumo")
    
    print("\n--- Fim dos links ---")


if __name__ == '__main__':
    display_available_links()
    app.run(debug=True)
    main()
