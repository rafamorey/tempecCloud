import datetime
import pymongo            
import paho.mqtt.client as mqtt                                           
import time                                      
import concurrent.futures

cuerdas = concurrent.futures.ThreadPoolExecutor(max_workers=10) 
unosiunono = True
def ONLINE_DEVICE():
    for r in db.list_collection_names():
        if r != 'enterprises' and r != 'devices' and r != 'usuarios':
            if db['fHistorial_'+ r.split('_')[1]].count_documents({}) > 0:             
                for g in db['fHistorial_'+ r.split('_')[1]].aggregate([{'$group': {'_id':{}, 'fecha': {'$last':'$date'}}}]):
                    c = datetime.datetime.now() - g['fecha']

                    bol = True if c.days < 1 and c.seconds < 300 else False

                    for ex in enterprises.aggregate([{'$match': {'devices.id': r.split('_')[1]}},
                                                    {'$project':{'_id':0, 'index': {'$indexOfArray': ["$devices.id", r.split('_')[1]]}}}]):
                        idx = ex['index']

                    print(f"{r} Online? {bol}")

                    enterprises.update_one({'devices.id': str(r.split('_')[1])},{'$set': {
                                                    f'devices.{idx}.online' : bol,
                                                    }})
            else:
                print(f"El equipo {r.split('_')[1]} aun no tiene datos")

def UPDATE_CONFIG_DEVICE_DB():
    for r in db.list_collection_names():
        if r != 'devices' and r != 'enterprises' and r != 'usuarios':
            id_dispositivo = r.split('_')[1]
            for x in enterprises.aggregate([{'$match': {'devices.id': {'$eq': r.split('_')[1]}}},
                            {'$unwind': '$devices'},
                            {'$match' : {'devices.id': {'$eq': r.split('_')[1]}}},
                            {'$project': {'_id':0, 'last_setpoint': '$devices.last_setpoint', 'last_hisH': '$devices.last_histH', 'last_hisL': '$devices.last_histL', 'last_alarmaH': '$devices.last_alarmaH', 'last_alarmaL': '$devices.last_alarmaL', 'last_grados': '$devices.last_grados', 'setpoint': '$devices.setPoint', 'hisH': '$devices.histH', 'hisL': '$devices.histL', 'alarmaH': '$devices.alarmaH', 'alarmaL': '$devices.alarmaL', 'grados': '$devices.grados'}}
                            ]):
                if x['setpoint'] != x['last_setpoint'] or x['hisH'] != x['last_hisH'] or x['hisL'] != x['last_hisL'] or x['alarmaH'] != x['last_alarmaH'] or x['alarmaL'] != x['last_alarmaL'] or x['grados'] != x['last_grados']:
                    for r in enterprises.aggregate([{'$match': {'devices.id': id_dispositivo}},
                                {'$project':{'_id':0, 'index': {'$indexOfArray': ["$devices.id", id_dispositivo]}}}]):
                        idx = str(r['index'])
                    enterprises.update_one({'devices.id': id_dispositivo},{'$set': {
                        f'devices.{idx}.last_name' : x['name'],
                        f'devices.{idx}.last_setpoint' : x['setpoint'],
                        f'devices.{idx}.last_histH' : x['hisH'],
                        f'devices.{idx}.last_histL': x['hisL'],
                        f'devices.{idx}.last_alarmaH': x['alarmaH'],
                        f'devices.{idx}.last_alarmaL': x['alarmaL'],
                        f'devices.{idx}.last_grados': x['grados'],
                        # f'devices.{idx}.last_update' : datetime.datetime.now() 
                        }})
                    mqttClient.publish('Tempec/' + id_dispositivo + "'", '20/' + id_dispositivo + '/' + x['name']  + '/' + str(x['setpoint']) + '/' + str(x['hisH']) + '/' + str(x['hisL']) + '/' + str(x['alarmaH']) + '/' + str(x['alarmaL']) + '/' + x['grados']) 

def BUCLE_ULTRA_INSTINTO():
    while True:
        ONLINE_DEVICE()
        UPDATE_CONFIG_DEVICE_DB()
        #print(F"UI - {datetime.datetime.now()}")
        time.sleep(74)

def INSERTAR_FHISTORIAL(msg_payload : str):
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
    f_historial.insert_one(dic_f)

def UPDATE_CONFIG_DEVICE_20(msg_payload):
    id_dispositivo = msg_payload.split('/')[1]
    for r in enterprises.aggregate([{'$match': {'devices.id': id_dispositivo}},
                        {'$project':{'_id':0, 'index': {'$indexOfArray': ["$devices.id", id_dispositivo]}}}]):
        idx = str(r['index'])

    enterprises.update_one({'devices.id': id_dispositivo},{'$set': {
                                             #f'devices.{idx}.name' : msg_payload.split('/')[2],
                                             f'devices.{idx}.setPoint' : float(msg_payload.split('/')[3]),
                                             f'devices.{idx}.histH' : float(msg_payload.split('/')[4]), 
                                             f'devices.{idx}.histL': float(msg_payload.split('/')[5]),
                                             #f'devices.{idx}.alarmaH': float(msg_payload.split('/')[6]),
                                             #f'devices.{idx}.alarmaL': float(msg_payload.split('/')[7]),
                                             #f'devices.{idx}.grados': msg_payload.split('/')[8],
                                             #f'devices.{idx}.last_name' : msg_payload.split('/')[2],
                                             #f'devices.{idx}.last_setpoint' : float(msg_payload.split('/')[3]),
                                             #f'devices.{idx}.last_histH' : float(msg_payload.split('/')[4]), 
                                             #f'devices.{idx}.last_histL': float(msg_payload.split('/')[5]),
                                             #f'devices.{idx}.last_alarmaH': float(msg_payload.split('/')[6]),
                                             #f'devices.{idx}.last_alarmaL': float(msg_payload.split('/')[7]),
                                             #f'devices.{idx}.last_grados': msg_payload.split('/')[8],
                                            #  f'devices.{idx}.date' : datetime.datetime.now()
                                             }})
    print(f"Update {id_dispositivo}")

def BLAST(msg_payload):   
    print(f"= = = = = = = = = {datetime.datetime.now()} = = = = = = = = = = = = = = = = = = = = = = = > {msg_payload}")
    if enterprises.count_documents({'devices.id': msg_payload.split('/')[1]}) > 0:
        if msg_payload.split('/')[0] == '10':
            INSERTAR_FHISTORIAL(msg_payload)
        elif msg_payload.split('/')[0] == '20':
            UPDATE_CONFIG_DEVICE_20(msg_payload)
        elif msg_payload.split('/')[0] == '30':
            primer = True if historial.count_documents({'_id':msg_payload.split('/')[1]}) > 0 else False
            INSERTAR_HISTORIAL(primer, 30, msg_payload)

def CONEISHION(client, userdata, flags, rc):
    client.subscribe("Tempec/Server")
    print(f"QMTT - Conexion Establecida {datetime.datetime.now()}")

def MESSAGEISHION(client, userdata, msg):
    cuerdas.submit(BLAST, msg.payload.decode())          

def TENDEISHION(a):
    tendencia = 0
    qwer = 0
    axu = str(a)
    a = [ele for ele in a if ele > 0] 

    if len(a) < 1:
        print(f"{axu} => -127")
        qwer = -127
    elif len(a) == 1:
        qwer = a
        print(f"{axu} => {str(a)}")
    else:
        for _ in range(2):
            if max(a) > min(a) * 1.2:
                a.remove(max(a))
                a.remove(min(a))

        if len(a) < 1:
            qwer = 111
            print(f"{axu} => 111")
        elif len(a) == 1:
            qwer = a
            print(f"{axu} => {str(a)}")
        else:
            for i in range(0, len(a)-1): 
                if a[i] > a[i+1]:
                    tendencia+=1
                elif a[i] < a[i+1]:
                    tendencia-=1
            suma = round(sum(a)/len(a),2)

            if tendencia > 1:
                qwer = max(a)
                print(f"{axu} => {max(a)}")
            elif tendencia < -1:
                qwer = min(a)
                print(f"{axu} => {min(a)}")
            else:
                qwer = suma
                print(f"{axu} => " + str(suma))   
    
    return float(str(qwer).replace('[','').replace(']',''))

def EL_COLECCIONISTA():
    for r in db.list_collection_names():
        if r != 'devices' and r != 'enterprises' and r != 'usuarios':
            #print(r)
            for c in enterprises.aggregate([{'$match': {'devices.id': {'$eq': r.split('_')[1]}}},
                            {'$unwind': '$devices'},
                            {'$match' : {'devices.id': {'$eq': r.split('_')[1]}}},
                            {'$project': {'_id':0,  'name': '$devices.name', 'alive': '$devices.online'}}
                            ]):
                if c['alive']:
                    #print("alive")
                    if db['fHistorial_' + r.split('_')[1]].count_documents({}) > 0:
                        v1_arr, v2_arr, k_arr = [], [], []
                    
                        for g in db['fHistorial_' + r.split('_')[1]].find({},{'_id':0}).sort('date',-1).limit(5):
                            v1_arr.append(g['int'])
                            v2_arr.append(g['ext'])
                            k_arr.append(g['grados'])

                        value_array = FAHRENHEIT_OR_CELCIUS(v1_arr, k_arr)
                        valor = TENDEISHION(value_array)

                        msg = 'aux/' + r.split('_')[1] + '/' + str(valor) + '/' + str(v2_arr[0])

                        k = True if db['fHistorial_' + r.split('_')[1]].count_documents({}) <= 0 else False

                        INSERTAR_HISTORIAL(k, r.split('_')[1], msg)
                    else:
                        print(f"El equipo {r.split('_')[1]} aun no tiene datos")

def INSERTAR_HISTORIAL(first_msg, opcion, msg_payload: str):
    conta = 0
    door = 0
    for z in enterprises.aggregate([{'$match': {'devices.id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$unwind': '$devices'},
                            {'$match' : {'devices.id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$project': {'_id':0, 'enter':'$enterprise', 'nombre': '$devices.name', 'sp': '$devices.setPoint', 'hmax': '$devices.histH', 'hmin': '$devices.histL'}}
                            ]):
        enter = z['enter']
        _name = z['nombre']
        _setpoint = z['sp']
        hisH = z['hmax']
        hisL  = z['hmin']

    d_id = msg_payload.split('/')[1]
    tempInt_actual = float(msg_payload.split('/')[2])
    tempExt = float(msg_payload.split('/')[3])

    if first_msg:
        tempMax = float(msg_payload.split('/')[2])
        dateMax = datetime.datetime.now()
        tempMin = float(msg_payload.split('/')[2])
        dateMin = datetime.datetime.now()
        _date = datetime.datetime.now()
        conta = 0
        fake = tempInt_actual

    else:
        if historial.count_documents({'id': d_id}) > 0:
            do = False
            for g in historial.find({'id': d_id},{'_id':0,'tempMax':1, 'tempMin':1, 'tempExt':1, 'tempInt':1, 'dateMax':1, 'dateMin':1, 'fake':1, 'date':1}).sort('date',-1).limit(1):
                tempMax = g['tempMax']
                dateMax = g['dateMax']
                tempMin = g['tempMin']
                dateMin = g['dateMin']

                if opcion == 30:
                    try:
                        if unosiunono:
                            if int(msg_payload.split('/')[4]) > 0: 
                                cantidad = msg_payload.split('/')[4] * 60
                                do = False
                                fake = tempInt_actual
                                x = datetime.datetime.now() - datetime.timedelta(seconds=cantidad)
                                unosiunono = False
                                door = msg_payload.split('/')[5]
                        else:
                            unosiunono = True
                            break
                    except:
                        do = False
                        fake = tempInt_actual
                        x = (g['date'] + datetime.timedelta(seconds=120)) - datetime.datetime.now()                       
                else:
                    x = datetime.timedelta(seconds=0)
                    do = True
                    door = msg_payload.split('/')[4]
                    if float(msg_payload.split('/')[2]) != -127.0 and float(msg_payload.split('/')[2]) != 111:
                        fake = tempInt_actual
                    else:
                        fake = g['fake']
  
            if float(msg_payload.split('/')[2]) > tempMax and float(msg_payload.split('/')[2]) != -127:  
                tempMax = float(msg_payload.split('/')[2])
                dateMax = datetime.datetime.now() + x
        
            elif float(msg_payload.split('/')[2]) < tempMin and float(msg_payload.split('/')[2]) != -127:
                tempMin = float(msg_payload.split('/')[2])
                dateMin = datetime.datetime.now() + x
            _date = datetime.datetime.now() + x
            # print(f"if {tempInt_actual} > {g['fake']} * 1.2 <")
            if tempInt_actual > g['fake'] * 1.2 or tempInt_actual < g['fake'] * 0.8:
                for con in db['devices'].find({'id': msg_payload.split('/')[1]},{'_id':0,'contador':1, 'date':1}).sort('date',-1).limit(1):
                    # Si aumento contador
                    if do:
                        conta = (con['contador'] + 1) if con['contador'] < 3 else 3 
                        fake = g['fake']
                        # print(f"contador={conta} fake={fake} ultima")
                    # No aumento contador
                    else:
                        conta = con['contador']
                        fake = tempInt_actual
                        # print(f"contador={conta} fake={fake} actual")
            # Si no es acknowlage
            else:
                conta = 0
                fake = tempInt_actual
                # print(f"contador={conta} fake={fake} False")

        # Si es el primer msg en H
        else:
            # Los valores son iguales a los que actuales (No comparo)
            # print("Es el primer msg en H")
            tempMax = float(msg_payload.split('/')[2])
            dateMax = datetime.datetime.now()
            tempMin = float(msg_payload.split('/')[2])
            dateMin = datetime.datetime.now()
            _date = datetime.datetime.now()
            conta = 0
            fake = tempInt_actual

    if tempInt_actual == -127:
        tempInt_actual = _setpoint - 5
    dic = {
        'enterprise': enter,
        'id': d_id,
        'name': _name,
        'setPoint': _setpoint,
        'tempInt': tempInt_actual,
        'tempExt': tempExt,
        'histH': hisH,
        'histL': hisL,
        'tempMax': tempMax,
        'dateMax': dateMax,
        'tempMin': tempMin,
        'dateMin': dateMin,
        'fake': fake,
        'contador': conta,
        'door': door,
        'date': _date
    }
    # historial.insert_one({'si_si': 'no_no'})
    id_dispositivo = msg_payload.split('/')[1]
    for r in enterprises.aggregate([{'$match': {'devices.id': id_dispositivo}},
                        {'$project':{'_id':0, 'index': {'$indexOfArray': ["$devices.id", id_dispositivo]}}}]):
        idx = str(r['index'])

    enterprises.update_one({'devices.id': id_dispositivo},{'$set': {
                                             f'devices.{idx}.tempInt' : tempInt_actual,
                                             f'devices.{idx}.tempExt' : tempExt,
                                             f'devices.{idx}.tempMax' : tempMax,
                                             f'devices.{idx}.dateMax' : dateMax,
                                             f'devices.{idx}.tempMin' : tempMin,
                                             f'devices.{idx}.dateMin' : dateMin,
                                             }})
    historial.insert_one(dic)
    print(f"Done Insert - {msg_payload.split('/')[1]} con date = {_date}")

def FAHRENHEIT_OR_CELCIUS(v_arr2, k_arr2):
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

def BUCLE_ULTRA_EGO():
    while True:
        EL_COLECCIONISTA()
        #print(f"UE - {datetime.datetime.now()}")
        time.sleep(120)

try:
    print("Iniciando MongoDB")
    mongo = pymongo.MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
    #mongo = pymongo.MongoClient("mongodb+srv://rafaelDiinpec:Mr178910@tc.kshjevt.mongodb.net/?retryWrites=true&w=majority")
    # db = mongo['test']       
    db = mongo['Tempec_Cloud']                                            
    enterprises = db['enterprises']                                            
    historial = db['devices']            
    print("MongoDB iniciado")
except:
    print("Error conexion MongoDB")

try:
    print("Iniciando MQTT")
    mqttClient = mqtt.Client()  
    mqttClient.reconnect_delay_set(5,10)
    mqttClient.on_connect = CONEISHION                                     
    mqttClient.on_message = MESSAGEISHION    
    # mqttClient.on_disconnect = DISCONEISHION
    mqttClient.connect("test.mosquitto.org", 1883, 60)    
    print("MQTT Iniciando")      
except:
    print(f"Desconectado a {datetime.datetime.now()}")

#monzav.connect("6c665d3e9b974b849cffc4266267b47b.s2.eu.hivemq.cloud", 8883, 10)
cuerdas.submit(BUCLE_ULTRA_EGO)
cuerdas.submit(BUCLE_ULTRA_INSTINTO)
mqttClient.loop_forever()