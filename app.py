#  ╔═══╦═════════╗
#  ║ 1 ║ SET UP  ║
#  ╚═══╩═════════╝


# Dash packages
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State, ALL
import dash_leaflet as dl
from dash_leaflet import express as dlx


# Data packages
import json
import utils


# Listas
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

UFS = [uf for uf in utils.lista_ufs()]
COLORS = [
    'default', 'royal', 'ruby', 'maize', 'volt'
]


def get_info(feature=None, kpi=None, uf='AC'):
    header = [html.H4(utils.lista_ufs()[uf]['Nome'])]
    if not feature:
        return header + ["Escolha um município"]
    return header + [html.B(feature["properties"]["name"]), html.Br(),
                     f'{kpi}: {float(feature["properties"][kpi])}%']




#  ╔═══╦════════════╗
#  ║ 2 ║ FRONT END  ║
#  ╚═══╩════════════╝


# Criar Dash App
app = dash.Dash(external_stylesheets=[dbc.themes.SANDSTONE])
app.title = 'Indicadores Municipais'
app.layout = html.Div([
    
    dcc.Store('memory_kpi', data='Lixo Coletado'),
    dcc.Store('memory_color', data='default'),
    dcc.Location(id='location'),
    
    dbc.NavbarSimple([
        dbc.DropdownMenu(
            [html.A(
                dbc.DropdownMenuItem(
                    [html.Span(html.Img(src=utils.bandeiras(uf, 20))),
                     html.Span('  ' + utils.lista_ufs()[uf]['Nome'])],
                    id = {'uf_menu_item': uf}), href='/'+uf) for uf in UFS],
            direction = 'left',
            nav = True,
            in_navbar = True,
            label = 'UF',
            id = 'button_uf'
        ),
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem(kpi, id = {'item_kpi': kpi}) for kpi in KPIS],
            direction = 'left',
            nav = True,
            in_navbar = True,
            label = 'Indicador',
            id = 'button_kpi'
        ),
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem(
                    [html.Span(html.Img(src=f'/assets/{color}.png', height=20)),
                     html.Span('  ' + color)],
                    id = {'item_color': color},
                    n_clicks_timestamp = 0
                ) for color in COLORS],
            direction = 'left',
            nav = True,
            in_navbar = True,
            label = 'Paleta de Cores',
            id = 'button_color'
        ),
    ],
    brand = "Mapa de Indicadores Municipais",
    brand_href = "#",
    color = "primary",
    dark = True,
),
    
    dbc.Container([
        dbc.Row(style={'width': '100%', 'height': '90vh', 'margin': "auto", "display": "block"}, id="map")
    ])
    
])




#  ╔═══╦═════════╗
#  ║ 3 ║ SERVER  ║
#  ╚═══╩═════════╝


# Trocar paleta de cores
@app.callback([Output('button_color', 'label'),
               Output('memory_color', 'data')],
              [Input({'item_color': ALL}, 'n_clicks_timestamp')])
def set_colorpallet(click):
    color = COLORS[click.index(max(click))]
    return color, color


# Carregar mapa
@app.callback([Output('map', 'children'),
               Output('button_kpi', 'label'),
               Output('button_uf', 'label'),
               Output('memory_kpi', 'data')],
              [Input({'item_kpi': ALL}, 'n_clicks'),
               Input('location', 'pathname'),
               Input('memory_color', 'data')])
def set_kpi(click, pathname, color):
    
    try:
        uf = pathname[1:]
        uf_dict = utils.lista_ufs()[uf]
    except:
        raise dash.exceptions.PreventUpdate
    
    # Identificar botão apertado
    kpi = dash.callback_context.triggered[0]['prop_id'][13:-11]
    if kpi == '':
        kpi = KPIS[0]
        
    # Baixar JSON
    with open(f'data/{uf}_geo.json', 'r') as js:
        geo = json.load(js)
    
    # Criar colorbar
    marks = utils.get_values(geo, kpi)[0]
    marks = [int(mark) for mark in marks]
    ctg = ["{}+".format(mark, marks[i + 1]) for i, mark in enumerate(marks[:-1])] + ["{}+".format(marks[-1])]
    colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=utils.get_colorscale(color), width=300, height=30, position="bottomleft")
    
    # Criar geojson
    options = {'hoverStyle': {'weight': 5, 'color': '#666', 'dashArray': ''}, 'zoomToBoundsOnClick': True}
    geojson = utils.geojson(geo, colorscale=color, kpi=kpi, id="geojson", defaultOptions=options)
    
    # Criar caixa de informações
    info = html.Div(children=get_info(), id="info", className="info",
                    style={"position": "absolute", "bottom": "10px", "right": "10px", "z-index": "1000"})
    
    return dl.Map(
        children = [dl.TileLayer(), geojson, colorbar, info],
        center = [uf_dict['Latitude'], uf_dict['Longitude']]
    ), kpi, uf, kpi


# Atualizar caixa de informações
@app.callback(Output("info", "children"),
             [Input("geojson", "featureHover")],
             [State('memory_kpi', 'data'),
              State('location', 'pathname')])
def info_hover(feature, data, uf):
    return get_info(feature, kpi=data, uf=uf[1:])


# Rodar server
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='8050', debug=False)