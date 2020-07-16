import requests

import dash_leaflet as dl
from bs4 import BeautifulSoup
import pandas as pd


# Lista de Unidades Federativas
def lista_ufs():
    
    return {
        
        # Região Norte
        'AC': {'Nome': 'Acre',
               'Área': 164123.040,
               'Latitude': -8.77,
               'Longitude': -70.55},
        'AM': {'Nome': 'Amazonas',
               'Área': 1559159.148,
               'Latitude': -3.47,
               'Longitude': -65.10},
        'AP': {'Nome': 'Amapá',
               'Área': 142828.521,
               'Latitude': 1.41,
               'Longitude': -51.77},
        'PA': {'Nome': 'Pará',
               'Área': 1247954.666,
               'Latitude': -3.79,
               'Longitude': -52.48},
        'RO': {'Nome': 'Rondônia',
               'Área': 237590.547,
               'Latitude': -10.83,
               'Longitude': -63.34},
        'RR': {'Nome': 'Roraima',
               'Área': 224300.506,
               'Latitude': 1.99,
               'Longitude': -61.33},
        'TO': {'Nome': 'Tocantins',
               'Área': 277720.520,
               'Latitude': -9.46,
               'Longitude': -48.26},
        
        # Região Nordeste
        'AL': {'Nome': 'Alagoas',
               'Área': 27778.506,
               'Latitude': -9.62,
               'Longitude': -36.82},
        'BA': {'Nome': 'Bahia',
               'Área': 564733.177,
               'Latitude': -13.29,
               'Longitude': -41.71},
        'CE': {'Nome': 'Ceará',
               'Área': 148920.472,
               'Latitude': -5.20,
               'Longitude': -39.53},
        'MA': {'Nome': 'Maranhão',
               'Área': 331937.450,
               'Latitude': -5.42,
               'Longitude': -45.44},
        'PB': {'Nome': 'Paraíba',
               'Área': 56585.000,
               'Latitude': -7.28,
               'Longitude': -36.72},
        'PE': {'Nome': 'Pernambuco',
               'Área': 98311.616,
               'Latitude': -8.38,
               'Longitude': -37.86},
        'PI': {'Nome': 'Piauí',
               'Área': 251577.738,
               'Latitude': -6.60,
               'Longitude': -42.28},
        'RN': {'Nome': 'Rio Grande do Norte',
               'Área': 52811.047,
               'Latitude': -5.81,
               'Longitude': -36.59},
        'SE': {'Nome': 'Sergipe',
               'Área': 21915.116,
               'Latitude': -10.57,
               'Longitude': -37.45},
        
        # Região Centro-Oeste
        'DF': {'Nome': 'Distrito Federal',
               'Área': 5779.999,
               'Latitude': -15.83,
               'Longitude': -47.86},
        'GO': {'Nome': 'Goiás',
               'Área': 340111.783,
               'Latitude': -15.98,
               'Longitude': -49.86},
        'MT': {'Nome': 'Mato Grosso',
               'Área': 903366.192,
               'Latitude': -12.64,
               'Longitude': -55.42},
        'MS': {'Nome': 'Mato Grosso do Sul',
               'Área': 357145.532,
               'Latitude': -20.51,
               'Longitude': -54.54},
        
        # Região Sudeste
        'ES': {'Nome': 'Espírito Santo',
               'Área': 46095.583,
               'Latitude': -19.19,
               'Longitude': -40.34},
        'MG': {'Nome': 'Minas Gerais',
               'Área': 586522.122,
               'Latitude': -18.10,
               'Longitude': -44.38},
        'RJ': {'Nome': 'Rio de Janeiro',
               'Área': 43780.172,
               'Latitude': -22.25,
               'Longitude': -42.66},
        'SP': {'Nome': 'São Paulo',
               'Área': 248222.362,
               'Latitude': -22.19,
               'Longitude': -48.79},
        
        # Região Sul
        'PR': {'Nome': 'Paraná',
               'Área': 199307.922,
               'Latitude': -24.89,
               'Longitude': -51.55},
        'RS': {'Nome': 'Rio Grande do Sul',
               'Área': 281730.223,
               'Latitude': -30.17,
               'Longitude': -53.50},
        'SC': {'Nome': 'Santa Catarina',
               'Área': 95736.165,
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


# Função Dash-Leaflet GeoJSON customizada
def _features_style(data, kpi, colorscale):

    values = [float(feature['properties'][kpi]) for feature in data['features']]

    mx = max(values)
    mn = min(values)

    marks = [mn + i*(mx-mn)/8 for i in range(8)]

    colorscales = {
        'default': ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026'],
        'azul':    ['#EDF1FC', '#B9C9F3', '#85A2EA', '#517AE1', '#2355D1', '#1B409D', '#122A69', '#091534']
    }
    
    cs = colorscales[colorscale]
    
    style = {}
    for i, value in enumerate(values):

        color = [cs[i] for i, item in enumerate(marks) if value >= item][-1]
        style.update({
            i: {
                'fillColor': color,
                'weight': 2,
                'opacity': 1,
                'color': 'white',
                'dashArray': '3',
                'fillOpacity': 0.7
            }
        })
        
    return style

def _validate_feature_ids(data):
    ids = [f["id"] for f in data["features"] if "id" in f]
    return len(list(set(ids))) == len(data["features"])

def geojson(data, kpi, colorscale='default', *args, **kwargs):
    
    feature_id = "id"
    if not _validate_feature_ids(data):
        feature_id = "dash_id"
        for i, f in enumerate(data["features"]):
            f[feature_id] = i
    
    feature_style = _features_style(data, kpi, colorscale)
    
    return dl.GeoJSON(*args, data=data, featureStyle=feature_style, featureId=feature_id, **kwargs)