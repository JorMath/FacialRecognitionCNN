from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import os
import cv2
import numpy as np
import tempfile

# Token de tu bot, obtenido al crear un nuevo bot en BotFather en Telegram
TOKEN = "6665053780:AAHtUOI-uzjamAK3jP2-a7gr15bA-tBzDTg"

# Función que maneja el comando /start
def start(update: Update, context: CallbackContext) -> None:
    """Inicia el bot"""
    update.message.reply_text('¡Bienvenido a nuestro proyecto, somos SecureHome, más protección para tu familia, más tranquilidad para ti!')

# Función que maneja el comando /info
def info(update: Update, context: CallbackContext) -> None:
    """Proporciona información sobre SecureHome"""
    message = (
        "SecureHome es un aplicativo que nos permitirá aumentar la seguridad de nuestro hogar mediante el reconocimiento facial a través de una cámara ubicada en la entrada principal. Tendrá integraciones con Alexa y Telegram, para gestionar de una manera más eficaz y al mismo tiempo tener la información a mano."
    )
    update.message.reply_text(message)

# Función que maneja el comando /acerca
def acerca(update: Update, context: CallbackContext) -> None:
    """Información sobre los autores del proyecto"""
    message = (
        "Proyecto creado para la seguridad del hogar\n"
        "Autores:\n"
        "- Jorman Chuquer\n"
        "- Brandon Jaya\n"
        "- Alexander Morales\n"
        "- Mateo Pilco"
    )
    update.message.reply_text(message)

# Función que maneja el comando /historial
def historial(update: Update, context: CallbackContext) -> None:
    """Envía el archivo historial.txt al usuario"""
    # Ruta del archivo historial.txt
    file_path = "C:/Users/jorma/Downloads/probando_face_recognition/probando_face_recognition/registros.txt"
    # Verificar si el archivo existe
    if os.path.exists(file_path):
        # Enviar el archivo al usuario
        with open(file_path, 'rb') as file:
            update.message.reply_document(file)
    else:
        update.message.reply_text("Lo siento, no se encontró el archivo de historial.")

# Función que maneja el comando /actual
def actual(update: Update, context: CallbackContext) -> None:
    """Toma una foto con la webcam y la envía"""
    # Iniciar la cámara
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        # Guardar la imagen temporalmente
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image_path = temp_file.name
        cv2.imwrite(image_path, frame)

        # Enviar la imagen al usuario
        update.message.reply_photo(open(image_path, 'rb'))
    else:
        update.message.reply_text("Lo siento, no se pudo capturar la imagen.")

# Función que maneja comandos desconocidos
def unknown(update: Update, context: CallbackContext) -> None:
    """Maneja comandos desconocidos"""
    update.message.reply_text("Comando desconocido. Utiliza /lista para ver la lista de comandos disponibles.")

# Función que maneja el comando /lista
def lista(update: Update, context: CallbackContext) -> None:
    """Muestra la lista de comandos disponibles con descripciones"""
    command_list = []
    for handler in context.dispatcher.handlers:
        if isinstance(handler, CommandHandler):
            command = handler.callback.__name__
            docstring = handler.callback.__doc__
            command_list.append(f"{command}: {docstring}")

    update.message.reply_text("Lista de comandos disponibles:\n" + "\n".join(command_list))

# Función principal
def main() -> None:
    # Crear el Updater y pasarle el token
    updater = Updater(TOKEN)

    # Obtener el dispatcher para registrar los manejadores
    dp = updater.dispatcher

    # Registrar los manejadores
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("acerca", acerca))
    dp.add_handler(CommandHandler("historial", historial))
    dp.add_handler(CommandHandler("actual", actual))
    dp.add_handler(CommandHandler("lista", lista))

    # Manejar comandos desconocidos
    dp.add_handler(MessageHandler(Filters.command, unknown))

    # Iniciar el bot
    updater.start_polling()

    # Mantener el programa en ejecución
    updater.idle()

# Ejecutar el programa principal
if __name__ == '__main__':
    main()
