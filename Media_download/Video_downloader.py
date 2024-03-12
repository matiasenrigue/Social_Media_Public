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
import threading
import time

# API KEY
from Logic.Tools import params

# Para manejar APIS
from pyunsplash import PyUnsplash
import pixabay.core



"""
Script para descargar imágenes a partir de un query:
    - Uso por ahora: imágenes de animales
"""


def Videos_Pexels_download_manager(query, carpeta_raw_data, k, formato):

    """
    Función para descargar imagenes a partir de un Keyword:
    - Usandos las APIS de Pexels, Unsplash, Pixaby
    """
    segundos_linux = datetime.now().strftime("%s")
    nombre_carpeta = f"Videos_{query}_{segundos_linux}"
    carpeta_descargas = os.path.join(carpeta_raw_data, nombre_carpeta)
    os.makedirs(carpeta_descargas, exist_ok=True)

    carpeta_descargas_bonus = os.path.join(carpeta_descargas, "extra")
    os.makedirs(carpeta_descargas_bonus, exist_ok=True)

    try:
        thread_Pexels = threading.Thread(target=download_from_Pexels, args=(query, carpeta_descargas, k, formato))
        thread_Pexels.start()
    except Exception as e:
        print(f"Error al descargar {e}")

    # try:
    #     thread_Unsplash = threading.Thread(target=download_from_Unsplash, args=(query, carpeta_descargas_bonus, k, formato))
    #     thread_Unsplash.start()
    # except Exception as e:
    #     print(f"Error al descargar {e}")

    try:
        thread_Pixaby = threading.Thread(target=download_from_Pixaby, args=(query, carpeta_descargas_bonus, k, formato))
        thread_Pixaby.start()
    except Exception as e:
        print(f"Error al descargar {e}")

    try:
        thread_Pexels.join()
    except Exception as e:
        print(f"Error al descargar {e}")

    # try:
    #     thread_Unsplash.join()
    # except Exception as e:
    #     print(f"Error al descargar {e}")

    try:
        thread_Pixaby.join()
    except Exception as e:
        print(f"Error al descargar {e}")



def descargar_video(url, ruta_completa):
    """
    Función para descargar un video desde un URL específico y guardarlo en una carpeta dada.
    Asume la existencia de una función 'descargar' que maneja la descarga del video.
    """

    try:
        video_response = requests.get(url, stream=True)
        video_response.raise_for_status()  # Esto lanzará un error si el estado no es 200

        with open(ruta_completa, 'wb') as f:
            for chunk in video_response.iter_content(chunk_size=8192): 
                f.write(chunk)

    except HTTPError as e:
        if e.response.status_code == 404:  # Verifica si el código de estado es 404, y si es así, no detener el script
            print(f"⚠️ Advertencia: No se encontró el video (Error 404).")
        else:  # Para otros errores HTTP, detiene la ejecución del script
            print(f"❌ Error HTTP al descargar el video: {e}")
            return "para"

    except Exception as e:  # Otros errores (e.g., problemas al abrir el video, errores al guardar el video)
        print(f"❌ No se pudo descargar el video. Error: {e}")




def download_from_Pexels(query, carpeta_descargas, k, formato):

    """
    Función para descargar imágenes a través de la API de Pexels
    """

    num_results = 80 # máximo
    api_key = params.Pexels_key
    headers = {"Authorization": api_key} # Headers para que funciona requets (usamos API key)
    segundos_linux = datetime.now().strftime("%s")  # segundero para evitar sobre escribir carpeta

    for j in range(k):
        url = f"https://api.pexels.com/videos/search?query={query}&page={j+1}&per_page={num_results}"
        r = requests.get(url, headers=headers)
        response = r.json()
        lista_videos = response["videos"]
    
        hd_videos = []
        for video in lista_videos:
            for file in video["video_files"]:
                if file["quality"] == "hd":
                    hd_videos.append(file["link"])
                    break  # Añade el video una vez y continúa con el siguiente video

        i = 1
        for url_video in hd_videos:
            
            nombre_archivo = f"Video_{query}_aPexels_{j}_{i}_{segundos_linux}.mp4"
            ruta_completa = os.path.join(carpeta_descargas, nombre_archivo)

            para = descargar_video(url_video, ruta_completa)
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

    for j in range(k + 1):

        photos = pu.photos(type_='random', count=30, featured=True, query=query)
        list_photos = photos.body

        i = 1
        for photo in list_photos:

            urls = photo["urls"]
            high_quality_link = urls["full"]
            nombre_archivo = f"Photo_{query}_Unsplash_{j}_{i}_{segundos_linux}.mp4"
            ruta_completa = os.path.join(carpeta_descargas, nombre_archivo)

            para = descargar_video(high_quality_link, ruta_completa)
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

    videos = px.queryVideo(query = query)
    num_of_vids = (k + 1) * 30
    
    i = 1
    for video in videos:
        
        if i >= num_of_vids:
            break

        nombre_archivo = f"Video_{query}_Pixaby_{i}_{segundos_linux}.mp4"
        ruta_completa = os.path.join(carpeta_descargas, nombre_archivo)
        
        try:
            video.download(ruta_completa, "large")  # video[0].download("space.mp4", "largeImage")
        except Exception as e:
            print(e)

        i +=1
        time.sleep(3)
