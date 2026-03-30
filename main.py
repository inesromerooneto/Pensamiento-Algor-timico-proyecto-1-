from pathlib import Path
import random
import time


def leer_tareas(nombre_archivo) -> list[dict[str, object]]:
    tareas = []
    ruta = Path(__file__).resolve().parent / nombre_archivo

    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()

            if linea == "":
                continue

            partes = [p.strip() for p in linea.split(",")]

            tarea = {
                "id": partes[0],
                "duracion": int(partes[1]),
                "categoria": partes[2]
            }

            tareas.append(tarea)

    return tareas

def leer_recursos(nombre_archivo) -> list[dict[str, object]]:
    recursos = []
    ruta = Path(__file__).resolve().parent / nombre_archivo

    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()

            if linea == "":
                continue

            partes = [p.strip() for p in linea.split(",")]

            recurso = {
                "id": partes[0],
                "categorias": partes[1:],
                "tiempo_libre": 0
            }

            recursos.append(recurso)

    return recursos
def crear_mapa_categorias(recursos):
    mapa = {}

    for recurso in recursos:
        for categoria in recurso["categorias"]:
            if categoria not in mapa:
                mapa[categoria] = []

            mapa[categoria].append(recurso)

    return mapa
def copiar_tareas(tareas):
    copia = []

    for t in tareas:
        nueva_tarea = {
            "id": t["id"],
            "duracion": t["duracion"],
            "categoria": t["categoria"]
        }
        copia.append(nueva_tarea)

    return copia

def copiar_recursos(recursos):
    copia = []

    for r in recursos:
        nuevo_recurso = {
            "id": r["id"],
            "categorias": r["categorias"][:],
            "tiempo_libre": 0
        }
        copia.append(nuevo_recurso)

    return copia

def cantidad_compatibles(tarea, recursos):
    contador = 0

    for r in recursos:
        if tarea["categoria"] in r["categorias"]:
            contador += 1

    return contador

def elegir_recurso(tarea, mapa_categorias):
    compatibles = mapa_categorias.get(tarea["categoria"], [])

    if len(compatibles) == 0:
        return None

    mejor_recurso = compatibles[0]

    for r in compatibles:
        if r["tiempo_libre"] < mejor_recurso["tiempo_libre"]:
            mejor_recurso = r

    return mejor_recurso

def asignar_tareas(tareas, recursos, mapa_categorias):
    asignaciones = []

    for tarea in tareas:
        recurso_elegido = elegir_recurso(tarea, mapa_categorias)

        if recurso_elegido is None:
            continue

        tiempo_inicio = recurso_elegido["tiempo_libre"]
        tiempo_fin = tiempo_inicio + tarea["duracion"]

        asignacion = {
            "id_tarea": tarea["id"],
            "id_recurso": recurso_elegido["id"],
            "tiempo_inicio": tiempo_inicio,
            "tiempo_fin": tiempo_fin
        }

        asignaciones.append(asignacion)

        recurso_elegido["tiempo_libre"] = tiempo_fin

    return asignaciones

def obtener_duracion(tarea):
    return tarea["duracion"]

def ordenar_tareas_segun_criterio(tareas, recursos, criterio):
    if criterio == "larga_primero":
        tareas.sort(key=obtener_duracion, reverse=True)

    return tareas

def calcular_makespan(recursos):
    makespan = 0

    for r in recursos:
        if r["tiempo_libre"] > makespan:
            makespan = r["tiempo_libre"]

    return makespan

def escribir_output(nombre_archivo, asignaciones):
    ruta = Path(__file__).resolve().parent / nombre_archivo

    with open(ruta, "w", encoding="utf-8") as archivo:
        for asignacion in asignaciones:
            linea = (
                f"{asignacion['id_tarea']},"
                f"{asignacion['id_recurso']},"
                f"{asignacion['tiempo_inicio']},"
                f"{asignacion['tiempo_fin']}\n"
            )
            archivo.write(linea)

def buscar_mejor_solucion(tareas_originales, recursos_originales):
    tareas = copiar_tareas(tareas_originales)
    recursos = copiar_recursos(recursos_originales)

    tareas = ordenar_tareas_segun_criterio(tareas, recursos, "larga_primero")
    mapa_categorias = crear_mapa_categorias(recursos)

    asignaciones = asignar_tareas(tareas, recursos, mapa_categorias)
    makespan = calcular_makespan(recursos)

    return asignaciones, makespan

tareas_originales = leer_tareas("tareas.txt")
recursos_originales = leer_recursos("recursos.txt")

mejor_asignacion, mejor_makespan = buscar_mejor_solucion(
    tareas_originales,
    recursos_originales
)

escribir_output("output.txt", mejor_asignacion)
print("Makespan:", mejor_makespan)

