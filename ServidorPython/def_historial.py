import mejoras

def tendencia(a):
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

def grafica():
    for r in mejoras.db.list_collection_names():
        if r != 'Historial' and r != 'Enterprises':
            for c in mejoras.enterprises.aggregate([{'$match': {'users.devices.d_id': {'$eq': r.split('_')[1]}}},
                            {'$unwind': '$users'},
                            {'$match' : {'users.devices.d_id': {'$eq': r.split('_')[1]}}},
                            {'$unwind': '$users.devices'},
                            {'$match' : {'users.devices.d_id': {'$eq': r.split('_')[1]}}},
                            {'$project': {'_id':0,  'alive': '$users.devices.online'}}]):

                if c['alive']:
                    if mejoras.db['fHistorial_' + r.split('_')[1]].count_documents({}) > 0:
                        v1_arr, v2_arr, k_arr , out0, out1 = [], [], [], [], []
                    
                        for g in mejoras.db['fHistorial_' + r.split('_')[1]].find({},{'_id':0}).sort('_date',-1).limit(5):
                            v1_arr.append(g['_inte'])
                            v2_arr.append(g['_exte'])
                            k_arr.append(g['_tipo'])
                            out0.append(g['_out_0'])
                            out1.append(g['_out_1'])

                        value_array = trasformada(v1_arr, k_arr)

                        valor = tendencia(value_array)
                        print(valor)
                        msg = 'aux/' + r.split('_')[1] + '/' + str(valor) + '/' + str(v2_arr[0]) + '/' + str(out0[0]) + '/' + str(out1[0])
                        # Hasta este punto tengo el msg con el valor que sera procesado con la ultima X (para saber de que hablo recordar al pizarron)
                        print("_Este es el msg = " + msg)

                        k = True if mejoras.db['fHistorial_' + r.split('_')[1]].count_documents({}) <= 0 else False

                        insertar_historial(k, r.split('_')[1], msg)
                    else:
                        print(f"El equipo {r.split('_')[1]} aun no tiene datos")
                    
                else:
                    print(f"El equipo {r.split('_')[1]} esta offline")

def insertar_historial(first_msg, opcion, msg_payload: str):
    conta = 0
    for z in mejoras.enterprises.aggregate([{'$match': {'users.devices.d_id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$unwind': '$users'},
                            {'$match' : {'users.devices.d_id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$unwind': '$users.devices'},
                            {'$match' : {'users.devices.d_id': {'$eq': msg_payload.split('/')[1]}}},
                            {'$project': {'_id':0, 'nombre': '$users.devices.d_name', 'sp': '$users.devices.setpoint', 'hmax': '$users.devices.histeresis_high', 'hmin': '$users.devices.histeresis_low'}}]):
           
        _name            = z['nombre']
        _setpoint        = z['sp']
        _histeresis_high = z['hmax']
        _histeresis_low  = z['hmin']

    d_id = msg_payload.split('/')[1]
    _temperatura_interior = float(msg_payload.split('/')[2])
    _temperatura_exterior = float(msg_payload.split('/')[3])
    print("Para este punto me faltan minimos, maximos, out's, count y fake")

    if first_msg:
        _temperatura_maxima = float(msg_payload.split('/')[2])
        _date_maxima = mejoras.datetime.datetime.now()
        _temperatura_minima = float(msg_payload.split('/')[2])
        _date_minima = mejoras.datetime.datetime.now()
        _date = mejoras.datetime.datetime.now()
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
        if mejoras.historial.count_documents({'d_id': d_id}) > 0:
            print("No es el primer msg en H")
            do = False
            for g in mejoras.historial.find({'d_id': d_id},{'_id':0,'_temperatura_maxima':1, '_temperatura_minima':1, '_temperatura_exterior':1, '_temperatura_interior':1, '_date_maxima':1, '_date_minima':1, '_fake':1, '_date':1}).sort('_date',-1).limit(1):
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
                    x = (g['_date'] + mejoras.datetime.timedelta(seconds=300)) - mejoras.datetime.datetime.now()    
                    # Para este punto ya tengo todo y voy a comparar
                    print("Para este punto ya tengo todo")
                else:
                    _out_0 = bool(int(msg_payload.split('/')[4]))
                    _out_1 = bool(int(msg_payload.split('/')[5]))
                    x = mejoras.datetime.timedelta(seconds=0)
                    print("Para este punto me falta el count y fake")
                    # Para este punto solo me falta count y fake
                    if float(msg_payload.split('/')[2]) != -127 and float(msg_payload.split('/')[2]) != 111:
                        do = False
                        fake = _temperatura_interior
                        print("Para este punto me falta el count 0")
                    else:
                        do = True
                        fake = g['_fake']
                        print("Para este punto me falta el count 1")
            print("Para este punto me faltan count")

            if float(msg_payload.split('/')[2]) > _temperatura_maxima and float(msg_payload.split('/')[2]) != -127:  
                _temperatura_maxima = float(msg_payload.split('/')[2])
                _date_maxima = mejoras.datetime.datetime.now() + x

            elif float(msg_payload.split('/')[2]) < _temperatura_minima and float(msg_payload.split('/')[2]) != -127:
                _temperatura_minima = float(msg_payload.split('/')[2])
                _date_minima = mejoras.datetime.datetime.now() + x

            _date = mejoras.datetime.datetime.now() + x

            print("Para este punto aun me falta el count")

            if g['_temperatura_interior'] * 1.2 < _temperatura_interior or g['_temperatura_interior'] * 0.8 > _temperatura_interior:
                for con in mejoras.db['Historial'].find({'d_id': msg_payload.split('/')[1]},{'_id':0,'_contador':1, '_date':1}).sort('_date',-1).limit(1):
                    pass
                if do:
                    conta = (con['_contador'] + 1) if con['_contador'] < 3 else 3 
                else:
                    conta = 0
            else:
                conta = 0
            print(conta)
            print("Para este punto ya tengo todo")
        else:
            print("Es el primer msg en H")
            _temperatura_maxima = float(msg_payload.split('/')[2])
            _date_maxima = mejoras.datetime.datetime.now()
            _temperatura_minima = float(msg_payload.split('/')[2])
            _date_minima = mejoras.datetime.datetime.now()
            _date = mejoras.datetime.datetime.now()
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
    mejoras.historial.insert_one(dic)
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
        grafica()
        for tiempo_grafica in range(1,31):
            print(f"{tiempo_grafica} - 30 Historial")
            mejoras.time.sleep(1)