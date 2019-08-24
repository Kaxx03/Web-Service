from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
n = 5
tipo_medicion = {'Sensor' : 'DHT11', 'Variable': 'Humedad Aire', 'Unidades' : '%'}

mediciones = [
    {'fecha': '2019-08-17 12:24:00', **tipo_medicion, 'Valor': 0.5},
    {'fecha': '2019-08-18 01:10:00', **tipo_medicion, 'Valor': 0.36},
    {'fecha': '2019-08-19 03:13:00', **tipo_medicion, 'Valor': 0.6},
    {'fecha': '2019-08-20 18:45:00', **tipo_medicion, 'Valor': 0.32},
    {'fecha': '2019-08-21 23:16:00', **tipo_medicion, 'Valor': 0.26},
]

@app.route("/")
def get():
    return tipo_medicion

@app.route("/mediciones", methods=['GET'])
def getAll():
    return jsonify(mediciones)

@app.route("/mediciones/mayorOtro/<float:valor>", methods=['GET'])
def getMayorOtro(valor):
    mayores = []
    for medicion in mediciones:
        if(valor <= medicion['Valor']):
            mayores.append(medicion)
    return jsonify(mayores)

@app.route("/mediciones/mayorPorcentaje/<float:valor>", methods=['GET'])
def getMayores(valor):
    
    may = 0
    aux = []
    aux2 = 0    
    i = 0
    mayores = []
    for medicion in mediciones:
        if(may < medicion['Valor']):
            may = medicion['Valor']
            aux = medicion
    mayores.append(aux)
    """while i < range(mediciones):
        for medicion in mediciones:
            if(may < medicion['Valor']):
                aux2 = medicion['Valor']
        for medicion in mediciones:
            if(aux2 == medicion['Valor']):
                mayores.append(medicion)
        may = aux['Valor']
        aux = None"""
    return jsonify(mayores)

@app.route("/mediciones/ordenOtroVec/<float:valor>")
def getByOrdOtroVec(valor):
    x = 1/n
    porc = x
    vec = []
    vecP = []
    vecMay = []
    for medicion in mediciones:
        vec.append(medicion['Valor'])
    for i in range(1,len(vec)):
        for j in range(0,len(vec)-i):
            if(vec[j+1] > vec[j]):
                aux=vec[j];
                vec[j]=vec[j+1];
                vec[j+1]=aux;
    for i in vec:
        if(porc <= valor + 0.001):
            vecP.append(i)
            porc = porc + x
    for i in vecP:
        for medicion in mediciones:
            if(i == medicion['Valor']):
                vecMay.append(medicion)
        medicion = None
    #for medicion in mediciones:
    #    if(valor == medicion['Valor']):
    #        x = medicion
    return jsonify(vecMay)

@app.route("/mediciones", methods=['POST'])
def postOne():
    global n
    n = 5
    now = datetime.now()
    body = request.json
    body['fecha'] = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    mediciones.append({**body, **tipo_medicion})
    n += 1
    return jsonify(mediciones)

app.run()