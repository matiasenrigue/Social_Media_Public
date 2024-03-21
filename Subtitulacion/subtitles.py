import whisper_timestamped
import json
import string
import os
import glob


def tiempo_a_formato_srt(tiempo):
    
    """
    Convertir salida subs a formato SRT de subtitulos
    """
    
    horas, resto = divmod(tiempo, 3600)
    minutos, segundos = divmod(resto, 60)
    milisegundos = int((segundos - int(segundos)) * 1000)
    segundos = int(segundos)
    return f"{int(horas):02}:{int(minutos):02}:{segundos:02},{milisegundos:03}"




def get_subtitles(audio_path, archivo_subs):

    """
    Función para obtener los subitutlos a partir de un audios:
    - Usamos el audio sin musica pero ya editado (velocidad, silencios, etc) para que tiempos cuadren con audio final con musica
    - Se hace gracias al modelo de OpenAI que corre LOCALMENTE
    """

    print("\n🔄 Generando Subtítulos...\n")

    # Conseguir subtitulos
    model = whisper_timestamped.load_model("base")
    results = whisper_timestamped.transcribe(model, audio_path)

    def aplanar_transcripcion_y_generar_srt(results, archivo_srt):
        with open(archivo_srt, 'w', encoding='utf-8') as f:
            contador = 1
            for segment in results["segments"]:
                for palabra in segment["words"]:
                    inicio = tiempo_a_formato_srt(palabra["start"])
                    fin = tiempo_a_formato_srt(palabra["end"])
                    texto = palabra["text"]

                    f.write(f'{contador}\n')
                    f.write(f'{inicio} --> {fin}\n')
                    f.write(f'{texto}\n\n')
                    
                    contador += 1

    aplanar_transcripcion_y_generar_srt(results, archivo_subs)

    print("\n📄 Subtítulos creados")


def audios_subtitulation():
    
    """
    Función para conseguir Subs para todos los archivos guardados en la carpeta "audios_to_sub"
    """
    
    folder = os.path.join(os.getcwd(),"audios_to_sub")
    audio_files = glob.glob(os.path.join(folder, '*.mp3'))
    
    if audio_files:
        for audio_path in audio_files:
            archivo_subs_cola = os.path.splitext(os.path.basename(audio_path))[0]
            archivo_subs = os.path.join(folder, f"{archivo_subs_cola}.srt")
            get_subtitles(audio_path, archivo_subs)
    
    else:
        print("\nNo se encontraron archivos de audio .mp3 en la carpeta 'audios_to_sub'")





    





def corregir_subtitulos(industrial = ""):
    """
    Función que indica qué palabras del archivo de subtítulos no coinciden con el script original y viceversa.
    - Habrá que corregirlas manualmente pues ningún código lo hace bien.
    - Usuario debe modificar archivo JSON en carpeta de video y cambiar las palabras que toquen.
    """
    from Logic.Uploads.telegram_mensajes import send_telegram

    def contar_palabras(lista_palabras):
        contador = {}
        for palabra in lista_palabras:
            if palabra in contador:
                contador[palabra] += 1
            else:
                contador[palabra] = 1
        return contador

    def limpiar_texto(texto):
        caracteres_a_eliminar = string.punctuation + "¡"  # Definir los caracteres especiales a eliminar
        texto_limpio = texto.translate(str.maketrans('', '', caracteres_a_eliminar)).lower()  # Eliminar caracteres especiales y convertir a minúsculas
        return texto_limpio.split()

    print("\n🔄 Verificando subtítulos...\n")

    with open("guion.txt", "r", encoding="utf-8") as file:
        texto_original = file.read()

    with open('transcripcion_aplanada.json', 'r', encoding='utf-8') as f:
        subtitulos_generados = json.load(f)

    palabras_originales = limpiar_texto(texto_original)
    contador_original = contar_palabras(palabras_originales)
    contador_subtitulos = {}

    for subt in subtitulos_generados:
        palabras_subt = limpiar_texto(subt['text'])
        for palabra in palabras_subt:
            if palabra in contador_subtitulos:
                contador_subtitulos[palabra] += 1
            else:
                contador_subtitulos[palabra] = 1

    palabras_faltantes_en_subtitulos = {}
    palabras_extras_en_subtitulos = {}

    for palabra, frecuencia in contador_original.items():
        if palabra not in contador_subtitulos:
            palabras_faltantes_en_subtitulos[palabra] = frecuencia

    for palabra, frecuencia in contador_subtitulos.items():
        if palabra not in contador_original:
            palabras_extras_en_subtitulos[palabra] = frecuencia

    Mensaje = "Correciones de subtitulos:\n"

    print("\n⚠️ Palabras a añadir:\nPalabras presentes en el guion y faltantes en los subtítulos: palabra : frecuencia")
    Mensaje += "\n\n⚠️ Palabras a añadir:\nPalabras presentes en el guion y faltantes en los subtítulos: palabra : frecuencia\n"
    for palabra, frecuencia in palabras_faltantes_en_subtitulos.items():
        print(f"{palabra}: {frecuencia}")
        Mensaje += f"\n{palabra}: {frecuencia}"

    print("\n⚠️ Palabras a cambiar:\nPalabras presentes en los subtítulos y faltantes en el guion: palabra : frecuencia")
    Mensaje += "\n\n\n⚠️ Palabras a cambiar:\nPalabras presentes en los subtítulos y faltantes en el guion: palabra : frecuencia\n"
    for palabra, frecuencia in palabras_extras_en_subtitulos.items():
        print(f"{palabra}: {frecuencia}")
        Mensaje += f"\n{palabra}: {frecuencia}"

    print("\n\n⚠️ Cambia el archivo json para corregir los subtitulos")
    print("⚠️ Usa Ctrl + F para buscar las palabras a cambiar\n\n\n\n")


    with open('correciones_subs.txt', 'w', encoding='utf-8') as correciones_file:
        correciones_file.write(Mensaje)

    if industrial:
        pass
    else:
        send_telegram(Mensaje)
        
        
        




"""
    OLD CODE !!


def get_subtitlesJSON(audio_path, archivo_subs):

    ""
    Función para obtener los subitutlos a partir de un audios:
    - Usamos el audio sin musica pero ya editado (velocidad, silencios, etc) para que tiempos cuadren con audio final con musica
    - Se hace gracias al modelo de OpenAI que corre LOCALMENTE
    ""

    print("\n🔄 Generando Subtítulos...\n")

    # Función para aplanar la estructura de los resultados
    def aplanar_transcripcion(results):
        palabras_transcripcion = []
        for segment in results["segments"]:
            palabras_transcripcion.extend(segment["words"])
        return palabras_transcripcion

    # Conseguir subtitulos
    model = whisper_timestamped.load_model("base")
    results = whisper_timestamped.transcribe(model, audio_path)

    # Aplana la transcripción
    transcripcion_aplanada = aplanar_transcripcion(results)

    with open(f'{archivo_subs}.json', 'w', encoding='utf-8') as f:
        json.dump(transcripcion_aplanada, f, ensure_ascii=False, indent=4)

    print("\n📄 Subtítulos creados")
"""