from datetime import datetime
import pymongo

mongo = pymongo.MongoClient("mongodb+srv://rafaelDiinpec:Mr178910@tc.kshjevt.mongodb.net/?retryWrites=true&w=majority")
db = mongo['test']
enterprise = db['enterprises']
# devices = db['devices_id']

def registrar_dispositivo():
    e_id = input("ingrese sú enterprise: ")
    dic = {
        'id': input("ingrese id de dispositivo: "),
        'name': input("name: "),
        # 'enterprise': e_id,
        'setPoint': float(input("setpoint: ")),
        'tempInt': 0.0,
        'tempExt': 0.0,
        'histH': float(input("histeresis_high: ")),
        'histL': float(input("histeresis_low: ")),
        'tempMax': 0.0,
        'dateMax': datetime.now(),
        'tempMin': 0.0,
        'dateMin': datetime.now(),
        'alarmaH': 2.0,
        'alarmaL': 2.0,
        'online': False,
        'grados':'C',
        'last_name': 'Monzav',
        'last_setpoint': 0.0,
        'last_histH': 0.0,
        'last_histL': 0.0,
        'last_alarmaH':0.0,
        'last_alarmaL':0.0,
        'last_grados':'C',
        'date': datetime.now()
    }

    enterprise.update_one({'enterprise': e_id }, {'$push' : {'devices' : dic }})

    # devices.insert_one({'dev_id': ddd})
    print("Done!\n\n")

def registrar_usuario():
    enter = input("enterprise: ")
    u_name = input("name: ")
    u_password = input("password: ")
    u_phone = input("phone: ")
    u_email = input("email: ")
    dic = {
        'enterprise':enter,
        'name':u_name,
        'password':u_password,
        'email':u_email,
        'phone': int(u_phone),
        'devices':[],
        'date': datetime.now()
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