from array import array
import datetime
from pymongo import MongoClient                                                      
import time                                      

mongo = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
db = mongo['Tempec_Cloud']                                                   
enterprises = db['Enterprises']     
historial = db['Historial']  

def tendencia(a:array):
    tendencia = 0
    qwer = 0
    print("paso 1 = " + str(a))

    a = [ele for ele in a if ele > 0] 
    print("paso 2 = " + str(a))

    if len(a) < 1:
        print("paso 3.1 = ERROR -127")
        qwer = 'error -127'
    elif len(a) == 1:
        qwer = a
        print("paso 3.2 = " + str(a))
    else:
        print("paso 3.3 = " + str(a))
        for ii in range(2):
            print(f"if {max(a)} > {min(a) * 1.2}")
            if max(a) > min(a) * 1.2:
                a.remove(max(a))
                a.remove(min(a))
            print(f"paso 4.{ii+1} = " + str(a))

        if len(a) < 1:
            qwer = 'error acknowlage'
            print("paso 5.1 = ERROR ACKNOWLAGE")
        elif len(a) == 1:
            qwer = a
            print("paso 5.2 = " + str(a))
        else:
            print("paso 5.3 = " + str(a))
            for i in range(0, len(a)-1): 
                if a[i] > a[i+1]:
                    tendencia+=1
                elif a[i] < a[i+1]:
                    tendencia-=1
            suma = round(sum(a)/len(a),2)
            print("Tendencia = " + str(tendencia))
            if tendencia > 1:
                qwer = max(a)
                print("paso 6.1 = " + str(max(a)))
            elif tendencia < -1:
                qwer = min(a)
                print("paso 6.2 = " + str(min(a)))
            else:
                qwer = suma
                print("paso 6.3 = " + str(suma))    
    print("return a")
    print(qwer)
    return qwer

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

                    k = True if db['fHistorial_' + r.split('_')[1]].count_documents({'d_id': r.split('_')[1]}) <= 0 else False
                    insertar_historial(k, r.split('_')[1], msg)
                    
                else:
                    print(f"El equipo {r.split('_')[1]} esta offline")

def insertar_historial(primer, opcion, msg_payload):
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
    _out_0 = bool(int(msg_payload.split('/')[4]))
    _out_1 = bool(int(msg_payload.split('/')[5]))
    print("paso 1 Insertar Historial")
    if primer:
        print("primer")
        _temperatura_maxima = float(msg_payload.split('/')[2])
        _date_maxima = datetime.datetime.now()
        _temperatura_minima = float(msg_payload.split('/')[2])
        _date_minima = datetime.datetime.now()
        _date = datetime.datetime.now()
    else:
        print("No primer")
        for g in historial.find({'d_id': d_id},{'_id':0,'_temperatura_maxima':1, '_temperatura_minima':1, '_temperatura_exterior':1, '_temperatura_interior':1, '_date_maxima':1, '_date_minima':1, '_date':1}).sort('_date',-1).limit(1):
                _temperatura_maxima = g['_temperatura_maxima']
                _date_maxima = g['_date_maxima']
                _temperatura_minima = g['_temperatura_minima']
                _date_minima = g['_date_minima']
                _date = g['_date'] + datetime.timedelta(seconds=300)

                if float(msg_payload.split('/')[2]) > _temperatura_maxima:  
                    _temperatura_maxima = float(msg_payload.split('/')[2])
                    _date_maxima += datetime.timedelta(seconds=300)

                elif float(msg_payload.split('/')[2]) < _temperatura_minima:
                    _temperatura_minima = float(msg_payload.split('/')[2])
                    _date_minima += datetime.timedelta(seconds=300)

        if opcion != 30:  
            _date = datetime.datetime.now()
    print("paso 2 Inser H")
    print(d_id)
    print(_name)
    print(_setpoint)
    print(_temperatura_interior)
    print(_temperatura_exterior)
    print(_out_0)
    print(_out_1)
    print(_histeresis_high)
    print(_histeresis_low)
    print(_temperatura_maxima)
    print(_date_maxima)
    print(_temperatura_minima)
    print(_date_minima)
    print(_date)
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
        '_date': _date
    }
    # historial.insert_one(dic)
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