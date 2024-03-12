import os
from Media_download.Images_downloader import Images_Pexels_download_manager
from datetime import datetime
import media_to_download


diccionario = media_to_download.downloads_dictionnary
formato = media_to_download.formato_elegido



def menu_descarga():
    print("📥 ¿Qué te gustaría descargar?")
    print("1️⃣ Imágenes")
    print("2️⃣ Videos (Función no disponible aún)")
    
    eleccion = input("Introduce 1 para imágenes o 2 para videos: ")
    
    if eleccion == '1':
        Photos_downloader()
    elif eleccion == '2':
        print("🚧 Lo sentimos, la descarga de videos aún no está disponible.")
        menu_descarga()
    else:
        print("❌ Opción no válida. Por favor, elige 1 o 2.")
        menu_descarga()





def Photos_downloader():

    """
    Función para descargar fotos de cada elemento que hay en el diccionario y guardarlas en la carpeta con ese nombre
    """

    # Crear carpeta raw_data si no existe
    os.makedirs("raw_data", exist_ok=True)
    carpeta_raw_data = os.path.join(os.getcwd(), "raw_data")


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



if __name__ == "__main__":
    menu_descarga()
