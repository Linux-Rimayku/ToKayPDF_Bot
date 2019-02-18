
import telebot
import threading
from telebot import types
from time import sleep
from foto import guardar
from foto import crear_archivo
from pdf import verificar
from pdf import crear_todo_pdf
from secrets import token_urlsafe
from random import randrange
from foto import cantidad_archivos, eliminar_archiv_imgs
from pdf import eliminar_archivo_pdf
from SoporteTexto import reglas, mensajes, msn_info
from time import sleep

'''
REQUERIMENTS

$ pip install pyTelegramBotAPI
$ pip install img2pdf
'''

# TOKE  para el acceso al bot
BOT_TOKEN = "BOT_TOKEY"
# INREVALO DE TIEMPO PARA EL REINICIO DEL BO EN CASO DE QUE OCURRA UN ERROR
BOT_INTERVAL = 3
BOT_TIMEOUT = 30

bot = telebot.TeleBot(BOT_TOKEN)

# METODO DE ESCUCHA PARA TEXTO, IMAGENES, VIDEOS, ENTRO OTROS
def listener(mensaje_telegram):

    for mensaje in mensaje_telegram:
        
        chatID = mensaje.chat.id
        user = mensaje.chat.username
        # TIPO DE MENSAJE QUE ENVIA EL USUARIO
        if(mensaje.content_type == "text"):
            
            if(mensaje.text == "TODO EN UN PDF 🗃"):
                # SE COMPRUEBA SI EXISE O CONTIENE IMAGENES
                comprobar = verificar(chatID)
                if(comprobar):
                    bot.send_message(chatID, str(mensajes[0]))
                    print("Cargar PDF")
                    sleep(5)
                    aletario = randrange(9999999)
                    nombrePDF = "./PDFs/" + "ToKayPDF" + "_" + str(aletario) + ".pdf" 
                    crear_todo_pdf(chatID, nombrePDF) # CREAR PDF
                    cargar(bot,chatID,nombrePDF) # CARGA PDF Y ENVIAR
                    eliminar_archivo_pdf(nombrePDF) # ELIMINAR PDF
                    eliminar_archiv_imgs(chatID) # ELIMINAR EL DIRECTORIO DE IMAGENES DEL USUARIO
                    bot.send_message(chatID, mensajes[1])
                else:
                    bot.send_message(chatID, mensajes[2])
            elif(mensaje.text == "REGLAS 📏"):
                bot.send_message(chatID, reglas)
            elif(mensaje.text == "INFO ℹ"):
                bot.send_message(chatID, msn_info, parse_mode='HTML', disable_web_page_preview=True)
        elif(mensaje.content_type == "photo"):
            if(cantidad_archivos(chatID) <=16):
                fileID = mensaje.photo[-1].file_id  # EXTRAER ID FILE
                # DESCARGAR IMAGENS DENTRO DE UN HILO
                hilo_descargar = threading.Thread(target=descargar, args=(bot, fileID, chatID,))
                hilo_descargar.start()
            else:
                bot.send_message(chatID, mensajes[3])
                
# METODO DE ESCUCHA DEL BOT
bot.set_update_listener(listener)
# METODO PARA EJECUTAR EL BOT
def bot_polling():
    print("EMPEZANDO BOT ...")
    while True:
        try:
            print("NUEVA INSTANCIA DE BOT INICIADA")
            #bot = telebot.TeleBot(BOT_TOKEN) #Generate new bot instance
            botactions(bot) #If bot is used as a global variable, remove bot as an input param
            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)
        except Exception as ex: #ERROR EN EL POLLING
            print("FALLÓ EL SONDEO DEL BOT, REINICIANDO EN {}sec. ERROR:\n{}".format(BOT_TIMEOUT, ex))
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else: # CIERRE LIMPIO
            bot.stop_polling()
            print("BOT TERMINADO")
            break # FIN DEL BLUCE

def botactions(bot):
    # EVENTO DE BIENVENIDA
    @bot.message_handler(commands=["start"])
    def command_start(message):
        chatID = message.chat.id
        nombre = message.chat.first_name
        bot.send_message(chatID,"Bienvenid@ "+ nombre + " 😊 a ToKayPDF, un convertidor de imagenes a PDF")
       #CREAR BOTOENES
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        boton_1 = types.KeyboardButton("TODO EN UN PDF 🗃")
        boton_2 = types.KeyboardButton("REGLAS 📏")
        boton_3 = types.KeyboardButton("INFO ℹ")
        markup.add(boton_1, boton_2, boton_3) # AGREAR BOTONES AL MAKUP
        bot.send_message(chatID, nombre  + " 😊 puedes enviar una o varias imágenes para luego convertirlo en un pdf")
        bot.send_message(chatID, "Elija una opción", reply_markup=markup)


# FUNCION PARA DESCARGA LA FOTO
def descargar(bot, fileID, chatID):
    file_info = bot.get_file(fileID) #A OBTENER EL ARCHIVO O  O LA IMAGEN
    download = bot.download_file(file_info.file_path) # DESCARGAR LA IMAGEN
    nombre_archivo = crear_archivo(chatID)
    guardar(nombre_archivo, download) # ALMACENAR LA IMAGEN

# FUNCION PARA CARGAR Y ENVIAR EL PDF
def cargar(bot, chatID, nombrePDF):
    doc = open(nombrePDF, "rb")
    bot.send_document(chatID,doc)

# CORRIENDO CON HILO
polling_thread = threading.Thread(target=bot_polling)
polling_thread.daemon = True
polling_thread.start()


#EJECUCION PRINCIPAL MIENTRAS CORRE EN EL HILO
if __name__ == "__main__":
    while True:
        try:
            sleep(120)
        except KeyboardInterrupt:
            break