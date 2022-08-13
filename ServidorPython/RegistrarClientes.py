from datetime import datetime
from pymongo import MongoClient

mongo = MongoClient('127.0.0.1', 27017)
db = mongo['Tempec']
users = db['Users']
historial = db['Historial']

#
# ESTE CODIGO NO LO COMENTE POR QUE ES MUY INTUITIVO
#

def registrar_cliente():
    print("================DATOS DEL CLIENTE====================")
    id = input("id: ")
    super = input("super: ")
    name = input("nombre: ")
    password = input("passoword: ")
    phone = input("phone: ")
    email = input("email: ")
    
    dic = {
        '_id':id,
        'super':bool(super),
        'name':name,
        'password':password,
        'phone': int(phone),
        'email':email,
        'devices':[]
    }
    users.insert_one(dic)
    print("Estos son los datos del cliente agregado: ")
    print(dic)
    print("\n\n")

def comprobar_cliente():
    print("================DATOS DEL DISPOSITIVO====================")
    id = input("Ingrese id: ")
    if users.count_documents({'_id':id}) > 0:
        print("El usuario es ", users.find_one({'_id':id})['name'])
        registrar_dispositivo(id)
    else:
        print("No se encontro un usuario con ese id")

def registrar_dispositivo(id):
    id_d = input("id: ")
    name = input("name: ")
    location = input("location: ")
    setpoint = input("setpoint: ")
    hish = input("histeresis high: ")
    hisl = input("histeresis low: ")
    dic = {
        '_id':id_d,
        'name': name,
        'location': location,
        'setpoint': setpoint,
        'histeresis_high': hish,
        'histeresis_low': hisl,
        'last_update': str(datetime.now())
    }

    users.update_one({'_id': id }, {'$push' : {'devices' : dic }})
    print("Estos son los datos del dispositivo agregado: ")
    print(dic)
    print("\n\n")

def inicio():
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("                           Programa para Registrar Clientes y/o Dispositivos")
    print("1- Registrar Cliente")
    print("2- Registrar Dispositivo")
    print("3- Nosé")

    opcion = input("          Opcion:")

    if opcion == '1':
      registrar_cliente()
    elif opcion == '2':
        comprobar_cliente()
    else:
        print("No te quieras pasar de listo!")

while 1:
    inicio()