from flask import *
from pymongo import MongoClient   

try:        
    print("Iniciando MongoDB...")
    mongo = MongoClient("mongodb+srv://monzav:mongodb057447@cluster0.qilrdwg.mongodb.net/?retryWrites=true&w=majority")
    db = mongo['Tempec_Cloud']                                                   
    enterprises = db['Enterprises']                                            
    historial = db['Historial']            
    print("MongoDB iniciado")                                  
except:
    print("No se pudo establecer conexion con MongoDB")  

app = Flask(__name__)
app.secret_key = "mmm123mmm321"

@app.route("/")
def login_page():
    return render_template("login_page.html")

@app.route("/user_login", methods=["POST", "GET"])
def autentication():
        if str(request.form['supa_user']) == 'on':
            if enterprises.count_documents({'e_id': str(request.form['u_id'])}) > 0:
                for e in enterprises.find({'e_id':str(request.form['i1'])}):
                    pass
            else:
                return render_template("not_found_id.html", id_a=str('u_id'))
        else:
            for e in enterprises.find({'e_id.':str(request.form['i1'])}):
                pass

if __name__ == '__main__':
    app.run(debug=True, port=4444)