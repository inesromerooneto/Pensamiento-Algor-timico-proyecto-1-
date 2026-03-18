def leer_tareas(nombre_archivo):
    tareas = []

    with open(nombre_archivo, "r") as archivo:
        for linea in archivo:
            linea = linea.strip()  # sacar saltos de línea

            if linea == "":
                continue  # saltar líneas vacías

            partes = linea.split(",")

            tarea = {
                "id": partes[0],
                "duracion": int(partes[1]),
                "categoria": partes[2]
            }

            tareas.append(tarea)

    return tareas

def leer_recursos(nombre_archivo):
    recursos = []

    with open(nombre_archivo, "r") as archivo:
        for linea in archivo:
            linea = linea.strip()

            if linea == "":
                continue

            partes = linea.split(",")

            recurso = {
                "id": partes[0],
                "categorias": partes[1:]  # todas las demás columnas
            }

            recursos.append(recurso)

    return recursos

def recursos_compatibles(tarea, recursos):
    compatibles = []

    for recurso in recursos:
        if tarea["categoria"] in recurso["categorias"]:
            compatibles.append(recurso)

    return compatibles

def crear_disponibilidad(recursos):
    disponibilidad = {}

    for recurso in recursos:
        disponibilidad[recurso["id"]] = 0

    return disponibilidad

def elegir_recurso(compatibles, disponibilidad):
    mejor = compatibles[0]

    for recurso in compatibles:
        if disponibilidad[recurso["id"]] < disponibilidad[mejor["id"]]:
            mejor = recurso

    return mejor