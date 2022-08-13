#AAA000 Devices
#000AAA Users

from datetime import datetime
from pymongo import MongoClient

mongo = MongoClient('127.0.0.1', 27017)
db = mongo['Tempec']
users = db['Users']
historial = db['Historial']


def registrar_cliente():
    print("================DATOS DEL CLIENTE====================")
    print("id: ", end="")
    id = input()
    print("super: ", end="")
    super = input()
    print("nombre: ", end="")
    name = input()
    print("password: ", end="")
    password = input()
    print("phone: ", end="")
    phone = input()
    print("email: ", end="")
    email = input()
    
    dic = {
        '_id':id,
        'super':bool(super),
        'name':name,
        'password':password,
        'phone': int(phone),
        'email':email,
        'devices':[]
    }
    print("Estos son los datos que re registraron:")
    print(dic)
    print("\n\n")

def registrar_dispositivo():
    print("================DATOS DEL DISPOSITIVO====================")
    print("Ingrese el id: ", end="")
    id = input()
    if users.count_documents({'_id':id}) > 0:
        print("El usuario es ", users.find_one({'_id':id})['name'])
    else:
        print("No se encontro un usuario con ese id")

def inicio():
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("                           Programa para Registrar Clientes y/o Dispositivos")
    print("1- Registrar Cliente y Dispositivo")
    print("2- Registrar Dispositivo")
    print("3- Cerrar")
    opcion = input("          Opcion:")

    if opcion == '1':
      registrar_cliente()
    elif opcion == '2':
        registrar_dispositivo()
    elif opcion == '3':
        pass
    else:
        print("No te quieras pasar de listo!")

while True:
    inicio()
