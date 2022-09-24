from array import array
from datetime import datetime
from operator import le
from re import A
from pymongo import MongoClient                 
import paho.mqtt.client as mqtt                   
import paho.mqtt.publish as publish              
import logging                               
import time                                      


mongo = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")

db = mongo['Tempec_Cloud']                                                   
enterprises = db['Enterprises']                                            
historial = db['Historial']  

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


def tendencia(a : array):
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
    
    return qwer

# q = [15.5, 15.7, 16.5, 17.5, 18.1]
# w = [18.1, 17.5, 16.5, 15.7, 15.5]
# e = [15.5, 16.7, 13.5, 15.5, 14.4]
# r = [55.6, 15.6, 16.5, 34.5, 15.0]
# t = [-127, 16.6, -127, -127, -127]
# y = [-127, -127, -127, -127, -127]
# u = [57.5, 62.2, 16.6, 67.8, 66.6]

for r in db.list_collection_names():
        if r != 'Historial' and r != 'Enterprises':
            for x in enterprises.aggregate([{'$match': {'users.devices.d_id': {'$eq': r.split('_')[1]}}},
                            {'$unwind': '$users'},
                            {'$match' : {'users.devices.d_id': {'$eq': r.split('_')[1]}}},
                            {'$unwind': '$users.devices'},
                            {'$match' : {'users.devices.d_id': {'$eq': r.split('_')[1]}}},
                            {'$project': {'_id':0,  'alive': '$users.devices.online'}}]):

                if x['alive']:
                    v_arr, k_arr = [], []
                
                    for g in db['fHistorial_' + r.split('_')[1]].find({},{'_id':0}).sort('_date',-1).limit(5):
                        v_arr.append(g['_valo'])
                        k_arr.append(g['_tipo'])
                    print(v_arr)
                    print(k_arr)

                    value_array = trasformada(v_arr, k_arr)

                    valor = tendencia(value_array)

                    print(valor)
                    
                else:
                    print("\n")
                    print(f"El equipo {r.split('_')[1]} esta offline")