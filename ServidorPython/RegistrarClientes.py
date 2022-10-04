from datetime import datetime
from pymongo import MongoClient

mongo = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
db = mongo['Tempec_Cloud']
enterprise = db['Enterprises']
# devices = db['devices_id']

def registrar_dispositivo():
    e_id = input("ingrese sú _id: ")
    dic = {
        'id': input("ingrese id de dispositivo: "),
        'name': input("name: "),
        'setpoint': float(input("setpoint: ")),
        'tempInt': 0.0,
        'tempExt': 0.0,
        'hisH': float(input("histeresis_high: ")),
        'hisL': float(input("histeresis_low: ")),
        'tempMax': 0.0,
        'dateMax': datetime.now(),
        'tempMin': 0.0,
        'dateMin': datetime.now(),
        'alarmaH': 2.0,
        'alarmaL': 2.0,
        'online': False,
        'grados':'C',
        'last_setpoint': 0.0,
        'last_hisH': 0.0,
        'last_hisL': 0.0,
        'last_alarmaH':0.0,
        'last_alarmaL':0.0,
        'last_grados':'C',
        'last_update': datetime.now()
    }

    enterprise.update_one({'_id': e_id }, {'$push' : {'devices' : dic }})

    # devices.insert_one({'dev_id': ddd})
    print("Done!\n\n")

def registrar_usuario():
    u_id = input("id: ")
    u_name = input("name: ")
    u_password = input("password: ")
    u_phone = input("phone: ")
    u_email = input("email: ")
    dic = {
        '_id':u_id,
        'name':u_name,
        'password':u_password,
        'email':u_email,
        'phone': int(u_phone),
        'devices':[]
    }

    # enterprise.update_one({'e_id': id }, {'$push' : {'users' : dic }})
    enterprise.insert_one(dic)
    print("Done!\n\n")

def inicio():
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("                           Programa para Registrar Empresas, Usuarios y Dispositivos")
    print("1- Registrar Cliente")
    print("2- Registrar Dispositivo")

    opcion = input("          Opcion:")

    if opcion == '1':
        registrar_usuario()
    elif opcion == '2':
        registrar_dispositivo()
        pass
    else:
        print("Skeereeee")

while 1:
    inicio()