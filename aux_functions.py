import requests

from bs4 import BeautifulSoup
import pandas as pd


# Lista de Unidades Federativas
def lista_ufs():
    
    return {
        
        # Região Norte
        'AC': {'Nome': 'Acre',
               'Latitude': -8.77,
               'Longitude': -70.55},
        'AM': {'Nome': 'Amazonas',
               'Latitude': -3.47,
               'Longitude': -65.10},
        'AP': {'Nome': 'Amapá',
               'Latitude': 1.41,
               'Longitude': -51.77},
        'PA': {'Nome': 'Pará',
               'Latitude': -3.79,
               'Longitude': -52.48},
        'RO': {'Nome': 'Rondônia',
               'Latitude': -10.83,
               'Longitude': -63.34},
        'RR': {'Nome': 'Roraima',
               'Latitude': 1.99,
               'Longitude': -61.33},
        'TO': {'Nome': 'Tocantins',
               'Latitude': -9.46,
               'Longitude': -48.26},
        
        # Região Nordeste
        'AL': {'Nome': 'Alagoas',
               'Latitude': -9.62,
               'Longitude': -36.82},
        'BA': {'Nome': 'Bahia',
               'Latitude': -13.29,
               'Longitude': -41.71},
        'CE': {'Nome': 'Ceará',
               'Latitude': -5.20,
               'Longitude': -39.53},
        'MA': {'Nome': 'Maranhão',
               'Latitude': -5.42,
               'Longitude': -45.44},
        'PB': {'Nome': 'Paraíba',
               'Latitude': -7.28,
               'Longitude': -36.72},
        'PE': {'Nome': 'Pernambuco',
               'Latitude': -8.38,
               'Longitude': -37.86},
        'PI': {'Nome': 'Piauí',
               'Latitude': -6.60,
               'Longitude': -42.28},
        'RN': {'Nome': 'Rio Grande do Norte',
               'Latitude': -5.81,
               'Longitude': -36.59},
        'SE': {'Nome': 'Sergipe',
               'Latitude': -10.57,
               'Longitude': -37.45},
        
        # Região Centro-Oeste
        'DF': {'Nome': 'Distrito Federal',
               'Latitude': -15.83,
               'Longitude': -47.86},
        'GO': {'Nome': 'Goiás',
               'Latitude': -15.98,
               'Longitude': -49.86},
        'MT': {'Nome': 'Mato Grosso',
               'Latitude': -12.64,
               'Longitude': -55.42},
        'MS': {'Nome': 'Mato Grosso do Sul',
               'Latitude': -20.51,
               'Longitude': -54.54},
        
        # Região Sudeste
        'ES': {'Nome': 'Espírito Santo',
               'Latitude': -19.19,
               'Longitude': -40.34},
        'MG': {'Nome': 'Minas Gerais',
               'Latitude': -18.10,
               'Longitude': -44.38},
        'RJ': {'Nome': 'Rio de Janeiro',
               'Latitude': -22.25,
               'Longitude': -42.66},
        'SP': {'Nome': 'São Paulo',
               'Latitude': -22.19,
               'Longitude': -48.79},
        
        # Região Sul
        'PR': {'Nome': 'Paraná',
               'Latitude': -24.89,
               'Longitude': -51.55},
        'RS': {'Nome': 'Rio Grande do Sul',
               'Latitude': -30.17,
               'Longitude': -53.50},
        'SC': {'Nome': 'Santa Catarina',
               'Latitude': -27.45,
               'Longitude': -50.95}
        
    }


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


# Gera URL da WikiMedia para a bandeira de um estado de um tamanho escolhido
def bandeiras(uf, tamanho=100):
    
    url = r'https://upload.wikimedia.org/wikipedia/commons/thumb/'
    
    bandeira = {

        # Região Norte
        'AC': f'4/4c/Bandeira_do_Acre.svg/{tamanho}px-Bandeira_do_Acre.svg.png',
        'AM': f'6/6b/Bandeira_do_Amazonas.svg/{tamanho}px-Bandeira_do_Amazonas.svg.png',
        'AP': f'0/0c/Bandeira_do_Amap%C3%A1.svg/{tamanho}px-Bandeira_do_Amap%C3%A1.svg.png',
        'PA': f'0/02/Bandeira_do_Par%C3%A1.svg/{tamanho}px-Bandeira_do_Par%C3%A1.svg.png',
        'RO': f'f/fa/Bandeira_de_Rond%C3%B4nia.svg/{tamanho}px-Bandeira_de_Rond%C3%B4nia.svg.png',
        'RR': f'9/98/Bandeira_de_Roraima.svg/{tamanho}px-Bandeira_de_Roraima.svg.png',
        'TO': f'f/ff/Bandeira_do_Tocantins.svg/{tamanho}px-Bandeira_do_Tocantins.svg.png',

        # Região Nordeste
        'AL': f'8/88/Bandeira_de_Alagoas.svg/{tamanho}px-Bandeira_de_Alagoas.svg.png',
        'BA': f'2/28/Bandeira_da_Bahia.svg/{tamanho}px-Bandeira_da_Bahia.svg.png',
        'CE': f'2/2e/Bandeira_do_Cear%C3%A1.svg/{tamanho}px-Bandeira_do_Cear%C3%A1.svg.png',
        'MA': f'4/45/Bandeira_do_Maranh%C3%A3o.svg/{tamanho}px-Bandeira_do_Maranh%C3%A3o.svg.png',
        'PB': f'b/bb/Bandeira_da_Para%C3%ADba.svg/{tamanho}px-Bandeira_da_Para%C3%ADba.svg.png',
        'PE': f'5/59/Bandeira_de_Pernambuco.svg/{tamanho}px-Bandeira_de_Pernambuco.svg.png',
        'PI': f'3/33/Bandeira_do_Piau%C3%AD.svg/{tamanho}px-Bandeira_do_Piau%C3%AD.svg.png',
        'RN': f'3/30/Bandeira_do_Rio_Grande_do_Norte.svg/{tamanho}px-Bandeira_do_Rio_Grande_do_Norte.svg.png',
        'SE': f'b/be/Bandeira_de_Sergipe.svg/{tamanho}px-Bandeira_de_Sergipe.svg.png',

        # Região Centro-Oeste
        'DF': f'3/3c/Bandeira_do_Distrito_Federal_%28Brasil%29.svg/{tamanho}px-Bandeira_do_Distrito_Federal_%28Brasil%29.svg.png',
        'GO': f'b/be/Flag_of_Goi%C3%A1s.svg/{tamanho}px-Flag_of_Goi%C3%A1s.svg.png',
        'MT': f'0/0b/Bandeira_de_Mato_Grosso.svg/{tamanho}px-Bandeira_de_Mato_Grosso.svg.png',
        'MS': f'6/64/Bandeira_de_Mato_Grosso_do_Sul.svg/{tamanho}px-Bandeira_de_Mato_Grosso_do_Sul.svg.png',

        # Região Sudeste
        'ES': f'4/43/Bandeira_do_Esp%C3%ADrito_Santo.svg/{tamanho}px-Bandeira_do_Esp%C3%ADrito_Santo.svg.png',
        'MG': f'f/f4/Bandeira_de_Minas_Gerais.svg/{tamanho}px-Bandeira_de_Minas_Gerais.svg.png',
        'RJ': f'7/73/Bandeira_do_estado_do_Rio_de_Janeiro.svg/{tamanho}px-Bandeira_do_estado_do_Rio_de_Janeiro.svg.png',
        'SP': f'2/2b/Bandeira_do_estado_de_S%C3%A3o_Paulo.svg/{tamanho}px-Bandeira_do_estado_de_S%C3%A3o_Paulo.svg.png',

        # Região Sul
        'PR': f'9/93/Bandeira_do_Paran%C3%A1.svg/{tamanho}px-Bandeira_do_Paran%C3%A1.svg.png',
        'RS': f'6/63/Bandeira_do_Rio_Grande_do_Sul.svg/{tamanho}px-Bandeira_do_Rio_Grande_do_Sul.svg.png',
        'SC': f'1/1a/Bandeira_de_Santa_Catarina.svg/{tamanho}px-Bandeira_de_Santa_Catarina.svg.png'

    }
    
    return url + bandeira[uf]