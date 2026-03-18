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

tareas = leer_tareas("tareas.txt")
recursos = leer_recursos("recursos.txt")

print("Tareas:", tareas)
print("Recursos:", recursos)