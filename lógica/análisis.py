from itertools import combinations

# generar potafolios válidos

def generar_portafolios_validos(acciones, min_acciones, max_corr, rendimientos, correlaciones, max_riesgo=None):
    portafolios_validos = []

    for i in range(min_acciones, len(acciones)+1):
        for combo in combinations(acciones, i):
            if not cumple_correlacion(combo, correlaciones, max_corr):
                continue
            if max_riesgo is not None and riesgo_promedio(combo, rendimientos) > max_riesgo:
                continue
            portafolios_validos.append(combo)

        return portafolios_validos

# selecionar mejor portafolio

def mejor_portafolio(portafolios, rendimientos):
    mejor = None
    mejor_rendimiento = -float('inf')

    for p in portafolios:
        r = rendimiento_promedio(p, rendimientos)
        if r > mejor_rendimiento:
            mejor_rendimiento = r
            mejor = p

    return mejor, mejor_rendimiento

# validar si un portafolio cumple la correlación máxima

def cumple_correlacion(portafolio, correlaciones, max_correlacion):
    from itertools import combinations
    for a1, a2 in combinations(portafolio, 2):
        if correlaciones.get((a1, a2), 0) > max_correlacion:
            return False
    return True

# calcular riesgo y rendimiento promedio

def rendimiento_promedio(portafolio, rendimientos):
    return sum(rendimientos[accion][0] for accion in portafolio) / len(portafolio)

def riesgo_promedio(portafolio, rendimientos):
    return sum(rendimientos[accion][1] for accion in portafolio) / len(portafolio)