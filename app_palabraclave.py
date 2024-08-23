from flask import Flask, render_template, request, jsonify
import speech_recognition as sr  # Importar la librería de reconocimiento de voz

app = Flask(__name__)

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')  # Renderiza una plantilla HTML

# Ruta para manejar la grabación de audio y el reconocimiento de voz
@app.route('/recognize', methods=['POST'])
def recognize():
    # Frase original y palabra clave
    texto_original = "yo soy muy alto"  # Definir la frase original
    palabra_clave = "alto"  # Definir la palabra clave que se espera reconocer

    # Crear un objeto Recognizer
    recognizer = sr.Recognizer()  # Crear una instancia del reconocedor de voz

    try:
        # Utilizar el micrófono como fuente de entrada
        with sr.Microphone() as source:  # Utilizar el micrófono como la fuente de audio
            recognizer.adjust_for_ambient_noise(source)  # Ajustar el reconocedor para el ruido ambiental
            print(f"Di la siguiente frase: '{texto_original}'")  # Indicar al usuario que debe decir la frase original
            audio = recognizer.listen(source)  # Escuchar y grabar el audio del micrófono

        # Utilizar el motor de reconocimiento de voz de Google
        texto_reconocido = recognizer.recognize_google(audio, language="es-ES")  # Reconocer el audio usando Google y especificar el idioma español
        print("Texto reconocido: " + texto_reconocido)  # Imprimir el texto reconocido

        # Dividir la frase en palabras clave o tokens
        palabras_originales = texto_original.lower().split()  # Convertir la frase original a minúsculas y dividirla en palabras
        palabras_reconocidas = texto_reconocido.lower().split()  # Convertir el texto reconocido a minúsculas y dividirlo en palabras

        # Verificar si la palabra clave está en las palabras reconocidas
        palabra_clave_encontrada = palabra_clave in palabras_reconocidas  # Comprobar si la palabra clave está en las palabras reconocidas

        if palabra_clave_encontrada:  # Si se encuentra la palabra clave
            # Calcular el número de palabras coincidentes
            palabras_coincidentes = set(palabras_originales) & set(palabras_reconocidas)  # Calcular las palabras coincidentes entre el texto original y el reconocido
            porcentaje_asertividad = len(palabras_coincidentes) / len(palabras_originales) * 100  # Calcular el porcentaje de palabras coincidentes
        else:
            porcentaje_asertividad = 0  # Si no se encuentra la palabra clave, el porcentaje de asertividad es 0

        print("Porcentaje de asertividad: {:.2f}%".format(porcentaje_asertividad))  # Imprimir el porcentaje de asertividad

        if palabra_clave_encontrada and porcentaje_asertividad > 0:  # Si se encuentra la palabra clave y el porcentaje de asertividad es mayor a 0
            mensaje = "La frase es aceptable ya que contiene la palabra clave."
        else:
            mensaje = "La frase es inaceptable, la palabra clave no fue reconocida."

        return jsonify({"mensaje": mensaje, "texto_reconocido": texto_reconocido, "porcentaje_asertividad": porcentaje_asertividad})  # Devolver los resultados como JSON

    except sr.UnknownValueError:  # Si no se puede reconocer el audio
        return jsonify({"mensaje": "No se pudo reconocer el audio."})
    except sr.RequestError as e:  # Si hay un error en la solicitud al motor de reconocimiento de voz
        return jsonify({"mensaje": "Error en la solicitud al motor de reconocimiento de voz; {0}".format(e)})

if __name__ == '__main__':
    app.run(debug=True)