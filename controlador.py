from modelo import lugares, reconstruir_grafo, dijkstra, G
from mapa import mostrar_mapa
from tkinter import messagebox

def calcular_ruta(origen, destino, intermedios):
    if len(set([origen] + intermedios + [destino])) != len([origen] + intermedios + [destino]):
        messagebox.showerror("Error", "No se permiten lugares repetidos.")
        return None, None
    if origen == "" or destino == "":
        messagebox.showerror("Error", "Selecciona origen y destino.")
        return None, None

    camino_total = []
    distancia_total = 0
    puntos = [origen] + intermedios + [destino]

    for i in range(len(puntos) - 1):
        tramo, dist = dijkstra(G, puntos[i], puntos[i + 1])
        if i > 0:
            tramo = tramo[1:]
        camino_total += tramo
        distancia_total += dist

    mostrar_mapa(camino_total, distancia_total)
    return camino_total, distancia_total

def agregar_nodo(nombre, lat, lon):
    if nombre in lugares:
        return False, "Ese nodo ya existe."
    lugares[nombre] = (lat, lon)
    reconstruir_grafo()
    return True, None

def eliminar_nodo(nombre):
    if nombre in lugares:
        del lugares[nombre]
        reconstruir_grafo()

def editar_nodo(nombre_original, nuevo_nombre, lat, lon):
    if nuevo_nombre != nombre_original and nuevo_nombre in lugares:
        return False, "Ese nombre ya existe."
    del lugares[nombre_original]
    lugares[nuevo_nombre] = (lat, lon)
    reconstruir_grafo()
    return True, None