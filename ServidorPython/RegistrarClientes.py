from datetime import datetime
from pymongo import MongoClient

# Enterprise AA
# User       AAA
# Devices    AAAA
# mongo = MongoClient('127.0.0.1', 27017)
mongo = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
db = mongo['Tempec_Cloud']
enterprise = db['Enterprises']

def registrar_empresa():
    print("================ DATOS DE LA EMPRESA ====================")
    id = input("_id: ")
    enterpri = input("enterprise: ")
    password = input("passoword: ")
    phone = input("phone: ")
    email = input("email: ")
    
    dic = {
        'e_id':id,
        'enterprise':enterpri,
        'e_password':password,
        'e_phone': int(phone),
        'e_email':email,
        'users': []
    }
    enterprise.insert_one(dic)
    print("Done!\n\n")

def comprobar_usuario(id_entreprise):
    id_usuario = input("Ingrese id de usuario: ")
    if enterprise.count_documents({'$and':[{'e_id':id_entreprise},{'users.u_id':id_usuario}]}) > 0:
        registrar_dispositivo(id_entreprise, id_usuario)
    else:
        print("No se encontro ese id de usuario en esa Empresa")

def comprobar_empresa(o):
    print("================DATOS DEL USUARIO====================")
    id = input("Ingrese id de Empresa: ")
    if enterprise.count_documents({'e_id':id}) > 0:
        print("La empresa es ", enterprise.find_one({'e_id':id})['enterprise'])
        if o == 0:
                registrar_usuario(id)
        elif o == 1:
            comprobar_usuario(id)
    else:
        print("No se encontro ninguna empresa con ese id")

def registrar_dispositivo(e_id, u_id):
    dic = {
        'd_id': input("d_id: "),
        'd_name': input("d_name: "),
        'location': input("location: "),
        'setpoint': float(input("setpoint: ")),
        'histeresis_high': float(input("histeresis_high: ")),
        'histeresis_low': float(input("histeresis_low: ")),
        'last_update': datetime.now(),
        'online': False
    }
    for r in enterprise.aggregate([{'$match': {'users.u_id': u_id}},
                                    {'$project':{'_id':0, 'index': {'$indexOfArray': ["$users.u_id", u_id]}}}]):
        ind = r['index']
    enterprise.update_one({'e_id': e_id }, {'$push' : {f'users.{ind}.devices' : dic }})
    print("Done!\n\n")

def registrar_usuario(id):
    u_id = input("id: ")
    u_name = input("name: ")
    u_password = input("password: ")
    u_phone = input("phone: ")
    u_email = input("email: ")
    dic = {
        'u_id':u_id,
        'u_name':u_name,
        'u_password':u_password,
        'u_phone':u_phone,
        'u_email':u_email,
        'devices':[]
    }

    enterprise.update_one({'e_id': id }, {'$push' : {'users' : dic }})
    print("Done!\n\n")

def inicio():
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("                           Programa para Registrar Empresas, Usuarios y Dispositivos")
    print("1- Registrar Empresa")
    print("2- Registrar Cliente")
    print("3- Registrar Dispositivo")

    opcion = input("          Opcion:")

    if opcion == '1':
      registrar_empresa()
    elif opcion == '2':
        comprobar_empresa(0)
    elif opcion == '3':
        comprobar_empresa(1)
        pass
    else:
        print("Skeereeee")

while 1:
    inicio()

# Enterprise    AB
# User          AAG
# Device        AAAG