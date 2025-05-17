import folium
import webbrowser
from modelo import G, lugares

def mostrar_mapa(camino, distancia_total):
    m = folium.Map(location=(4.7, -74.05), zoom_start=12)

    for lugar, (lat, lon) in lugares.items():
        folium.Marker(
            location=(lat, lon),
            popup=f"{lugar}\n{lat:.5f}, {lon:.5f}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    for u, v, d in G.edges(data=True):
        loc1 = G.nodes[u]['pos']
        loc2 = G.nodes[v]['pos']
        folium.PolyLine([loc1, loc2], color='gray', weight=2, opacity=0.5).add_to(m)

    for i in range(len(camino) - 1):
        loc1 = G.nodes[camino[i]]['pos']
        loc2 = G.nodes[camino[i + 1]]['pos']
        folium.PolyLine([loc1, loc2], color='red', weight=5, tooltip=f"{camino[i]} → {camino[i+1]}").add_to(m)

    m.save('ruta_optima.html')
    webbrowser.open('ruta_optima.html')