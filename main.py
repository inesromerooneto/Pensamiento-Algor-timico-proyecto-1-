from pathlib import Path

def leer_tareas(nombre_archivo):
    tareas = []
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
            
def leer_recursos(nombre_archivo):
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
                "categorias": partes [1:]  # todas las partes después del ID son categorías 
            }

            recursos.append(recurso)

    return recursos

tareas = leer_tareas("tareas.txt")
recursos = leer_recursos("recursos.txt")

print("Tareas:", tareas)
print("Recursos:", recursos)

#Revisar compatibilidad entre recursos y tareas

def compatibilidad_recursos(tarea, recursos):
    lista = []
    for r in recursos:
        if tarea["categoria"] in r["categorias"]:
            lista.append(r["id"])
    return lista

for tarea in tareas: 
    comp = compatibilidad_recursos(tarea, recursos)
    print("Tarea", tarea["id"], "->", comp)