
# Importar librerías y módulos.
import pandas as pd
from pandas import Series
from funcionalidad_filtro import crear_filtro, cargar_filtros
from funciones_usuario import (
    solicitar_elecciones,
    listar_vehiculos,
    hasta_precio_bajo,
    hasta_precio_normal,
    hasta_precio_alto,
    mayor_a_precio_alto
)
from funciones_administrador import (
    solicitar_datos_vehiculo,
    solicitar_id_vehiculo,
    buscar_por_id,
    eliminar_vehiculo,
    agregar_vehiculo_df,
    LISTA_ADMINISTRADORES,
    mensaje
)

# Definir el nombre del archivo .csv que se usará.
NOMBRE_ARCHIVO = "registro_vehiculo.csv"
# Cargar los datos del archivo en un DataFrame de la librería "pandas".
df_archivo = pd.read_csv(NOMBRE_ARCHIVO)

# Crear un objeto Series para cada columna del DataFrame.
vehiculo_id = Series(df_archivo.Id)
vehiculo_tipo = Series(df_archivo.Tipo)
vehiculo_marca = Series(df_archivo.Marca)
vehiculo_modelo = Series(df_archivo.Modelo)
vehiculo_kilometraje = Series(df_archivo.Kilometraje)
vehiculo_precio = Series(df_archivo.Precio)

# Crear un filtro para cada columna del DataFrame. Son necesarios para la interfaz.
filtro_id = crear_filtro(df_archivo.Id)
filtro_tipo = crear_filtro(df_archivo.Tipo)
filtro_marca = crear_filtro(df_archivo.Marca)
filtro_modelo = crear_filtro(df_archivo.Modelo)
filtro_kilometraje = Series(name="Kilometraje", data=["Nuevo", "Usado"])
filtro_precio = Series(
    name="Precio",
    data=[
        hasta_precio_bajo,
        hasta_precio_normal,
        hasta_precio_alto,
        mayor_a_precio_alto
    ]
)

# Cargar los filtros en el menu_de_filtros para su uso en la interfaz.
cargar_filtros(
    filtro_tipo,
    filtro_marca,
    filtro_modelo,
    filtro_kilometraje,
    filtro_precio
)

# While loop principal. Inicio de la interfaz de usuario.
loop_end = False
while not loop_end:

    # Menú principal.
    opcion_elegida = input("""
Menú principal.
1) Buscar vehículos
2) Acceso de administrador
3) Salir
""")

    if opcion_elegida == "1":
        elecciones_usuario = solicitar_elecciones(df_archivo)

        print(listar_vehiculos(elecciones_usuario, df_archivo))

        input("\nPresione Enter para seguir")

    elif opcion_elegida == "2":
        while True:
            credenciales_correctas = False
            print("Ingrese nombre de usuario. Para salir, presione Enter sin rellenar nada.")
            print(f"(Usuarios: \"{LISTA_ADMINISTRADORES[0].get_nombre}\", \"{LISTA_ADMINISTRADORES[1].get_nombre}\")")
            usuario = input()

            if usuario == "":
                break
            clave = input("Ingrese contraseña. Para salir, presione Enter sin rellenar nada.\n")

            if clave == "":
                break

            for admin in LISTA_ADMINISTRADORES:
                admin_nombre = admin.get_nombre
                admin_clave = admin.get_clave

                # Si las credenciales son correctas.
                if usuario == admin_nombre and clave == admin_clave:
                    credenciales_correctas = True

            if credenciales_correctas:
                while True:

                    # Menú de administrador.
                    opcion_elegida_administrador = input("""
Menú de Administrador.
¿Qué desea hacer?
1) Buscar un vehículo.
2) Agregar un vehículo.
3) Eliminar un vehículo.
4) Cerrar sesión.
""")

                    # Opción 1.
                    if opcion_elegida_administrador == "1":
                        while True:
                            # Menú de busqueda.
                            opcion_buscar_vehiculo = input("""
1) Buscar por id.
2) Buscar por categorias.
3) Atrás.
""")
                            # Opción 1.1
                            if opcion_buscar_vehiculo == "1":
                                valor_id = solicitar_id_vehiculo(df_archivo)

                                if valor_id == mensaje:
                                    print(mensaje)

                                else:
                                    print(buscar_por_id(valor_id, df_archivo))

                            # Opción 1.2
                            elif opcion_buscar_vehiculo == "2":
                                elecciones_usuario = solicitar_elecciones(df_archivo)

    #                               print(elecciones_usuario)

                                print(listar_vehiculos(elecciones_usuario, df_archivo))

                                input("Presione Enter para seguir")

                            # Opción 1.3
                            elif opcion_buscar_vehiculo == "3":
                                break

                            else:
                                continue
                            continue

                    # Opción 2.
                    elif opcion_elegida_administrador == "2":
                        datos = solicitar_datos_vehiculo(df_archivo)
                        agregar_vehiculo_df(df_archivo,
                                            datos['Tipo'],
                                            datos['Marca'],
                                            datos['Modelo'],
                                            datos['Kilometraje'],
                                            datos['Precio']
                                            )
                        cambio = df_archivo.to_csv(NOMBRE_ARCHIVO, index=False, mode="w")
                        print("Vehículo añadido.")

                    # Opción 3.
                    elif opcion_elegida_administrador == "3":
                        id_seleccionado = solicitar_id_vehiculo(df_archivo)

                        if id_seleccionado == mensaje:
                            print(mensaje)

                        else:
                            df_archivo = eliminar_vehiculo(df_archivo, id_seleccionado)

                            if df_archivo is None:
                                # Vuelve a leer el csv para que df_archivo no se quede en None, luego regresa a opciones
                                df_archivo = pd.read_csv(NOMBRE_ARCHIVO)

                            else:
                                cambio = df_archivo.to_csv(NOMBRE_ARCHIVO, index=False, mode="w")

                    # Opción 4.
                    elif opcion_elegida_administrador == "4":
                        break

                    else:
                        continue

            # Si el nombre de usuario o la contraseña son incorrectos.
            else:
                print("Nombre de usuario o contraseña incorrectos")
                continue
            pass

    # Si se eligió la opción de salir del sistema.
    elif opcion_elegida == "3":
        loop_end = True

    else:
        continue
