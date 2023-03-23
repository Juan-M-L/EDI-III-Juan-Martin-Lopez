import pandas as pd

mensaje = "Vehículo no encontrado."


class Administrador:
    def __init__(self, nro_id: int, nombre: str, clave: str) -> None:
        self._nro_id = nro_id
        self._nombre = nombre
        self._clave = clave

    @property
    def get_id(self) -> int:
        return self._nro_id

    @property
    def get_nombre(self) -> str:
        return self._nombre

    @property
    def get_clave(self) -> str:
        return self._clave


def buscar_por_id(valor_id: int, df_archivo: pd.DataFrame) -> pd.DataFrame:
    return df_archivo[df_archivo["Id"] == valor_id]


# Elimina un vehiculo del dataframe
def eliminar_vehiculo(df_archivo, id_vehiculo) -> pd.DataFrame:
    end_loop = False
    while not end_loop:
        vehiculo_seleccionado = df_archivo[df_archivo["Id"] == id_vehiculo]
        confirmacion = input(f"{vehiculo_seleccionado}\n¿Confirmar? S/N ")
        # Eliminar vehiculo.
        if confirmacion.lower() == "s":
            df_archivo = df_archivo[df_archivo["Id"] != id_vehiculo]
            print("Vehículo eliminado.")
            return df_archivo
        elif confirmacion.lower() == "n":
            end_loop = True
        else:
            break

# Añade un vehículo nuevo al dataframe y lo guarda en el archivo .csv con un ID generado.


def agregar_vehiculo_df(archivo: pd.DataFrame, tipo: str, marca: str, modelo: str, kilometraje: float, precio: float):

    vehiculo_id = archivo["Id"].max() + 1

    archivo.loc[vehiculo_id] = {
         "Id": vehiculo_id,
         "Tipo": tipo,
         "Marca": marca,
         "Modelo": modelo,
         "Kilometraje": kilometraje,
         "Precio": precio
    }
    return archivo


def solicitar_id_vehiculo(archivo):
    while True:
        try:
            id_seleccionado = int(input("Ingrese el id del vehiculo: "))
            break
        except ValueError:
            continue
    if archivo[archivo["Id"] == id_seleccionado].empty:
        return mensaje
    return id_seleccionado


def solicitar_datos_vehiculo(objetivo_solicitud):
    header_dict = {
        'Tipo': [],
        'Marca': [],
        'Modelo': [],
        'Kilometraje': [],
        'Precio': []
    }
    headers = []
    for header in objetivo_solicitud:
        headers.append(header)

    for header in header_dict:
        while True:
            eleccion = input(f"Ingrese el/la {header} del vehículo: ")
            if eleccion == "":
                continue
            if isinstance(header_dict[header], str):
                eleccion = eleccion.title()
            elif isinstance(header_dict[header], int):
                eleccion = int(eleccion)
            elif isinstance(header_dict[header], float):
                eleccion = float(eleccion)
            header_dict[header] = eleccion
            break
        continue

    while True:
        print("Se ingresarán estos datos. Compruebe que sean correctos:")
        for i in header_dict.items():
            print(f"{i[1]}")
        decision = input("Para realizar un cambio, ingresa \"r\". Para continuar, presiona Enter ")

        if decision.lower() == "r":
            for i in header_dict.items():
                print(f"{i[0]}. {i[1]}")

            while True:
                try:
                    seleccion = input("¿Qué desea cambiar? ingrese el filtro (Tipo, Marca; Modelo...) que corresponda a la elección: ")
                    seleccion = seleccion.title()
                    if seleccion in header_dict:
                        pass
                    else:
                        continue
                except ValueError:
                    continue

                modificacion = (input("Ingrese el nuevo contenido: "))
                print(modificacion)

                print(header_dict[seleccion])
                header_dict[seleccion] = modificacion
                break
        elif decision == "":
            return header_dict
        else:
            continue


LISTA_ADMINISTRADORES = [
                            Administrador(1, "pedro", "1234"),
                            Administrador(2, "alvaro", "asdf")
                        ]
