import speech_recognition as sr  # Importar la librería de reconocimiento de voz
import unicodedata  # Importar módulo para normalizar texto

# Función para eliminar acentos y normalizar texto
def eliminar_acentos(texto):
    return ''.join(
        (c for c in unicodedata.normalize('NFD', texto)
         if unicodedata.category(c) != 'Mn')
    )

# Frase esperada
textoanterior = "Buenos días Claro que si antes de mostrarle las diferentes opciones que tenemos una pregunta el colchón es para usted"  # Definir la frase que se espera escuchar

# Crear un objeto Recognizer
recognizer = sr.Recognizer()  # Crear una instancia del reconocedor de voz

# Utilizar el micrófono como fuente de entrada
with sr.Microphone() as source:  # Utilizar el micrófono como la fuente de audio
    print("Cliente: Buenos días, estoy buscando un colchón")  # Imprimir el texto del cliente para contexto
    print("Amigo vendedor, di la siguiente frase para atender a tu cliente: Buenos días Claro que sí antes de mostrarle las diferentes opciones que tenemos una pregunta el colchón es para usted")  # Pedir al vendedor que diga la frase esperada
    recognizer.adjust_for_ambient_noise(source)  # Ajustar el reconocedor para el ruido ambiental
    audio = recognizer.listen(source)  # Escuchar y grabar el audio del micrófono

    try:
        # Utilizar el motor de reconocimiento de voz de Google
        text = recognizer.recognize_google(audio, language="es-ES")  # Reconocer el audio usando Google y especificar el idioma español
        print("Texto reconocido: " + text)  # Imprimir el texto reconocido

        # Normalizar ambos textos para comparar
        textoanterior_normalizado = eliminar_acentos(textoanterior.strip().lower())
        text_normalizado = eliminar_acentos(text.strip().lower())

        # Debugging outputs
        print(f"Texto esperado (normalizado): {repr(textoanterior_normalizado)}")  # Imprimir representación exacta
        print(f"Texto reconocido (normalizado): {repr(text_normalizado)}")  # Imprimir representación exacta
        print(f"Longitud texto esperado: {len(textoanterior_normalizado)}")  # Imprimir longitud
        print(f"Longitud texto reconocido: {len(text_normalizado)}")  # Imprimir longitud

        if text_normalizado == textoanterior_normalizado:  # Comparar el texto reconocido con el texto esperado
            print("Correcto")  # Imprimir "Correcto" si coinciden
        else:
            print("Incorrecto")  # Imprimir "Incorrecto" si no coinciden

    except sr.UnknownValueError:  # Si no se puede reconocer el audio
        print("No se pudo reconocer el audio.")  # Indicar que no se pudo reconocer el audio
    except sr.RequestError as e:  # Si hay un error en la solicitud al motor de reconocimiento de voz
        print("Error en la solicitud al motor de reconocimiento de voz; {0}".format(e))  # Indicar el error ocurrido
