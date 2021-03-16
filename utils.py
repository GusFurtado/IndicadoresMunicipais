import requests

import dash_leaflet as dl
from bs4 import BeautifulSoup
import pandas as pd



def lista_ufs() -> dict:
    '''
    Lista de atributos das Unidades da Federação.

    Retorna
    -------
    dict
        Dictionary em que cada key é uma sigla de uma UF e cada value é um
        dictionary de atributos de mesma UF, contendo nome, área, latitude e
        longitude.
    
    --------------------------------------------------------------------------
    '''
    
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



def lista_municipios():
    '''
    Capturar lista de municípios do Wikipedia e seus respectivos atributos.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Tabela de municípios do Wikipedia convertida em DataFrame.

    --------------------------------------------------------------------------
    '''

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



def get_colorscale(color:str) -> list:
    '''
    Paleta de cores para o mapa da aplicação.

    Parâmetros
    ----------
    color : str
        Nome da paleta de cores, sendo uma das seguintes opções:
        'default', 'royal', 'ruby', 'maize', 'volt' ou 'portal'.

    Retorna
    -------
    list of string
        Lista de oito hexcodes das cores da paleta.

    --------------------------------------------------------------------------
    '''
    
    colorscales = {
        'default': ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026'],
        'royal':   ['#EDF1FC', '#B9C9F3', '#85A2EA', '#517AE1', '#2355D1', '#1B409D', '#122A69', '#091534'],
        'ruby':    ['#FDEDEE', '#F7B6BA', '#F17E86', '#EB4752', '#DC1826', '#A5121C', '#6E0C13', '#370609'],
        'maize':   ['#FFFCEB', '#FFF3AD', '#FFEA70', '#FFE033', '#F5D000', '#B89C00', '#7A6800', '#3D3400'],
        'volt':    ['#FBFFEB', '#EFFFAD', '#E2FF70', '#D6FF33', '#C4F500', '#93B800', '#627A00', '#313D00'],
        'portal':  ['#FF5D00', '#FF9A00', '#FFBE5C', '#FFDEAD', '#ADE1FF', '#5CC3FF', '#00A2FF', '#0065FF']
    }
    
    return colorscales[color]



def get_values(data, kpi):
    '''
    Gera pontos de referência da paleta de cores em função dos maiores e
    menores valores da série

    --------------------------------------------------------------------------
    '''
    
    values = [float(feature['properties'][kpi]) for feature in data['features']]
    mx = max(values)
    mn = min(values)

    return [mn + i*(mx-mn)/8 for i in range(8)], values
    


def _features_style(data, kpi, colorscale):

    marks, values = get_values(data, kpi)
    cs = get_colorscale(colorscale)
    
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