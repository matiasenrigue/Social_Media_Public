import os
from Media_download.Images_downloader import Images_Pexels_download_manager
from Media_download.Video_downloader import Videos_Pexels_download_manager

from datetime import datetime
import media_to_download


diccionario = media_to_download.downloads_dictionnary
formato = media_to_download.formato_elegido



def menu_descarga():
    print("\n📥 ¿Qué te gustaría descargar?")
    print("\n1️⃣ Imágenes")
    print("2️⃣ Videos (Función no disponible aún\n")
    
    eleccion = input("Introduce 1 para imágenes o 2 para videos: ")
    
    if eleccion == '1':
        Photos_downloader()
    elif eleccion == '2':
        Videos_downloader()
    else:
        print("❌ Opción no válida. Por favor, elige 1 o 2.")
        menu_descarga()





def Photos_downloader():

    """
    Función para descargar fotos de cada elemento que hay en el diccionario y guardarlas en la carpeta con ese nombre
    """
    carpeta_raw_data = os.path.join(os.getcwd(), "raw_data_Photos")
    os.makedirs(carpeta_raw_data, exist_ok=True)

    print("descargas por hacer")
    for elemento in diccionario:
        query = elemento
        k = diccionario[elemento]
        print(f"{query} : {k}")


    for elemento in diccionario:
        query = elemento
        k = diccionario[elemento]

        hora = datetime.now().strftime("%H-%M-%S")
        print(f"\nIniciando descarga para {query} a las {hora} -- Nivel: {k}\n")
        Images_Pexels_download_manager(query, carpeta_raw_data, k, formato)




def Videos_downloader():

    """
    Función para descargar fotos de cada elemento que hay en el diccionario y guardarlas en la carpeta con ese nombre
    """

    carpeta_raw_data = os.path.join(os.getcwd(), "raw_data_Videos")
    os.makedirs(carpeta_raw_data, exist_ok=True)

    print("descargas por hacer")
    for elemento in diccionario:
        query = elemento
        k = diccionario[elemento]
        print(f"{query} : {k}")


    for elemento in diccionario:
        query = elemento
        k = diccionario[elemento]

        hora = datetime.now().strftime("%H-%M-%S")
        print(f"\nIniciando descarga para {query} a las {hora} -- Nivel: {k}\n")
        Videos_Pexels_download_manager(query, carpeta_raw_data, k, formato)




if __name__ == "__main__":
    menu_descarga()
