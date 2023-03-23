from pandas import Series
mensaje_error_01 = "Error: La función no reconoce el valor ingresado como una Series."

menu_de_filtros = []  # Los módulos de Python son singleton por naturaleza. Solo existirá una instancia de esta variable


def crear_filtro(series):
    try:
        lista_opciones = series.drop_duplicates()
        return lista_opciones
    except AttributeError:
        raise Exception(mensaje_error_01)


def cargar_filtros(*series):
    for i in series:
        menu_de_filtros.append(i)
