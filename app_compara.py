from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import os
import wave
import pyaudio
import time

app = Flask(__name__)

# Frase original
texto_original = "Hola Marina qué gafas tan bonitas"

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html', frase=texto_original)

# Ruta para iniciar la grabación
@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recording
    recording = True
    global frames
    frames = []
    
    def record_audio():
        global frames
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        try:
            while recording:
                data = stream.read(1024)
                frames.append(data)
        except IOError:
            pass
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

    # Start recording in a new thread
    import threading
    threading.Thread(target=record_audio).start()
    
    return jsonify({'status': 'recording_started'})

# Ruta para detener la grabación y procesar el audio
@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global recording
    recording = False
    
    # Save the recorded audio to a file
    audio_file = "audio.wav"
    p = pyaudio.PyAudio()
    with wave.open(audio_file, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        texto_reconocido = recognizer.recognize_google(audio, language="es-ES")
        palabras_originales = texto_original.lower().split()
        palabras_reconocidas = texto_reconocido.lower().split()
        palabras_coincidentes = set(palabras_originales) & set(palabras_reconocidas)
        porcentaje_asertividad = len(palabras_coincidentes) / len(palabras_originales) * 100
        return jsonify({'texto_reconocido': texto_reconocido, 'porcentaje_asertividad': f"{porcentaje_asertividad:.2f}%"})
    except sr.UnknownValueError:
        return jsonify({'error': 'No se pudo reconocer el audio.'})
    except sr.RequestError as e:
        return jsonify({'error': f'Error en la solicitud al motor de reconocimiento de voz; {e}'})

if __name__ == '__main__':
    app.run(debug=True)
