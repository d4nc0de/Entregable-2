
from itertools import combinations

class Accion:
    def __init__(self, nom, rendimiento, riesgo):
        self.nombre = nom
        self.rendimiento_anual = float(rendimiento)
        self.factor_riesgo = int(riesgo)

    def __repr__(self):
        return f"Accion: {self.nombre}. Rendimiento: {self.rendimiento_anual}. Riesgo: {self.factor_riesgo}"

with open("docs/rendimientos.txt") as rend:
    acciones = []
    for linea in rend:
        nombre, rendimiento, riesgo = linea.split()
        acciones.append(Accion(nombre, rendimiento, riesgo))

with open("docs/correlaciones.txt") as corr:
    correlaciones = {}
    n = int(corr.readline())
    for linea in corr:
        accion1, accion2, valor = linea.split()
        correlaciones[(accion1, accion2)] = float(valor)

def cumple_correlacion(portafolio, max_corr):
    for a1, a2 in combinations(portafolio, 2):
        a = correlaciones.get((a1.nombre, a2.nombre), 0) or correlaciones.get((a2.nombre, a1.nombre), 0)
        if a is None or a > max_corr:
            return False
    return True

def maximo_beneficio(corr_max, n):
    portafolios_posibles = []
    rendimiento_max = 0
    mejor_portafolio = None

    for rango in range(n, len(acciones) + 1):
        for portafolio in combinations(acciones, rango):
            if cumple_correlacion(portafolio, corr_max):
                if rendimiento_promedio(portafolio) > rendimiento_max:
                    rendimiento_max = rendimiento_promedio(portafolio)
                    mejor_portafolio = portafolio
                portafolios_posibles.append(portafolio)

    return mejor_portafolio, rendimiento_max, len(portafolios_posibles)

def verificar_correlacion_max_y_riesgo_controlado(portafolio, corr_max, riesgo_max):
    if not cumple_correlacion(portafolio, corr_max):
        return False
    return riesgo_promedio(portafolio) <= riesgo_max


def riesgo_controlado(corr_max, n, riesgo):
    portafolios_posibles = []
    rendimiento_max = 0
    riesgo_max = 0
    mejor_portafolio = None

    for rango in range(n, len(acciones) + 1):
        for portafolio in combinations(acciones, rango):
            if verificar_correlacion_max_y_riesgo_controlado(portafolio, corr_max, riesgo):
                if rendimiento_promedio(portafolio) > rendimiento_max:
                    rendimiento_max = rendimiento_promedio(portafolio) #Rendimiento mayor, se reemplaza
                    riesgo_max = riesgo_promedio(portafolio) #Riesgo mayor, se reemplaza
                    mejor_portafolio = portafolio
                portafolios_posibles.append(portafolio)

    return mejor_portafolio, rendimiento_max, riesgo_max, len(portafolios_posibles)

def rendimiento_promedio(portafolio):
    return sum(accion.rendimiento_anual for accion in portafolio) / len(portafolio)

def riesgo_promedio(portafolio):
    return sum(accion.factor_riesgo for accion in portafolio) / len(portafolio)


x = 0
while x != 3:
    print("\nSISTEMA GESTIÓN DE PORTAFOLIOS DE INVERSIÓN\n")
    print("1. Portafolio de máximo beneficio")
    print("2. Portafolio con riesgo controlado")
    print("3. Terminar")

    try:
        x = int(input("\nIngrese la opción que desea ejecutar (1-3): "))
    except ValueError:
        print("Entrada inválida. Por favor, ingrese un número entre 1 y 3.")
        continue

    if x == 1:
        print("\nPORTAFOLIO DE MÁXIMO BENEFICIO\n")
        corr_max = float(input("Ingrese la correlación máxima permitida: "))
        n_min = int(input("Ingrese el número mínimo de acciones en el portafolio: "))
        mejor_portafolio, rendimiento_max, total_validos = maximo_beneficio(corr_max, n_min)


        if mejor_portafolio is None:
            print("\nNO SE ENCONTRÓ PORTAFOLIO\n")
        else:
            print("\nLas acciones del portafolio con rendimiento promedio máximo son:")
            for accion in mejor_portafolio:
                print(f"- {accion.nombre} (Rendimiento: {accion.rendimiento_anual}. Riesgo: {accion.factor_riesgo})")

            print(f"\nSu rendimiento promedio es: {round(rendimiento_max, 3)} ({round(rendimiento_max, 3)*100}%)")
            print(f"\nNúmero total de portafolios posibles válidos: {total_validos}")

    elif x == 2:
        print("\nPORTAFOLIO CON RIESGO CONTROLADO\n")
        corr_max = float(input("Ingrese la correlación máxima permitida: "))
        n_min = int(input("Ingrese el número mínimo de acciones en el portafolio: "))
        riesgo_max = float(input("Ingrese el riesgo promedio máximo permitido: "))
        mejor_portafolio, rendimiento_max, riesgo_max, total_validos = riesgo_controlado(corr_max, n_min, riesgo_max)

        
        if mejor_portafolio is None:
            print("\nNO SE ENCONTRÓ PORTAFOLIO\n")
        else:
            print("\nLas acciones del portafolio con rendimiento promedio máximo son:")
            for accion in mejor_portafolio:
                print(f"- {accion.nombre} (Rendimiento: {accion.rendimiento_anual}. Riesgo: {accion.factor_riesgo})")

            print(f"\nRendimiento promedio del portafolio: {round(rendimiento_max, 3)} ({round(rendimiento_max * 100, 2)}%)")
            print(f"Riesgo promedio del portafolio: {round(riesgo_max, 2)}")
            print(f"Número total de portafolios válidos: {total_validos}")

    elif x == 3:
        print("¡Adiós!")
    else:
        print("⚠️ Opción inválida. Por favor, ingrese un número entre 1 y 3.")