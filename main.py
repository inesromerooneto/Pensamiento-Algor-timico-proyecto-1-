from pathlib import Path


def leer_tareas(nombre_archivo) -> list[dict[str, object]]:
    tareas : list[dict[str, object]] = []
    ruta = Path(__file__).resolve().parent / nombre_archivo

    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()  # sacar saltos de línea

            if linea == "":
                continue  # saltar líneas vacías

            partes = [p.strip() for p in linea.split(",")]  # dividir por comas y quitar espacios

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
                "categorias": partes[1:],  # todas las partes después del ID son categorías 
                "tiempo_libre": 0
            }

            recursos.append(recurso)

    return recursos

tareas = leer_tareas("tareas.txt")
recursos = leer_recursos("recursos.txt")



#Revisar compatibilidad entre recursos y tareas

def compatibilidad_recursos(tarea, recursos):
    lista = []
    for r in recursos:
        if tarea["categoria"] in r["categorias"]:
            lista.append(r["id"])
    return lista


#Siguiente paarte: por tarea, ver recursos compatibles, elegir uno, asignarlo, actualizar (exclusividaad)
#Porque si un recurso ya tiene una tarea asignada, no puede hacer otra al mismo tiempo

def elegir_recurso(tarea, recursos):
    compatibles = []

    for r in recursos:
        if tarea["categoria"] in r["categorias"]:
            compatibles.append(r)

    if len(compatibles) == 0:
        return None

    mejor = compatibles[0]

    for r in compatibles:
        if r["tiempo_libre"] < mejor["tiempo_libre"]:
            mejor = r

    return mejor

def asignar_tareas(tareas, recursos):
    asignaciones = []

    for tarea in tareas:
        recurso_elegido = elegir_recurso(tarea, recursos)

        if recurso_elegido == None:
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
tareas.sort(key=obtener_duracion, reverse=True)



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


asignaciones = asignar_tareas(tareas, recursos)
escribir_output("output.txt", asignaciones)
makespan = calcular_makespan(recursos)
print("Makespan:", makespan)