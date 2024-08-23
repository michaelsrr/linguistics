def comparar_respuesta(respuesta_usuario, frase_correcta):
    respuesta_usuario = respuesta_usuario.lower()
    frase_correcta = frase_correcta.lower()

    if respuesta_usuario == frase_correcta:
        return True
    else:
        return False

frase_esperada = "muy bien, gracias"

print("Frase: Hola, cómo estás?")

respuesta_usuario = input("Tu respuesta: ")

if comparar_respuesta(respuesta_usuario, frase_esperada):
    print("¡Correcto! La respuesta es válida.")
else:
    print("Incorrecto. La respuesta no coincide con la frase esperada.")
    