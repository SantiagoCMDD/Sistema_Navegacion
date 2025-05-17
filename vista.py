import tkinter as tk
from tkinter import ttk, messagebox
from modelo import lugares, reconstruir_grafo
from controlador import calcular_ruta, agregar_nodo, eliminar_nodo, editar_nodo

def iniciar_interfaz():
    ventana = tk.Tk()
    ventana.title("Sistema de Navegación con CRUD")

    tk.Label(ventana, text="--- Gestión de Nodos ---").pack(pady=5)
    frame_inputs = tk.Frame(ventana)
    frame_inputs.pack()

    tk.Label(frame_inputs, text="Nombre:").grid(row=0, column=0)
    entrada_nombre = tk.Entry(frame_inputs)
    entrada_nombre.grid(row=0, column=1)
    tk.Label(frame_inputs, text="Latitud:").grid(row=1, column=0)
    entrada_lat = tk.Entry(frame_inputs)
    entrada_lat.grid(row=1, column=1)
    tk.Label(frame_inputs, text="Longitud:").grid(row=2, column=0)
    entrada_lon = tk.Entry(frame_inputs)
    entrada_lon.grid(row=2, column=1)

    frame_botones = tk.Frame(ventana)
    frame_botones.pack()

    def actualizar_lista_nodos():
        for i in tree.get_children():
            tree.delete(i)
        for nombre, (lat, lon) in lugares.items():
            tree.insert('', 'end', values=(nombre, lat, lon))
        actualizar_comboboxes()

    def agregar():
        try:
            lat = float(entrada_lat.get())
            lon = float(entrada_lon.get())
        except ValueError:
            messagebox.showerror("Error", "Latitud y longitud deben ser números.")
            return
        ok, msg = agregar_nodo(entrada_nombre.get(), lat, lon)
        if not ok:
            messagebox.showerror("Error", msg)
        actualizar_lista_nodos()

    def eliminar():
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Selecciona un nodo para eliminar.")
            return
        nombre = tree.item(seleccionado[0])['values'][0]
        eliminar_nodo(nombre)
        actualizar_lista_nodos()

    def editar():
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Selecciona un nodo para editar.")
            return
        nombre_original = tree.item(seleccionado[0])['values'][0]
        try:
            lat = float(entrada_lat.get())
            lon = float(entrada_lon.get())
        except ValueError:
            messagebox.showerror("Error", "Latitud y longitud deben ser números.")
            return
        ok, msg = editar_nodo(nombre_original, entrada_nombre.get(), lat, lon)
        if not ok:
            messagebox.showerror("Error", msg)
        actualizar_lista_nodos()

    tk.Button(frame_botones, text="Agregar Nodo", command=agregar).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Editar Nodo", command=editar).grid(row=0, column=1, padx=5)
    tk.Button(frame_botones, text="Eliminar Nodo", command=eliminar).grid(row=0, column=2, padx=5)

    tree = ttk.Treeview(ventana, columns=("Nombre", "Lat", "Lon"), show='headings')
    tree.heading("Nombre", text="Nombre")
    tree.heading("Lat", text="Latitud")
    tree.heading("Lon", text="Longitud")
    tree.pack(pady=10)

    tk.Label(ventana, text="Origen:").pack()
    origen_cb = ttk.Combobox(ventana)
    origen_cb.pack()

    tk.Label(ventana, text="Destino:").pack()
    destino_cb = ttk.Combobox(ventana)
    destino_cb.pack()

    intermedios_dinamicos = []
    frame_intermedios = tk.Frame(ventana)
    frame_intermedios.pack(pady=5)
    for i in range(10):
        var = tk.BooleanVar()
        cb = ttk.Combobox(frame_intermedios)
        chk = tk.Checkbutton(frame_intermedios, text=f"¿Pasar por otro punto? ({i+1})", variable=var)
        chk.grid(row=i, column=0, sticky='w')
        cb.grid(row=i, column=1)
        intermedios_dinamicos.append((var, cb))

    def actualizar_comboboxes():
        nodos = list(lugares.keys())
        origen_cb['values'] = nodos
        destino_cb['values'] = nodos
        for _, cb in intermedios_dinamicos:
            cb['values'] = nodos

    def ejecutar_ruta():
        origen = origen_cb.get()
        destino = destino_cb.get()
        intermedios = [cb.get() for var, cb in intermedios_dinamicos if var.get()]
        camino, distancia = calcular_ruta(origen, destino, intermedios)
        if camino:
            messagebox.showinfo("Ruta Calculada", f"Ruta: {' → '.join(camino)}\nDistancia total: {round(distancia)} m")

    tk.Button(ventana, text="Calcular ruta óptima", command=ejecutar_ruta).pack(pady=10)
    actualizar_lista_nodos()
    ventana.mainloop()