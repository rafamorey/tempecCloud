from array import array
from datetime import date, datetime, timedelta
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


for g in historial.find({'d_id': 'AAAA'},{'_id':0,'_temperatura_maxima':1, '_temperatura_minima':1, '_temperatura_exterior':1, '_temperatura_interior':1, '_date_maxima':1, '_date_minima':1, '_date':1}).sort('_date',-1).limit(1):
            _temperatura_maxima = g['_temperatura_maxima']
            _date_maxima = g['_date_maxima']
            _temperatura_minima = g['_temperatura_minima']
            _date_minima = g['_date_minima']
            print(g)
