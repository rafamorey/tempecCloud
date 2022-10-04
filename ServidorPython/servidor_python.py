import datetime
import pymongo            
import paho.mqtt.client as mqtt                   
import paho.mqtt.publish as publish                         
import time                                      
import concurrent.futures

executor = concurrent.futures.ThreadPoolExecutor(max_workers=10) 

def tic_tac(): # Funcion Bucle Alive
    for r in db.list_collection_names():
        if r != 'Historial' and r != 'Enterprises':
            if db['fHistorial_'+ r.split('_')[1]].count_documents({}) > 0:
                for g in db['fHistorial_'+ r.split('_')[1]].aggregate([{'$group': {'_id':{}, 'fecha': {'$last':'$date'}}}]):
                    c = datetime.datetime.now() - g['fecha']
                    bol = True if c.days < 1 and c.seconds < 300 else False

                    for ex in enterprises.aggregate([{'$match': {'devices.id': r.split('_')[1]}},
                                                    {'$project':{'_id':0, 'index': {'$indexOfArray': ["$devices.id", r.split('_')[1]]}}}]):
                        idx = ex['index']

                    enterprises.update_one({'devices.id': str(r.split('_')[1])},{'$set': {
                                                    f'devices.{idx}.online' : bol,
                                                    }})
            else:
                print(f"El equipo {r.split('_')[1]} aun no tiene datos")

def tac_tic():
    for r in db.list_collection_names():
        if r != 'Historial' and r != 'Enterprises':
            for x in enterprises.aggregate([{'$match': {'devices.id': {'$eq': r.split('_')[1]}}},
                            {'$unwind': '$devices'},
                            {'$match' : {'devices.id': {'$eq': r.split('_')[1]}}},
                            {'$project': {'_id':0,  'grados': '$devices.grados'}}
                            ]):
                grados = x['grados']
                print(grados)

def bucle_alive(): # Funcion Bucle Alive
    while True:
        for tiempo_alive in range(1,6):
            print(f"{tiempo_alive} - 5 _Online")
            time.sleep(1)
        tic_tac()
        tac_tic()
        print("Done !")

def insertar_f_historial(msg_payload : str):
    for x in enterprises.aggregate([{'$match': {'devices.id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$unwind': '$devices'},
                            {'$match' : {'devices.id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$project': {'_id':0,  'grados': '$devices.grados'}}
                            ]):
        grados = x['grados']

    f_historial = db['fHistorial_' + str(msg_payload.split('/')[1])]

    dic_f = {
        'int': float(msg_payload.split('/')[2]),
        'ext': float(msg_payload.split('/')[3]),
        'grados': grados,
        'date': datetime.datetime.now()
    }
    # f_historial.insert_one(dic_f)
    print(dic_f)

def update_device(msg_payload):
    id_dispositivo = msg_payload.split('/')[1]
    for r in enterprises.aggregate([{'$match': {'devices.id': id_dispositivo}},
                        {'$project':{'_id':0, 'index': {'$indexOfArray': ["$devices.id", id_dispositivo]}}}]):
        idx = str(r['index'])
        print(idx)
    print(id_dispositivo)
    enterprises.update_one({'devices.id': id_dispositivo},{'$set': {
                                             f'devices.{idx}.name' : msg_payload.split('/')[2],
                                             f'devices.{idx}.setpoint' : float(msg_payload.split('/')[3]),
                                             f'devices.{idx}.hisH' : float(msg_payload.split('/')[4]), 
                                             f'devices.{idx}.hisL': float(msg_payload.split('/')[5]),
                                             f'devices.{idx}.alarmaH': float(msg_payload.split('/')[6]),
                                             f'devices.{idx}.alarmaL': float(msg_payload.split('/')[7]),
                                             f'devices.{idx}.grados': msg_payload.split('/')[8],
                                             f'devices.{idx}.last_update' : datetime.datetime.now()
                                             }})
    print("====Update==================================" + str(datetime.datetime.now()) +"=============================================")

def main(msg_payload):   
    print(msg_payload)
    if enterprises.count_documents({'devices.id': msg_payload.split('/')[1]}) > 0:
        print(f'Si existe el dispositivo')
        if msg_payload.split('/')[0] == '10':
            insertar_f_historial(msg_payload)
        elif msg_payload.split('/')[0] == '20':
            update_device(msg_payload)
        elif msg_payload.split('/')[0] == '30':
            primer = True if historial.count_documents({'d_id':msg_payload.split('/')[1]}) > 0 else False
            insertar_historial(primer, 30, msg_payload)

def on_connect(client, userdata, flags, rc):
    client.subscribe("Tempec/Server")
    print(" GOGOGOGO     GOGOGO              GO")
    print("GO          GO      GO            GO")
    print("GO   GOGO   GO      GO            GO")
    print("GO     GO   GO      GO      ")
    print(" GOGOGO       GOGOGO              GO")
    print("\n")

def on_message(client, userdata, msg):
    executor.submit(main, msg.payload.decode())          

def tendencia(a):#Funcion Historial
    tendencia = 0
    qwer = 0
    print("_Ultimos 5 datos de = " + str(a))

    a = [ele for ele in a if ele > 0] 
    print("_Elimino todos los -127 = " + str(a))

    if len(a) < 1:
        print("!_Todos los datos eran -127")
        qwer = -127
    elif len(a) == 1:
        qwer = a
        print("!_Solo quedo este dato = " + str(a))
    else:
        print("_Estos son los datos que no son negativos = " + str(a))
        for _ in range(2):
            if max(a) > min(a) * 1.2:
                a.remove(max(a))
                a.remove(min(a))
            print(f"_Eliminando acknowlage = " + str(a))

        if len(a) < 1:
            qwer = 111
            print("!_Todos los datos eran acknowlage")
        elif len(a) == 1:
            qwer = a
            print("!_Solo quedo este dato = " + str(a))
        else:
            print("_Estos son los datos que no son acknowlage = " + str(a))
            for i in range(0, len(a)-1): 
                if a[i] > a[i+1]:
                    tendencia+=1
                elif a[i] < a[i+1]:
                    tendencia-=1
            suma = round(sum(a)/len(a),2)
            print("_La tendencia es = " + str(tendencia))
            if tendencia > 1:
                qwer = max(a)
                print("!_Este es el dato = " + str(max(a)))
            elif tendencia < -1:
                qwer = min(a)
                print("!_Este es el dato = " + str(min(a)))
            else:
                qwer = suma
                print("!_Este es el dato = " + str(suma))   
    
    return float(str(qwer).replace('[','').replace(']',''))

def grafica():#Funcion Historial
    for r in db.list_collection_names():
        if r != 'Historial' and r != 'Enterprises':
            for c in enterprises.aggregate([{'$match': {'devices.id': {'$eq': r.split('_')[1]}}},
                            {'$unwind': '$devices'},
                            {'$match' : {'devices.id': {'$eq': r.split('_')[1]}}},
                            {'$project': {'_id':0,  'name': '$devices.name', 'alive': '$devices.online'}}
                            ]):

                if c['alive']:
                    if db['fHistorial_' + r.split('_')[1]].count_documents({}) > 0:
                        v1_arr, v2_arr, k_arr = [], [], []
                    
                        for g in db['fHistorial_' + r.split('_')[1]].find({},{'_id':0}).sort('date',-1).limit(5):
                            v1_arr.append(g['int'])
                            v2_arr.append(g['ext'])
                            k_arr.append(g['grados'])

                        value_array = trasformada(v1_arr, k_arr)

                        valor = tendencia(value_array)
                        print(valor)
                        msg = 'aux/' + r.split('_')[1] + '/' + str(valor) + '/' + str(v2_arr[0])
                        # Hasta este punto tengo el msg con el valor que sera procesado con la ultima X (para saber de que hablo recordar al pizarron)

                        k = True if db['fHistorial_' + r.split('_')[1]].count_documents({}) <= 0 else False

                        insertar_historial(k, r.split('_')[1], msg)
                    else:
                        print(f"El equipo {r.split('_')[1]} aun no tiene datos")
                    
                else:
                    print(f"El equipo {r.split('_')[1]} esta offline")

def insertar_historial(first_msg, opcion, msg_payload: str):#Funcion Historial
    conta = 0
    for z in enterprises.aggregate([{'$match': {'devices.id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$unwind': '$devices'},
                            {'$match' : {'devices.id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$project': {'_id':0, 'nombre': '$devices.name', 'sp': '$devices.setpoint', 'hmax': '$devices.hisH', 'hmin': '$devices.hisL'}}
                            ]):
        _name = z['nombre']
        _setpoint = z['sp']
        hisH = z['hmax']
        hisL  = z['hmin']

    d_id = msg_payload.split('/')[1]
    tempInt = float(msg_payload.split('/')[2])
    tempExt = float(msg_payload.split('/')[3])

    if first_msg:
        tempMax = float(msg_payload.split('/')[2])
        dateMax = datetime.datetime.now()
        tempMin = float(msg_payload.split('/')[2])
        dateMin = datetime.datetime.now()
        _date = datetime.datetime.now()
        conta = 0
        fake = tempInt
        print("Fue el primer msg en F\nTengo todo")
    else:
        if historial.count_documents({'d_id': d_id}) > 0:
            print("No es el primer msg en H")
            do = False
            for g in historial.find({'d_id': d_id},{'_id':0,'tempMax':1, 'tempMin':1, 'tempExt':1, 'tempInt':1, 'dateMax':1, 'dateMin':1, 'fake':1, 'date':1}).sort('date',-1).limit(1):
                tempMax = g['tempMax']
                dateMax = g['dateMax']
                tempMin = g['tempMin']
                dateMin = g['dateMin']
                print("No fue el primer msg")
                if opcion == 30:
                    do = False
                    fake = tempInt
                    x = (g['date'] + datetime.timedelta(seconds=300)) - datetime.datetime.now()    
                    print("Para este punto ya tengo todo")
                else:
                    x = datetime.timedelta(seconds=0)
                    print("Para este punto me falta el count y fake")
                    if float(msg_payload.split('/')[2]) != -127 and float(msg_payload.split('/')[2]) != 111:
                        do = False
                        fake = tempInt
                        print("Para este punto me falta el count 0")
                    else:
                        do = True
                        fake = g['fake']
                        print("Para este punto me falta el count 1")

            if float(msg_payload.split('/')[2]) > tempMax and float(msg_payload.split('/')[2]) != -127:  
                tempMax = float(msg_payload.split('/')[2])
                dateMax = datetime.datetime.now() + x

            elif float(msg_payload.split('/')[2]) < tempMin and float(msg_payload.split('/')[2]) != -127:
                tempMin = float(msg_payload.split('/')[2])
                dateMin = datetime.datetime.now() + x

            _date = datetime.datetime.now() + x

            if g['tempInt'] * 1.2 < tempInt or g['tempInt'] * 0.8 > tempInt:
                for con in db['Historial'].find({'d_id': msg_payload.split('/')[1]},{'_id':0,'contador':1, 'date':1}).sort('date',-1).limit(1):
                    pass
                if do:
                    conta = (con['contador'] + 1) if con['contador'] < 3 else 3 
                else:
                    conta = 0
            else:
                conta = 0
            print(conta)
            print("Para este punto ya tengo todo")
        else:
            print("Es el primer msg en H")
            tempMax = float(msg_payload.split('/')[2])
            dateMax = datetime.datetime.now()
            tempMin = float(msg_payload.split('/')[2])
            dateMin = datetime.datetime.now()
            _date = datetime.datetime.now()
            conta = 0
            fake = tempInt
            print("Fue el primer msg\nTengo todo")

    dic = {
        'd_id': d_id,
        'name': _name,
        'setpoint': _setpoint,
        'tempInt': tempInt,
        'tempExt': tempExt,
        'hisH': hisH,
        'hisL': hisL,
        'tempMax': tempMax,
        'dateMax': dateMax,
        'tempMin': tempMin,
        'dateMin': dateMin,
        'fake': fake,
        'contador': conta,
        'date': _date
    }

    # historial.insert_one(dic)
    print(dic)

def trasformada(v_arr2, k_arr2):#Funcion Historial
    value_array2 = []
    ky = True if k_arr2[0] == 'C' else False
    idx = 0
    for re in k_arr2:
        if re == 'F' and ky:
            v_arr2[idx] = (v_arr2[idx] - 32) * (5/9)
        elif re == 'C' and not ky:
            v_arr2[idx] = (v_arr2[idx] * (9/5)) + 32
        value_array2.append(round(v_arr2[idx],2))
        idx+=1
    return value_array2

def bucle(): #Funcion Historial
    time.sleep(5)
    while True:
        grafica()
        for tiempo_grafica in range(1,31):
            print(f"{tiempo_grafica} - 30 Historial")
            time.sleep(1)

print("Iniciando MongoDB...")
mongo = pymongo.MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
db = mongo['Tempec_Cloud']                                                   
enterprises = db['Enterprises']                                            
historial = db['Historial']            
print("MongoDB iniciado")

print("Iniciando MQTT...")
monzav = mqtt.Client()  
monzav.connect("test.mosquitto.org", 1883, 60) 

print("MQTT Iniciando")
monzav.on_connect = on_connect                                     
monzav.on_message = on_message                                                 
#monzav.connect("6c665d3e9b974b849cffc4266267b47b.s2.eu.hivemq.cloud", 8883, 10)
# executor.submit(bucle)
executor.submit(bucle_alive)
monzav.loop_forever()