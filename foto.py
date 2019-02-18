from secrets import token_urlsafe
from os import mkdir
from os import path
from os import getcwd
from time import sleep
from os import remove
from glob import glob
from shutil import rmtree


# ALMACENAR IMAGEN EN EL DIRECTORIO DEL USAURIO
def guardar(nombreArchivo,download):

    with open(nombreArchivo,"wb") as new_file:
        new_file.write(download)
        new_file.close()
    # ELIMINAR IMAGEN 
    eliminar_archivo(nombreArchivo)
    
        

def crear_archivo(chatID):
    aleatorio = token_urlsafe(15)
    nombreArchivo = str(chatID) + "_" + aleatorio + ".jpg"
    chat_id = str(chatID)
    carpeta = "./imagenes/"+ chat_id
    # SE COMRPUEBA SI EXISTE EL DIRECTORIO DEL USUARIO
    if(path.exists(carpeta)):
        ruta_archivo ="./imagenes/" + chat_id + "/" + nombreArchivo # RUTA DE LA  IMAGEN
        return ruta_archivo
    else:
        mkdir("./imagenes/" + str(chatID)) # SE CREAR DIRECTORIO DEL USUARIO EN EL CASO DE QUE NO EXISTA
        ruta_archivo = "./imagenes/" + chat_id +"/"+ nombreArchivo # RUTA DE LA IMAGEN
        return ruta_archivo
    

def eliminar_archivo(nombreArchivo):
    # tiempo en que tardará eliminarse
    sleep(300)
    if(path.exists(nombreArchivo)):
        remove(nombreArchivo)
    else:
        print("no existe, fue eliminado luego de que el pdf fue gnerado")

# FUNCION QUE DEVUELVE LA CANTIDAD DE IMAGENES QUE EXISTE EN EL DIRECOTRIO DEL  USUARIO
def cantidad_archivos(chatID):
    chat_id = str(chatID)
    ruta = "./imagenes/" + chat_id
    return len(glob(ruta +"/*"+".jpg"))

# FUNCION PARA ELIMINAR EL DIRECTORIO CON IMAGENES INCLUIDAS O NO INCLUIDAS DEL USUARIO
def eliminar_archiv_imgs(chatID):
    chat_id = str(chatID)
    ruta = "./imagenes/" + chat_id
    rmtree(ruta)