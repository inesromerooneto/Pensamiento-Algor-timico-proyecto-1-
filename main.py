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


def compatibilidad_recursos(tarea, recursos):
    lista = []

    for r in recursos:
        if tarea["categoria"] in r["categorias"]:
            lista.append(r["id"])

    return lista


def cantidad_compatibles(tarea, recursos):
    contador = 0

    for r in recursos:
        if tarea["categoria"] in r["categorias"]:
            contador += 1

    return contador


def elegir_recurso(tarea, recursos, desempate_random=False):
    compatibles = []

    for r in recursos:
        if tarea["categoria"] in r["categorias"]:
            compatibles.append(r)

    if len(compatibles) == 0:
        return None

    mejor_tiempo = compatibles[0]["tiempo_libre"]

    for r in compatibles:
        if r["tiempo_libre"] < mejor_tiempo:
            mejor_tiempo = r["tiempo_libre"]

    mejores = []

    for r in compatibles:
        if r["tiempo_libre"] == mejor_tiempo:
            mejores.append(r)

    if desempate_random and len(mejores) > 1:
        return random.choice(mejores)

    return mejores[0]


def asignar_tareas(tareas, recursos, desempate_random=False):
    asignaciones = []

    for tarea in tareas:
        recurso_elegido = elegir_recurso(tarea, recursos, desempate_random)

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

    elif criterio == "corta_primero":
        tareas.sort(key=obtener_duracion)

    elif criterio == "restrictiva_primero":
        tareas.sort(key=lambda t: (cantidad_compatibles(t, recursos), -t["duracion"]))

    elif criterio == "mixta":
        tareas.sort(key=lambda t: (-t["duracion"], cantidad_compatibles(t, recursos)))

    elif criterio == "aleatoria":
        random.shuffle(tareas)

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


def buscar_mejor_solucion(tareas_originales, recursos_originales, tiempo_limite=8):
    mejor_asignaciones = []
    mejor_makespan = None

    criterios = [
        "larga_primero",
        "corta_primero",
        "restrictiva_primero",
        "mixta",
        "aleatoria"
    ]

    inicio = time.time()
    intento = 0

    while time.time() - inicio < tiempo_limite:
        random.seed(intento)

        tareas = copiar_tareas(tareas_originales)
        recursos = copiar_recursos(recursos_originales)

        criterio = criterios[intento % len(criterios)]
        tareas = ordenar_tareas_segun_criterio(tareas, recursos, criterio)

        if criterio == "aleatoria" or criterio == "mixta":
            desempate_random = True
        else:
            desempate_random = False

        asignaciones = asignar_tareas(tareas, recursos, desempate_random)
        makespan = calcular_makespan(recursos)

        if mejor_makespan is None or makespan < mejor_makespan:
            mejor_makespan = makespan
            mejor_asignaciones = asignaciones

        intento += 1

    return mejor_asignaciones, mejor_makespan


tareas_originales = leer_tareas("tareas_EP.txt")
recursos_originales = leer_recursos("recursos_EP.txt")

mejor_asignacion, mejor_makespan = buscar_mejor_solucion(
    tareas_originales,
    recursos_originales,
    tiempo_limite=0.5
)

escribir_output("output.txt", mejor_asignacion)
print("Makespan:", mejor_makespan)

def main():
    tareas_originales = leer_tareas("tareas_1000.txt")
    recursos_originales = leer_recursos("recursos_500.txt")

    mejor_asignacion, mejor_makespan = buscar_mejor_solucion(
        tareas_originales,
        recursos_originales,
        tiempo_limite=0.5
    )

    escribir_output("output.txt", mejor_asignacion)
    print("Makespan:", mejor_makespan)
