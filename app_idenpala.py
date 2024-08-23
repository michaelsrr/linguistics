from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import unicodedata
import os
import pyaudio
import wave

app = Flask(__name__)

# Configuración de la ruta para FFmpeg
os.environ['PATH'] += os.pathsep + r'C:\ffmpeg\ffmpeg-n7.0-latest-win64-gpl-7.0\bin'

# Función para eliminar acentos y normalizar texto
def eliminar_acentos(texto):
    return ''.join(
        (c for c in unicodedata.normalize('NFD', texto)
         if unicodedata.category(c) != 'Mn')
    )

# Frase esperada
textoanterior = "Buenos días Claro que sí antes de mostrarle las diferentes opciones que tenemos una pregunta el colchón es para usted"

recognizer = sr.Recognizer()

@app.route('/')
def index():
    return render_template('index.html', texto=textoanterior)

@app.route('/grabar', methods=['POST'])
def grabar():
    # Guardar el archivo de audio
    archivo_audio = 'grabacion.wav'
    if os.path.exists(archivo_audio):
        os.remove(archivo_audio)

    # Configuración de la grabación
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 10

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(archivo_audio, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    return jsonify({"status": "grabacion_completada"})

@app.route('/transcribir', methods=['POST'])
def transcribir():
    archivo_audio = 'grabacion.wav'
    
    if not os.path.exists(archivo_audio):
        return jsonify({"status": "error", "message": "No se encontró el archivo de audio."})

    with sr.AudioFile(archivo_audio) as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio, language="es-ES")
        textoanterior_normalizado = eliminar_acentos(textoanterior.strip().lower())
        text_normalizado = eliminar_acentos(text.strip().lower())

        if text_normalizado == textoanterior_normalizado:
            resultado = "Correcto"
        else:
            resultado = "Incorrecto"
        
        return jsonify({"status": "success", "texto_reconocido": text, "resultado": resultado})
    
    except sr.UnknownValueError:
        return jsonify({"status": "error", "message": "No se pudo reconocer el audio."})
    except sr.RequestError as e:
        return jsonify({"status": "error", "message": f"Error en la solicitud al motor de reconocimiento de voz; {e}"})

if __name__ == '__main__':
    app.run(debug=True)