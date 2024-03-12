from moviepy.editor import VideoFileClip
import os



def Video_cutting(ruta_carpeta_videos, ruta_carpeta_destino):
    
    duracion_fragmento = 4.5

    if not os.path.exists(ruta_carpeta_destino):
        os.makedirs(ruta_carpeta_destino)

    # Lista todos los archivos en la carpeta de videos
    archivos = os.listdir(ruta_carpeta_videos)

    # Filtra solo los archivos de video (puedes ajustar las extensiones según tus necesidades)
    videos = [archivo for archivo in archivos if archivo.endswith(('.mp4', '.mov', '.avi'))]

    # Procesa cada video
    for video in videos:
        ruta_completa = os.path.join(ruta_carpeta_videos, video)
        clip = VideoFileClip(ruta_completa)
        
        # Calcula cuántos fragmentos se generarán
        num_fragmentos = int(clip.duration) // duracion_fragmento
        
        # Divide el video en fragmentos y los guarda
        for i in range(num_fragmentos):
            inicio = i * duracion_fragmento
            fin = inicio + duracion_fragmento
            fragmento = clip.subclip(inicio, fin)
            
            # Define el nombre del archivo de salida
            nombre_salida = f'{video}_fragmento_{i+1}.mp4'
            ruta_salida = os.path.join(ruta_carpeta_destino, nombre_salida)
            
            # Escribe el fragmento a un archivo
            fragmento.write_videofile(ruta_salida, codec='libx264', audio_codec='aac')
            
        # Libera los recursos del clip
        clip.close()
        


def procesar_carpetas_RAW_DATA():

    ruta_carpeta_raiz = os.path.join(os.getcwd, 'raw_data_Videos')
    carpetas = [os.path.join(ruta_carpeta_raiz, nombre) for nombre in os.listdir(ruta_carpeta_raiz) if os.path.isdir(os.path.join(ruta_carpeta_raiz, nombre))]
    
    for carpeta in carpetas:
        nombre_carpeta = os.path.basename(carpeta) # pillar el final de la ruta (el nombre)
        ruta_carpeta_destino = os.path.join(os.getcwd, 'VIDEOS_processed_data', nombre_carpeta)
        
        carpeta_2 = os.path.join(carpeta, "extra")
        
        # Llama a tu función original para procesar los videos
        Video_cutting(carpeta, ruta_carpeta_destino)
        Video_cutting(carpeta_2, ruta_carpeta_destino)
        
  
    




if __name__ == "__main__":
    
    procesar_carpetas_RAW_DATA()
    
