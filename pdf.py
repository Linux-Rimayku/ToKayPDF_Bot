from os import path
from glob import glob
from secrets import token_urlsafe
from os import listdir
from img2pdf import convert
from os import remove




# FUNCION QUE PERMITE VERIFICAR SI EXISTE EL DIRECTORIO E IMAGENES
def verificar(chatID):
    chat_id = str(chatID)
    ruta = "./imagenes/" + chat_id
    if(path.exists(ruta) and (len(glob(ruta +"/*"+".jpg"))>0)):
        return True
    else:
        return False


# FINCION QUE PERMITE GENERAR EL PDF Y ALMACENARLO
def crear_todo_pdf(chatID, nombrePDF):
    cantidad = 0
    imagenes = []
    ruta = "./imagenes/" + str(chatID) + "/"
    listarImagenes  = listdir(ruta)

    # listar archivos
    for list in listarImagenes:  
        #print(list)
        # listar imagenes que terminen con formato .jpg
        if(list.endswith(".jpg")):
            if(cantidad <=14):
                a = ruta +list
                imagenes.append(a)
                cantidad = cantidad +1
    print("Cantidad de imagenes: "+str(cantidad))
    documento = open(nombrePDF , "wb")
    documento.write(convert(imagenes))
    documento.close()

# FUNCION PARA ELIMINAR EL PDF
def eliminar_archivo_pdf(nombrePDF):
    remove(nombrePDF)


