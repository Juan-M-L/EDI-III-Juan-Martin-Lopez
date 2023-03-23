import pandas as pd

from funcionalidad_filtro import menu_de_filtros

precio_bajo = 200000.00
precio_normal = 500000.00
precio_alto = 1000000.00

hasta_precio_bajo = f"Hasta ${precio_bajo}"
hasta_precio_normal = f"Hasta ${precio_normal}"
hasta_precio_alto = f"Hasta ${precio_alto}"
mayor_a_precio_alto = f"Mayor a ${precio_alto}"


kilometraje_nuevo = 0
kilometraje_usado = 300000


# Funciones pequeñas que se usarán dentro de las funciones mayores.


# Saca las opciones de la variable series. Hecha para usar con Series procesadas.
def get_opciones(series: pd.Series) -> list:
    lista = []
    for opcion in series:
        lista.append(opcion)
    return lista


# Muestra una lista numerada de las opciones dentro de una series tipo filtro.
def mostrar_opciones(filtro) -> None:
    indice_filtro = 0
    for opcion in filtro:
        indice_filtro += 1
        linea_de_texto = f"{indice_filtro}) {opcion}"

        print(linea_de_texto)

# Fin de las funciones pequeñas.


# Funciones mayores que ofrecen las funcionalidades clave del programa.
def solicitar_elecciones(df_archivo) -> list:
    filtros_elegidos = []  # Variable que almacena los filtros elegidos en una lista.
    filtro_objetivo = 0  # Variable int hecha para manipular filtros.
    filtros_restantes = len(df_archivo.columns) - 1  # Variable int que muestra los filtros que faltan completar.

    numero_retrocesos = 0
    retrocediendo = numero_retrocesos > 0

    while filtros_restantes != 0:
        # Se redefine filtro_actual para que cambie al siguiente filtro.
        filtro_actual = menu_de_filtros[filtro_objetivo]

        mensaje_parte_1 = "Ingrese el número correspondiente al filtro que desee. Si desea retroceder, ingrese \"r\"."
        mensaje_parte_2 = f"Filtro: {filtro_actual.name} de vehículo.\nSi desea dejar el filtro libre, sólo presiona Enter."

        print(mensaje_parte_1)
        mostrar_opciones(filtro_actual)
        print(mensaje_parte_2)
        opcion_seleccionada = input()

        if bool(opcion_seleccionada):  # Si opcion_seleccionada tiene un valor.
            # Esta parte investiga si apretaste "R" o "r" para saber si tiene que ir un filtro_actual hacia atrás.
            if opcion_seleccionada in ("R", "r") and filtro_objetivo > 0:
                filtro_objetivo -= 1
                filtros_restantes += 1

                numero_retrocesos += 1
                print(numero_retrocesos)
                retrocediendo = numero_retrocesos > 0  # Se actualiza el valor.
                continue
            elif opcion_seleccionada in ("R", "r"):
                continue

            try:  # Verifica si se ingresó un int y le resta 1 para que el valor mínimo sea 0 y no se salga del índice.
                opcion_seleccionada_int = int(opcion_seleccionada) - 1
            except ValueError:
                continue

            opciones_filtro_actual = get_opciones(filtro_actual)
            #
            if 0 <= opcion_seleccionada_int < len(opciones_filtro_actual):  # Se verifica que lo ingresado sea válido.

                eleccion = get_opciones(filtro_actual)[opcion_seleccionada_int]
                # Estas líneas hacen que el programa elimine la vieja elección para reemplazarla con la nueva.
                if retrocediendo:
                    filtros_elegidos[filtro_objetivo] = eleccion

                    numero_retrocesos -= 1
                    retrocediendo = numero_retrocesos > 0  # Se actualiza el valor.
                elif not retrocediendo:
                    filtros_elegidos.append(eleccion)

                filtro_objetivo += 1
                filtros_restantes -= 1

                continue
            else:
                continue

        else:  # Si opcion_seleccionada está vacía (El usuario no ingresa nada) Se añade None (Null) a filtros_elegidos.
            if retrocediendo:
                filtros_elegidos[filtro_objetivo] = None

                numero_retrocesos -= 1
                retrocediendo = numero_retrocesos > 0  # Se actualiza el valor.
            elif not retrocediendo:
                filtros_elegidos.append(None)

            filtro_objetivo += 1
            filtros_restantes -= 1
            continue

    return filtros_elegidos


def listar_vehiculos(elecciones_usuario, archivo) -> pd.DataFrame:
    while True:
        print("Estas son sus elecciones:")
        for i in elecciones_usuario:
            if i is None:
                continue
            print(i)

        resultado = archivo

        decision_usuario = input("¿Desea agregar o cambiar algo? Si es así, ingrese \"r\". Si no, presione Enter.\n")
        if decision_usuario in ("R", "r"):
            # Mostrarle los filtros que puede cambiar.
            cont = 0
            header_id = True
            for header in archivo:
                if header_id:
                    header_id = False
                    continue
                cont += 1
                print(f"{cont}: {header}")

            filtro_elegido = "_"
            while True:
                try:
                    filtro_elegido = int(input("¿Qué filtro desea cambiar?\n")) - 1
                    if 0 <= filtro_elegido < len(elecciones_usuario):
                        break
                    else:
                        continue
                except ValueError:
                    continue

            # Mostrar los cambios posibles.
            nueva_eleccion = 0
            while True:
                print("Elija el nuevo filtro presionando el número correspondiente.")
                mostrar_opciones(menu_de_filtros[filtro_elegido])
                try:
                    nueva_eleccion = int(input())
                    if 0 < nueva_eleccion <= len(elecciones_usuario):
                        break
                    else:
                        continue
                except ValueError:
                    continue

            # Aplicar el cambio seleccionado.
            cont = 0
            for i in menu_de_filtros[filtro_elegido]:
                cont += 1
                if cont == nueva_eleccion:
                    elecciones_usuario[filtro_elegido] = i
                    break
            continue

        # Realizar la búsqueda.
        elif decision_usuario == "":
            indice_filtro = 0
            header_id = True

            for row in resultado:
                if header_id:
                    header_id = False
                    continue

                eleccion_usuario = elecciones_usuario[indice_filtro]
                if eleccion_usuario is None:
                    indice_filtro += 1
                    continue

                # Si eleccion_usuario es Kilometraje.
                if eleccion_usuario.__contains__("Nuevo"):
                    nuevo = resultado[row] == 0

                    resultado = resultado[nuevo]
                    indice_filtro += 1
                    continue

                elif eleccion_usuario.__contains__("Usado"):
                    usado = resultado[row] > 0
                    resultado = resultado[usado]
                    indice_filtro += 1
                    continue

                # Si eleccion_usuario es Precio.
                if eleccion_usuario.__contains__("Hasta"):
                    if eleccion_usuario.__contains__(hasta_precio_bajo):
                        resultado = resultado[resultado[row] <= precio_bajo]
                    elif eleccion_usuario.__contains__(hasta_precio_normal):
                        resultado = resultado[resultado[row] <= precio_normal]
                    elif eleccion_usuario.__contains__(hasta_precio_alto):
                        resultado = resultado[resultado[row] <= precio_alto]
                    indice_filtro += 1
                    continue
                if eleccion_usuario.__contains__(mayor_a_precio_alto):
                    resultado = resultado[resultado[row] >= precio_alto]
                    indice_filtro += 1
                    continue

                # Si eleccion_usuario no es ninguno de los anteriores.
                resultado = resultado[resultado[row] == eleccion_usuario]
                indice_filtro += 1

        else:  # Este else sirve en caso de que el usuario ingrese cualquier caracter que no active funciones.
            continue
        if resultado.empty:
            return "No se encontraron resultados."

        # Si el DataFrame "resultado" no está vacío, imprime un mensaje con la cantidad de filas y el resultado.
        print(f"Se han encontrado {resultado.shape[0]} resultados basados en tus filtros elegidos.")
        return resultado.to_string(index=False)
# Fin de las funciones mayores.
