import os
import random
import datetime
import re
from PIL import Image
import shutil


"""
Script de funciones que se usan en el resto de códigos
    OJO! En el script normal las funciones no se llaman desde aquí 
        si no desde el package "SocialMedia"
"""

def convertir_ruta_windows_a_wsl(ruta_windows):

    """
    Función para pegar la ruta de una carpeta del explorador de archivos Windwos y devolver ruta linux
    En caso de ser ruta linux no se cambia
    """

    patron = r'^\\\\wsl\$\\Ubuntu(.+)$'
    coincidencia = re.match(patron, ruta_windows)
    if coincidencia:
        ruta_linux = coincidencia.group(1).replace('\\', '/')
        return ruta_linux
    else:
        return ruta_windows



def ordenar_por_aspecto(ruta_carpeta):

    """
    Función para:
    - ordenar las imagenes de más vertical a más horizontal
    - guardar una copia según su clasificacion de vertical y horizontal
    """

    carpeta = convertir_ruta_windows_a_wsl(ruta_carpeta)
    fecha_nueva = datetime.datetime.now().strftime("%Y-%m-%d-%s")

    imagenes = []
    for archivo in os.listdir(carpeta):
        ruta_archivo = os.path.join(carpeta, archivo)
        try:
            with Image.open(ruta_archivo) as img:
                ancho, alto = img.size
                aspect_ratio = alto / ancho
                imagenes.append((archivo, ruta_archivo, aspect_ratio))
        except IOError:
            pass

    imagenes.sort(key=lambda x: x[2], reverse=True)

    for i, (nombre_archivo, ruta_archivo, _) in enumerate(imagenes):
        prefijo = "HD_" if nombre_archivo.startswith("HD_") else ""
        nuevo_nombre = f"{prefijo}{fecha_nueva}_{i*4+15}.jpg"
        os.rename(ruta_archivo, os.path.join(carpeta, nuevo_nombre))

    print("\n✅ Ordenamiento por aspecto hecho\n")

    clasificar_imagenes(carpeta)



def clasificar_imagenes(ruta_carpeta):

    """
    Funcion para guardar imagenes en carpetas según si son verticales u horizonales
    Si son cuadradas se guardan en ambas
    """

    carpeta = convertir_ruta_windows_a_wsl(ruta_carpeta)  # Convertir la ruta
    carpeta_horizontales = os.path.join(carpeta, "horizontales")
    carpeta_verticales = os.path.join(carpeta, "verticales")

    # Crear subcarpetas si no existen
    os.makedirs(carpeta_horizontales, exist_ok=True)
    os.makedirs(carpeta_verticales, exist_ok=True)

    for archivo in os.listdir(carpeta):
        ruta_archivo = os.path.join(carpeta, archivo)
        try:
            with Image.open(ruta_archivo) as img:
                ancho, alto = img.size
                # Verificar si es horizontal, vertical o cuadrada
                if ancho > alto:
                    shutil.copy(ruta_archivo, carpeta_horizontales)
                elif alto > ancho:
                    shutil.copy(ruta_archivo, carpeta_verticales)
                else: # Es cuadrada
                    shutil.copy(ruta_archivo, carpeta_horizontales)
                    shutil.copy(ruta_archivo, carpeta_verticales)
        except IOError:
            pass