import networkx as nx
from geopy.distance import geodesic

lugares = {
    "Centro Comercial Santafe": (4.7630560, -74.0456679),
    "Centro Comercial Unicentro": (4.7018081, -74.0412263),
    "Arturo Calle 153": (4.7411318, -74.0647445),
}

G = nx.Graph()

def reconstruir_grafo():
    G.clear()
    for lugar1, coord1 in lugares.items():
        G.add_node(lugar1, pos=coord1)
        for lugar2, coord2 in lugares.items():
            if lugar1 != lugar2:
                dist = geodesic(coord1, coord2).meters
                G.add_edge(lugar1, lugar2, weight=dist)

def dijkstra(grafo, inicio, fin):
    import heapq
    dist = {n: float('inf') for n in grafo}
    prev = {n: None for n in grafo}
    dist[inicio] = 0
    heap = [(0, inicio)]
    while heap:
        actual_dist, actual = heapq.heappop(heap)
        if actual == fin:
            break
        for vecino in grafo[actual]:
            peso = grafo[actual][vecino]['weight']
            nueva_dist = actual_dist + peso
            if nueva_dist < dist[vecino]:
                dist[vecino] = nueva_dist
                prev[vecino] = actual
                heapq.heappush(heap, (nueva_dist, vecino))
    camino = []
    nodo = fin
    while nodo:
        camino.insert(0, nodo)
        nodo = prev[nodo]
    return camino, dist[fin]