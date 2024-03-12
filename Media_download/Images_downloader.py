# Para descargar imagen
import requests
from requests.exceptions import HTTPError
from PIL import Image
from io import BytesIO
import time

# Manejar descargas
import os
from datetime import datetime
import sys


# API KEY
from Logic.Tools import params


import threading
import time

# Para manejar APIS
from pyunsplash import PyUnsplash
import pixabay.core

from Logic.Tools.Shuffle_pics import ordenar_por_aspecto



"""
Script para descargar imágenes a partir de un query:
    - Uso por ahora: imágenes de animales
"""


def Images_Pexels_download_manager(query, carpeta_raw_data, k, formato):

    """
    Función para descargar imagenes a partir de un Keyword:
    - Usandos las APIS de Pexels, Unsplash, Pixaby
    """
    segundos_linux = datetime.now().strftime("%s")
    nombre_carpeta = f"Fotos_{query}_{segundos_linux}"
    carpeta_descargas = os.path.join(carpeta_raw_data, nombre_carpeta)
    os.makedirs(carpeta_descargas, exist_ok=True)

    carpeta_descargas_bonus = os.path.join(carpeta_descargas, "extra")
    os.makedirs(carpeta_descargas_bonus, exist_ok=True)

    try:
        thread_Pexels = threading.Thread(target=download_from_Pexels, args=(query, carpeta_descargas, k, formato))
        thread_Pexels.start()
    except Exception as e:
        print(f"Error al descargar {e}")

    try:
        thread_Unsplash = threading.Thread(target=download_from_Unsplash, args=(query, carpeta_descargas_bonus, k, formato))
        thread_Unsplash.start()
    except Exception as e:
        print(f"Error al descargar {e}")

    try:
        thread_Pixaby = threading.Thread(target=download_from_Pixaby, args=(query, carpeta_descargas_bonus, k, formato))
        thread_Pixaby.start()
    except Exception as e:
        print(f"Error al descargar {e}")

    try:
        thread_Pexels.join()
    except Exception as e:
        print(f"Error al descargar {e}")

    try:
        thread_Unsplash.join()
    except Exception as e:
        print(f"Error al descargar {e}")

    try:
        thread_Pixaby.join()
    except Exception as e:
        print(f"Error al descargar {e}")

    ordenar_por_aspecto(carpeta_descargas_bonus)




def descargar_imagen(url, ruta_completa):

    """
    Función para descargar una imagen desde un URL específico y guardarla en una carpeta dada.
    Asume la existencia de una función 'descargar' que maneja la descarga de la imagen.
    """


    try:
        image_response = requests.get(url)
        image_response.raise_for_status()  # Esto lanzará un error si el estado no es 200

        image_data = BytesIO(image_response.content)
        image = Image.open(image_data)
        image.save(ruta_completa)

    except HTTPError as e:
        if e.response.status_code == 404: # Verifica si el código de estado es 404, y si es así, no detener el script
            print(f"⚠️ Advertencia: No se encontró la imagen (Error 404).")
        else: # Para otros errores HTTP, detiene la ejecución del script
            print(f"❌ Error HTTP al descargar la imagen: {e}")
            return "para"

    except Exception as e: # Otros errores (e.g., problemas al abrir la imagen, errores al guardar la imagen)
        print(f"❌ No se pudo descargar la imagen. Error: {e}")




def download_from_Pexels(query, carpeta_descargas, k, formato):

    """
    Función para descargar imágenes a través de la API de Pexels
    """

    num_results = 80 # máximo
    api_key = params.Pexels_key
    headers = {"Authorization": api_key} # Headers para que funciona requets (usamos API key)
    segundos_linux = datetime.now().strftime("%s")  # segundero para evitar sobre escribir carpeta
    
    dict_orientacion = {
        "Vertical" : "portrait",
        "Horizontal" : "landscape"
    }
    orientacion = dict_orientacion[formato]  # definir horientación según lo elegido del usuario

    for j in range(k):
        url = f"https://api.pexels.com/v1/search?query={query}&page={j+1}&per_page={num_results}"
        r = requests.get(url, headers=headers)
        response = r.json()
        lista_fotos = response["photos"]

        i = 1
        for foto in lista_fotos:

            source = foto["src"]
            link_vertical = source[orientacion]

            nombre_archivo = f"Photo_{query}_aPexels_{j}_{i}_{segundos_linux}.jpg"
            ruta_completa = os.path.join(carpeta_descargas, nombre_archivo)

            para = descargar_imagen(link_vertical, ruta_completa)
            if para:
                break
            i += 1
            time.sleep(3)

    sys.exit("Pexels acabó")



def download_from_Unsplash(query, carpeta_descargas, k, formato):

    """
    Función para descargar imágenes a través de la API de UNsplash
    """

    pu = PyUnsplash(api_key=params.Unsplash_key)  # instantiate PyUnsplash object
    segundos_linux = datetime.now().strftime("%s")  # segundero para evitar sobre escribir carpeta

    dict_orientacion = {
        "Vertical" : "portrait",
        "Horizontal" : "landscape"
    }
    orientacion = dict_orientacion[formato]  # definir horientación según lo elegido del usuario

    for j in range(k + 1):

        photos = pu.photos(type_='random', count=30, featured=True, query=query, orientation = orientacion)
        list_photos = photos.body

        i = 1
        for photo in list_photos:

            urls = photo["urls"]
            high_quality_link = urls["full"]
            nombre_archivo = f"Photo_{query}_Unsplash_{j}_{i}_{segundos_linux}.jpg"
            ruta_completa = os.path.join(carpeta_descargas, nombre_archivo)

            para = descargar_imagen(high_quality_link, ruta_completa)
            if para:
                break
            i += 1
            time.sleep(3)





def download_from_Pixaby(query, carpeta_descargas, k, formato):

    """
    Función para descargar imágenes a través de la API de Pixaby
    """
    px = pixabay.core(params.Pixaby_key)
    segundos_linux = datetime.now().strftime("%s")
    
    dict_orientacion = {
        "Vertical" : "vertical",
        "Horizontal" : "horizontal"
    }
    orientacion = dict_orientacion[formato]  # definir horientación según lo elegido del usuario

    pictures = px.query(
        query = query,
        orientation = orientacion,
        category = ["animals", "nature"]
        )

    num_of_pics = (k + 1) * 30
    i = 1
    for picture in pictures:
        
        if i >= num_of_pics:
            break

        nombre_archivo = f"Photo_{query}_Pixaby_{i}_{segundos_linux}.jpg"
        ruta_completa = os.path.join(carpeta_descargas, nombre_archivo)
        
        try:
            picture.download(ruta_completa, "largeImage")  # picture[0].download("space.jpg", "largeImage")
        except Exception as e:
            print(e)

        i +=1
        time.sleep(3)
