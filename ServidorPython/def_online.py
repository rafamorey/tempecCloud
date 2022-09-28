import mejoras
                                          
def obtener_user(ux):
    for h in mejoras.enterprises.aggregate([{'$match': {'users.devices.d_id': ux}},
                        {'$unwind':'$users'},
                        {'$match':{'users.devices.d_id': ux}},
                        {'$project': {'users.u_id':1, '_id':0}}
                        ]):
        f = h['users']
    return str(f).split("'")[3]

def tic_tac():
    for r in mejoras.db.list_collection_names():
        if r != 'Historial' and r != 'Enterprises' and r != 'devices_id':
            for g in mejoras.db['fHistorial_'+ r.split('_')[1]].aggregate([{'$group': {'_id':{}, 'fecha': {'$last':'$_date'}}}]):
                c = mejoras.datetime.now() - g['fecha']
                bol = True if c.days < 1 and c.seconds < 700 else False

                uu = obtener_user(r.split('_')[1])

                for j in mejoras.enterprises.aggregate([{'$match': {'users.u_id': uu}},
                            {'$project':{'_id':0, 'index': {'$indexOfArray': ["$users.u_id", uu]}}}]):
                    u = str(j['index'])

                for l in mejoras.enterprises.aggregate([{'$match': {'users.devices.d_id': r.split('_')[1]}},
                                    {'$unwind': '$users'},
                                    {'$match': {'users.u_id': uu}},
                                    {'$project':{'_id':0, 'index': {'$indexOfArray': ["$users.devices.d_id", r.split('_')[1]]}}}
                                    ]):
                    d = str(l['index'])

                mejoras.enterprises.update_one({'users.devices.d_id': str(r.split('_')[1])},{'$set': {
                                                f'users.{u}.devices.{d}.online' : bol,
                                                }})

def bucle_alive():
    while True:
        for tiempo_alive in range(1,6):
            print(f"{tiempo_alive} - 5 _Online")
            mejoras.time.sleep(1)
        tic_tac()
        print("Done !")

def imprimir_algo():
    print("FNWEQOIJWQOIEFNODNVQSUNBFUIQ;;oimfpqodifmnoqwnfvupqbnpiubLSFNUWRQEIBGIU")