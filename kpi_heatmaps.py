marks = [0, 10, 20, 30, 60, 70, 80, 90]
colorscale = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026']

def get_lixo(feature):
    color = [colorscale[i] for i, item in enumerate(marks) if float(feature["properties"]['Lixo Coletado']) > item][-1]
    return dict(fillColor=color, weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)

def get_energia(feature):
    color = [colorscale[i] for i, item in enumerate(marks) if float(feature["properties"]['Energia Elétrica']) > item][-1]
    return dict(fillColor=color, weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)

def get_agua(feature):
    color = [colorscale[i] for i, item in enumerate(marks) if float(feature["properties"]['Rede Geral de Abastecimento de Água']) > item][-1]
    return dict(fillColor=color, weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)

def get_sanitario(feature):
    color = [colorscale[i] for i, item in enumerate(marks) if float(feature["properties"]['Sem Banheiro ou Sanitário']) > item][-1]
    return dict(fillColor=color, weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)