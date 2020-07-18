import json

from DadosAbertosBrasil import ibge, favoritos

import utils


# Definir lista de parâmetros do SIDRA
KPIS = {
        
    'Taxa de Alfabetização': {
        'agregado': 1383,
        'periodo': 2010,
        'variaveis': 1646,
        'classificacoes': {2: 6794}
    },

    'População Economicamente Ativa': {
        'agregado': 616,
        'periodo': 2010,
        'variaveis': 1000140,
        'classificacoes': {90: 3287}
    },
    
    'População sem Religião': {
        'agregado': 137,
        'periodo': 2010,
        'variaveis': 1000093,
        'classificacoes': {133: 2836}
    },

    'População Indígena': {
        'agregado': 136,
        'periodo': 2010,
        'variaveis': 1000093,
        'classificacoes': {86: 2780}
    },
    
    'Rede Geral de Abastecimento de Água': {
        'agregado': 3218,
        'periodo': 2010,
        'variaveis': 1000096,
        'classificacoes': {61: 92853}
    },
    
    'Sem Banheiro ou Sanitário': {
        'agregado': 3218,
        'periodo': 2010,
        'variaveis': 1000096,
        'classificacoes': {299: 10006}
    },
    
    'Lixo Coletado': {
        'agregado': 3218,
        'periodo': 2010,
        'variaveis': 1000096,
        'classificacoes': {67: 2520}
    },
    
    'Energia Elétrica': {
        'agregado': 3218,
        'periodo': 2010,
        'variaveis': 1000096,
        'classificacoes': {309: 3011}
    }
    
}


# Baixar dados do SIDRA
resultados = []
for i in KPIS:
    
    print(f'Baixando dados de {i}')
    kpi = KPIS[i]

    sidra = ibge.Sidra(agregado = kpi['agregado'],
                       periodos = kpi['periodo'],
                       variaveis = kpi['variaveis'],
                       classificacoes = kpi['classificacoes'],
                       localidades = {'N6': 'all'})

    resultados.append(sidra.rodar())


# Criar GeoJSONs
UFS = [uf[:2] for uf in utils.lista_ufs()]    

for uf in UFS:
    print(f'Criando GeoJSON de {uf}')
    geo = favoritos.geojson(uf)
    for id_geo in geo['features']:
        for i, resultado in zip(KPIS, resultados):
            for id_res in resultado[0]['resultados'][0]['series']:
                if id_geo['properties']['id'] == id_res['localidade']['id']:
                    try:
                        value = float(id_res['serie'][str(kpi['periodo'])])
                    except:
                        value = 0
                    id_geo['properties'].update({i: value})
                    break

    with open(f'data/{uf}_geo.json', 'w') as f:
        json.dump(geo, f)

print('Fim.')