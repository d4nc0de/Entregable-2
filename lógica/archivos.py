# funciones para leer los archivos

def leer_correlaciones(ruta):
    with open(ruta, 'r') as archivo:
        lineas = archivo.readlines()
        n = int(lineas[0].strip())
        correlaciones = {}

        for linea in lineas[1:]:
            accion1, accion2, valor = linea.strip().split()
            correlaciones[(accion1, accion2)] = float(valor)
            correlaciones[(accion2, accion1)] = float(valor)
    
    return n, correlaciones

def leer_rendimientos(ruta):
    with open(ruta, 'r') as archivo:
        rendimientos = {}

    for linea in archivo:
        accion, rendimiento, riesgo = linea.strip().split()
        rendimientos[accion] = (float(rendimiento), int(riesgo))

    return rendimientos