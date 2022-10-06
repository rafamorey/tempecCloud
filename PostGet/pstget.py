from flask import *
import json
import pymongo 
import paho.mqtt.client as mqtt  

mongo = pymongo.MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
db = mongo['Tempec_Cloud']
enterprises = db['Enterprises']

monzav = mqtt.Client()  
monzav.connect("test.mosquitto.org", 1883, 60) 

# monzav.publish('Tempec/Devices','Hola Germancito')

app = Flask(__name__)

@app.route('/login', methods=['POST','GET'])
def consult_user():
    dic = json.loads(request.data.decode())
    if enterprises.count_documents({'devices.name': dic['name']}) > 0:
        for x in enterprises.aggregate([{'$match': {'devices.name': {'$eq': dic['name']}}},
                            {'$unwind': '$devices'},
                            {'$match' : {'devices.name': {'$eq': dic['name']}}},
                            {'$project': {
                                'id': '$devices.id', 
                                'name': '$devices.name',
                                'setpoint': '$devices.setpoint',
                                'tempInt': '$devices.tempInt',
                                'tempExt': '$devices.tempExt',
                                'hisH': '$devices.hisH',
                                'hisL': '$devices.hisL',
                                'tempMax': '$devices.tempMax',
                                'dateMax': '$devices.dateMax',
                                'tempMin': '$devices.tempMin',
                                'dateMin': '$devices.dateMin',
                                'alarmaH': '$devices.alarmaH',
                                'alarmaL': '$devices.alarmaL',
                                'grados': '$devices.grados',
                                'online': '$devices.online',
                                'last_update': '$devices.last_update'
                                }}
                            ]):
            return x
    else:
        return {'message':'Not Found a Device'}

if __name__ == "__main__":
    app.run(debug=False)