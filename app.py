import flask
from flask import request, jsonify
import pyrebase
from scipy import spatial
from array import *
import json
app = flask.Flask(__name__)
config = {
"apiKey": "AIzaSyDHAqA4SINy1fAoNJ6xn3MiJEh5ZO-pR4U",
"authDomain": "emergency-b0afc.firebaseapp.com/",
"databaseURL": "https://emergency-b0afc.firebaseio.com/",
"storageBucket": "emergency-b0afc.appspot.com"
}
app.config["DEBUG"] = True
firebase = pyrebase.initialize_app(config)
db = firebase.database()



@app.route('/emergency', methods=['POST','GET'])
def hello():
    lists = []
    kiyo = {}
    x = request.args['x']
    y = request.args['y']
    imei = request.args['imei']
    uuid = request.args['uuid']
    db.child('requests').child(uuid).child('x').set(x)
    db.child('requests').child(uuid).child('y').set(y)
    db.child('requests').child(uuid).child('imei').set(imei)
    num = [(float(x),float(y))]
    print(num)


    all_users = db.child("Available").get()

    for x in all_users.each():
        listo = []
        strin = x.val()
        stri = x.key()
        kiyo[strin] = stri

        strin = strin.split(',')
        for i in strin:
             listo.append(float(i))
        tupl = tuple(listo)

        lists.append(tupl)


    tree = spatial.KDTree(lists)

    x = (list(tree.query(num)))
    print(x)
    num1 = tuple(x[1].tolist())[0]
    co_num = lists[num1]
    to =  str(co_num[0])+','+str(co_num[1])
    out = { 'name' : kiyo[to],
            'x' : to.split(',')[0],
            'y': to.split(',')[1]
            }
    jso = json.dumps(out)
    print(out)
    return jso
app.run(port=7890)
