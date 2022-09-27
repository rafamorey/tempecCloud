from array import array
import datetime
from xmlrpc.client import NOT_WELLFORMED_ERROR
from pymongo import MongoClient                                                      
import time                                      

mongo = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
db = mongo['Tempec_Cloud']                                                   
enterprises = db['Enterprises']     
historial = db['Historial']  

def tendencia(a:array):
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
    return float(qwer)

def grafica():
    for r in db.list_collection_names():
        if r != 'Historial' and r != 'Enterprises':
            for x in enterprises.aggregate([{'$match': {'users.devices.d_id': {'$eq': r.split('_')[1]}}},
                            {'$unwind': '$users'},
                            {'$match' : {'users.devices.d_id': {'$eq': r.split('_')[1]}}},
                            {'$unwind': '$users.devices'},
                            {'$match' : {'users.devices.d_id': {'$eq': r.split('_')[1]}}},
                            {'$project': {'_id':0,  'alive': '$users.devices.online'}}]):

                if x['alive']:
                    v1_arr, v2_arr, k_arr , out0, out1 = [], [], [], [], []
                
                    for g in db['fHistorial_' + r.split('_')[1]].find({},{'_id':0}).sort('_date',-1).limit(5):
                        v1_arr.append(g['_inte'])
                        v2_arr.append(g['_exte'])
                        k_arr.append(g['_tipo'])
                        out0.append(g['_out_0'])
                        out1.append(g['_out_1'])

                    value_array = trasformada(v1_arr, k_arr)

                    valor = tendencia(value_array)

                    msg = 'aux/' + r.split('_')[1] + '/' + str(valor) + '/' + str(v2_arr[0]) + '/' + str(out0[0]) + '/' + str(out1[0])
                    # Hasta este punto tengo el msg con el valor que sera procesado con la ultima X (para saber de que hablo recordar al pizarron)
                    print("_Este es el msg = " + msg)

                    k = True if db['fHistorial_' + r.split('_')[1]].count_documents({}) <= 0 else False

                    insertar_historial(k, r.split('_')[1], msg)
                    
                else:
                    print(f"El equipo {r.split('_')[1]} esta offline")

def insertar_historial(first_msg, opcion, msg_payload: str):
    for x in enterprises.aggregate([{'$match': {'users.devices.d_id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$unwind': '$users'},
                            {'$match' : {'users.devices.d_id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$unwind': '$users.devices'},
                            {'$match' : {'users.devices.d_id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$project': {'_id':0, 'nombre': '$users.devices.d_name', 'sp': '$users.devices.setpoint', 'hmax': '$users.devices.histeresis_high', 'hmin': '$users.devices.histeresis_low'}}]):
           
        _name            = x['nombre']
        _setpoint        = x['sp']
        _histeresis_high = x['hmax']
        _histeresis_low  = x['hmin']

    d_id = msg_payload.split('/')[1]
    _temperatura_interior = float(msg_payload.split('/')[2])
    _temperatura_exterior = float(msg_payload.split('/')[3])
    print("Para este punto me faltan minimos, maximos, out's, count y fake")

    if first_msg:
        _temperatura_maxima = float(msg_payload.split('/')[2])
        _date_maxima = datetime.datetime.now()
        _temperatura_minima = float(msg_payload.split('/')[2])
        _date_minima = datetime.datetime.now()
        _date = datetime.datetime.now()
        conta = 0
        fake = _temperatura_interior
        if opcion == 30:
            _out_0 = False
            _out_1 = True
        else:
            _out_0 = bool(int(msg_payload.split('/')[4]))
            _out_1 = bool(int(msg_payload.split('/')[5]))
        print("Fue el primer msg en F\nTengo todo")
    else:
        if historial.count_documents({'d_id': d_id}) > 0:
            print("No es el primer msg en H")
            do = False
            for g in historial.find({'d_id': d_id},{'_id':0,'_temperatura_maxima':1, '_temperatura_minima':1, '_temperatura_exterior':1, '_temperatura_interior':1, '_date_maxima':1, '_date_minima':1, '_date':1}).sort('_date',-1).limit(1):
                _temperatura_maxima = g['_temperatura_maxima']
                _date_maxima = g['_date_maxima']
                _temperatura_minima = g['_temperatura_minima']
                _date_minima = g['_date_minima']
                print("No fue el primer msg")
                if opcion == 30:
                    _out_0 = False
                    _out_1 = False
                    do = False
                    fake = _temperatura_interior
                    x = (g['_date'] + datetime.timedelta(seconds=300)) - datetime.datetime.now()    
                    # Para este punto ya tengo todo y voy a comparar
                    print("Para este punto ya tengo todo")
                else:
                    _out_0 = bool(int(msg_payload.split('/')[4]))
                    _out_1 = bool(int(msg_payload.split('/')[5]))
                    x = 0
                    print("Para este punto me falta el count y fake")
                    # Para este punto solo me falta count y fake
                    if float(msg_payload.split('/')[2]) != -127 and float(msg_payload.split('/')[2]) != 111:
                        do = False
                        fake = _temperatura_interior
                        print("Para este punto me falta el count 0")
                    else:
                        do = True
                        fake = g['_temperatura_interior']
                        print("Para este punto me falta el count 1")
            print("Para este punto me faltan count")
            if float(msg_payload.split('/')[2]) > _temperatura_maxima:  
                _temperatura_maxima = float(msg_payload.split('/')[2])
                _date_maxima = datetime.datetime.now() + x
                print("Podre ser yo?")
            elif float(msg_payload.split('/')[2]) < _temperatura_minima:
                _temperatura_minima = float(msg_payload.split('/')[2])
                _date_minima = datetime.datetime.now() + x
                print(" o yo?")
            _date = datetime.datetime.now() + x 
            print("Para este punto aun me falta el count")
            if g['_temperatura_interior'] * 1.2 < _temperatura_interior or g['_temperatura_interior'] * 0.8 > _temperatura_interior:
                for con in db['fHistorial_' + msg_payload.split('/')[1]].find({},{'_id':0,'_contador':1, '_date':1}).sort('_date',-1).limit(1):
                    pass
                if do:
                    conta = (con['_contador'] + 1) if conta < 3 else 3 
                else:
                    conta = 0
            else:
                conta = 0
            print("Para este punto ya tengo todo")
        else:
            print("Es el primer msg en H")
            _temperatura_maxima = float(msg_payload.split('/')[2])
            _date_maxima = datetime.datetime.now()
            _temperatura_minima = float(msg_payload.split('/')[2])
            _date_minima = datetime.datetime.now()
            _date = datetime.datetime.now()
            conta = 0
            fake = _temperatura_interior
            if opcion == 30:
                _out_0 = False
                _out_1 = True
            else:
                _out_0 = bool(int(msg_payload.split('/')[4]))
                _out_1 = bool(int(msg_payload.split('/')[5]))
            print("Fue el primer msg\nTengo todo")

    dic = {
        'd_id': d_id,
        '_name': _name,
        '_setpoint': _setpoint,
        '_temperatura_interior': _temperatura_interior,
        '_temperatura_exterior': _temperatura_exterior,
        '_out_0': _out_0,
        '_out_1': _out_1,
        '_histeresis_high': _histeresis_high,
        '_histeresis_low': _histeresis_low,
        '_temperatura_maxima': _temperatura_maxima,
        '_date_maxima': _date_maxima,
        '_temperatura_minima': _temperatura_minima,
        '_date_minima': _date_minima,
        '_fake': fake,
        '_contador': conta,
        '_date': _date
    }
    historial.insert_one(dic)
    print(dic)

def trasformada(v_arr2, k_arr2):
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

def bucle():
    while True:
        print("Graficar Start")
        grafica()
        print("Graficar End")
        time.sleep(30)