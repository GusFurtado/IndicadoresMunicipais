'''
O Projeto Mapa de Indicadores Municipais pode ser separado nas seguintes etapas:

- Capturar dados abertos do IBGE através da biblioteca Dados Abertos Brasil;
- Inserir os dados capturados em um arquivo GeoJSON;
- Carregar o novo GeoJSON em um mapa Leaflet;
- Construir uma interface de inputs e callbacks via Dash;
- Deploy do app no Heroku
'''



import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State, ALL
import dash_leaflet as dl
from dash_leaflet import express as dlx

import utils



KPIS = [
    'Taxa de Alfabetização',
    'População Economicamente Ativa',
    'População sem Religião',
    'População Indígena',
    'Lixo Coletado',
    'Energia Elétrica',
    'Rede Geral de Abastecimento de Água',
    'Sem Banheiro ou Sanitário'
]

UFS = sorted([uf for uf in utils.lista_ufs()])

COLORS = [
    'default',
    'royal',
    'ruby',
    'maize',
    'volt',
    'portal'
]



def get_info(feature=None, kpi=None, uf='AC'):

    header = [
        html.H4(
            utils.lista_ufs()[uf]['Nome'],
            style = {
                'margin': '0 0 5px',
                'color': '#777'
            }
        )
    ]

    if not feature:
        return header + ["Escolha um município"]

    return header + [
        html.B(
            feature["properties"]["name"]
        ),
        html.Br(),
        f'{kpi}: {float(feature["properties"][kpi])}%'
    ]



app = dash.Dash(external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server
app.title = 'Indicadores Municipais'
app.layout = html.Div([
    
    dcc.Location('memory_uf'),
    dcc.Store('memory_kpi', storage_type='session'),
    dcc.Store('memory_color', storage_type='session'),
    
    dbc.NavbarSimple([
            
        dbc.DropdownMenu([
            html.A(
                dbc.DropdownMenuItem([
                    html.Span(html.Img(src=utils.bandeiras(uf, 20))),
                    html.Span('  ' + utils.lista_ufs()[uf]['Nome'])
                ],
                    id = {'uf_menu_item': uf}
                ),
                href = '/'+uf
            ) for uf in UFS
        ],
            direction = 'left',
            nav = True,
            in_navbar = True,
            label = 'UF',
            id = 'button_uf'
        ),
    
        dbc.DropdownMenu([
            dbc.DropdownMenuItem(
                kpi,
                n_clicks_timestamp = 0,
                id = {'item_kpi': kpi}
            ) for kpi in KPIS
        ],
            direction = 'left',
            nav = True,
            in_navbar = True,
            label = 'Indicador',
            id = 'button_kpi'
        ),
    
        dbc.DropdownMenu([
            dbc.DropdownMenuItem([
                html.Span(
                    html.Img(
                        src = f'https://raw.githubusercontent.com/GusFurtado/IndicadoresMunicipais/master/assets/{color}.png',
                        height=20
                    )
                ),
                html.Span('  ' + color)
            ],
                n_clicks_timestamp = 0,
                id = {'item_color': color}
            ) for color in COLORS
        ],
            direction = 'left',
            nav = True,
            in_navbar = True,
            label = 'Paleta de Cores',
            id = 'button_color'
        ),
    ],
    brand = 'Dados Abertos Brasil',
    brand_style = {
        'font-weight': 'bold',
        'color': '#FEDF00'
    },
    brand_href = "https://www.gustavofurtado.com/dab.html",
    color = "primary",
    dark = True,
),
    
    html.Div([
        dbc.Row(
            style = {
                'width': '100%',
                'height': '90vh',
                'margin': "auto",
                "display": "block"
            },
            id = "map"
        )
    ])
])



@app.callback(
    [Output('button_kpi', 'label'),
    Output('memory_kpi', 'data')],
    [Input({'item_kpi': ALL}, 'n_clicks_timestamp')])
def set_kpi(click):
    kpi = KPIS[click.index(max(click))]
    return kpi, kpi



@app.callback(
    [Output('button_color', 'label'),
    Output('memory_color', 'data')],
    [Input({'item_color': ALL}, 'n_clicks_timestamp')])
def set_color(click):
    color = COLORS[click.index(max(click))]
    return color, color



@app.callback(
    [Output('map', 'children'),
    Output('button_uf', 'label')],
    [Input('memory_kpi', 'data'),
    Input('memory_color', 'data')],
    [State('memory_uf', 'pathname')],
    prevent_initial_call = True)
def load_leaflet(kpi, color, uf):
    
    try:
        uf = uf[1:]
        uf_dict = utils.lista_ufs()[uf]
    except:
        uf = 'SP'
        uf_dict = utils.lista_ufs()[uf]
        
        
    with open(f'data/{uf}_geo.json', 'r') as js:
        geo = json.load(js)
    
    marks = utils.get_values(geo, kpi)[0]
    marks = [int(mark) for mark in marks]
    ctg = ["{}+".format(mark, marks[i + 1]) for i, mark in enumerate(marks[:-1])] \
        + ["{}+".format(marks[-1])]
    colorbar = dlx.categorical_colorbar(
        categories = ctg,
        colorscale = utils.get_colorscale(color),
        width = 300,
        height = 30,
        position = "bottomleft"
    )

    options = {
        'hoverStyle': {
            'weight': 5,
            'color': '#666',
            'dashArray': ''
        },
        'zoomToBoundsOnClick': True
    }

    geojson = utils.geojson(
        geo,
        colorscale = color,
        kpi = kpi,
        id = "geojson",
        defaultOptions = options
    )

    info = html.Div(
        children = get_info(),
        id = "info",
        className = "info",
        style = {
            "position": "absolute",
            "bottom": "10px",
            "right": "10px",
            "z-index": "1000",
            'padding': '6px 8px',
            'font': '14px/16px Arial, Helvetica, sans-serif',
            'background': 'rgba(255,255,255,0.8)',
            'box-shadow': '0 0 15px rgba(0,0,0,0.2)',
            'border-radius': '5px'
        }
    )
    
    return dl.Map(
        children = [
            dl.TileLayer(),
            geojson,
            colorbar,
            info
        ],

        center = [
            uf_dict['Latitude'],
            uf_dict['Longitude']
        ]
    ), uf



@app.callback(
    Output("info", "children"),
    [Input("geojson", "featureHover")],
    [State('memory_kpi', 'data'),
    State('memory_uf', 'pathname')])
def info_hover(feature, data, uf):
    if uf == '/':
        uf = '/SP'
    return get_info(feature, kpi=data, uf=uf[1:])



if __name__ == '__main__':
    app.run_server(
        host = '0.0.0.0',
        port = '8050',
        debug = False
    )