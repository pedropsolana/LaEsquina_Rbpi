import firebase_admin
import RPi.GPIO as GPIO
import time
from firebase_admin import credentials
from firebase_admin import db

SW=False

#Configuro PIN
PIN = 10
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN,GPIO.OUT)

#Cargo el certificado de mi proyecto en firebase
firebase_sdk = credentials.Certificate('ionic-laesquina-firebase-adminsdk-cedcg-8f5851c213.json')

#Hago referencia a la base de datos realtime database de firebase
firebase_admin.initialize_app(firebase_sdk,{'databaseURL':'https://ionic-laesquina-default-rtdb.europe-west1.firebasedatabase.app/'})

#Creo una coleccion con el nombre productos con un producto
ref = db.reference('/orders')

while True:
    
    #Cojo los datos y los paso a uun diccionario
    diccionario = ref.get()

    #Recorro el diccionario y si hay un solo registro con estado=1 quiere decir
    #que hay algun pedido en Abierto sin atender y pongo la variable a True
    for i in diccionario.items():
        for n in i[1].items():
            if n[0]=='estado':           
                print(n)
                if n[1]== '1':
                    SW=True
                else:
                    SW=False

    #Si la variable esta a True y encendemos luz, sino apagamos.
    if SW==True:
        GPIO.output(PIN,GPIO.HIGH)
    else:
        GPIO.output(PIN,GPIO.LOW)
    time.sleep(5)
    print("Paso")
