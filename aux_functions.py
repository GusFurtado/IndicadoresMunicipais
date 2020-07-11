import requests

from bs4 import BeautifulSoup
import pandas as pd


# Lista de Unidades Federativas
def lista_ufs():
    return ['AC - Acre',              'AL - Alagoas',              'AP - Amapá',
            'AM - Amazonas',          'BA - Bahia',                'CE - Ceará',
            'DF - Distrito Federal',  'ES - Espírito Santo',       'GO - Goiás',
            'MA - Maranhão',          'MT - Mato Grosso',          'MS - Mato Grosso do Sul',
            'MG - Minas Gerais',      'PA - Pará',                 'PB - Paraíba',
            'PR - Paraná',            'PE - Pernambuco',           'PI - Piauí',
            'RJ - Rio de Janeiro',    'RN - Rio Grande do Norte',  'RS - Rio Grande do Sul',
            'RO - Rondônia',          'RR - Roraima',              'SC - Santa Catarina',
            'SP - São Paulo',         'SE - Sergipe',              'TO - Tocantins']


# Baixar lista de municípios do Wikipedia
def lista_municipios():

    # Request soup
    s = requests.Session()
    html = s.get(r'https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Brasil_por_popula%C3%A7%C3%A3o').text
    soup = BeautifulSoup(html, 'html.parser')

    # Scrapping
    table = soup.find_all('table', 'wikitable')
    tbody = table[0].find('tbody')
    header = [th.text.replace('\n', '') for th in tbody.find_all('th')]
    data = [[td.text.replace('\n', '').replace(u'\xa0', '') for td in tr.find_all('td')] for tr in tbody.find_all('tr')][1:]

    # DataFrame
    df = pd.DataFrame(data, columns=header)
    df['href'] = [td.find('a')['href'] for td in tbody.find_all('tr')[1:]]
    
    return df