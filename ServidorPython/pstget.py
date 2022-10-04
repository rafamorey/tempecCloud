from flask import *
import pymongo
import servidor_python

# Conexion MongoDB
mongo = pymongo.MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
db = mongo['Tempec_Cloud']
enterprise = db['Enterprises']
devices = db['devices_id']
# # #

app = Flask(__name__)

@app.route('/login', methods=['POST','GET'])
def consult_user():
    if enterprise.count_documents({'devices.name': str(request.headers.get('name'))}) > 0:
        servidor_python.monzav.publish('Server/Devices','Hola Gerancito')
        return enterprise.find_one({'devices.name': str(request.headers.get('name'))})
    else:
        return {'message':'Not Found'}

@app.route('/login1', methods=['GET','POST'])
def usrC():
    return {'message':'A ver que hago'}

if __name__ == "__main__":
    app.run(debug=False)