from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from sqlalchemy import create_engine
from json import dumps
import sys
import logging
from decimal import *
import flask.json
import datetime

#Create a engine for connecting to SQLite3.
#Assuming potes.db is in your app root folder

app = Flask(__name__)
api = Api(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'potes.db')

db = SQLAlchemy(app)
ma = Marshmallow(app)

file_handler = logging.FileHandler('potes.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)
app.json_encoder = MyJSONEncoder


class Pote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True)
    limite = db.Column(db.Numeric(10,2))
    prioridade = db.Column(db.Integer)
    moeda = db.Column(db.String(3))
    saldo = db.Column(db.Numeric(10,2))

    def __init__(self, nome, limite, prioridade = 1, moeda = "R$", saldo = 0):
        self.nome = nome
        self.limite = limite
        self.prioridade = prioridade
        self.moeda = moeda
        self.saldo = saldo


class PoteSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'nome', 'limite', 'prioridade', 'moeda', 'saldo')


pote_schema = PoteSchema()
potes_schema = PoteSchema(many=True)


class Transaction(db.Model):
    CREATE = 0
    CREDIT = 1
    DEBIT = 2
    DELETE = 3

    id = db.Column(db.Integer, primary_key=True)
    pote_id = db.Column(db.Integer, db.ForeignKey(Pote.id), primary_key=True)
    # data = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    tipo = db.Column(db.Integer)
    valor = db.Column(db.Numeric(10,2))
    pote = db.relationship("Pote", foreign_keys="Transaction.pote_id")

    def __init__(self, pote_id, tipo, valor = 0.00):
        self.pote_id = pote_id
        self.tipo = tipo
        self.valor = valor


class TransactionSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'pote_id', 'data', 'tipo', 'valor',)

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)

@app.route("/potes/api/v1.0/potes", methods = ['GET'])
def get_potes_list():
    all_potes = Pote.query.all()
    result = potes_schema.dump(all_potes)
    return jsonify(result.data)


@app.route("/potes/api/v1.0/pote/<int:pote_id>", methods = ['GET'])
def get_pote(pote_id):
    pote = Pote.query.get(pote_id)
    result = pote_schema.jsonify(pote)
    return result


@app.route("/potes/api/v1.0/pote", methods = ['POST'])
def create_pote():
    """
    curl -v POST http://localhost:5000/potes/api/v1.0/pote -d '{"nome":"Poupança","limite":2000.22,"prioridade":1,"moeda":"R$","saldo":1500.54}' --header "Content-Type: application/json"
    """

    nome = request.json['nome']
    limite = request.json['limite']
    prioridade = request.json['prioridade']
    moeda = request.json['moeda']
    saldo = request.json['saldo']

    pote = Pote(nome, limite, prioridade, moeda, saldo)
    db.session.add(pote)
    db.session.commit()
    result = pote_schema.dump(pote).data

    # Save create transaction
    transaction = Transaction(result['id'], Transaction.CREATE, saldo)
    db.session.add(transaction)
    db.sessin.commit()
    return jsonify({'pote': result})


@app.route('/potes/api/v1.0/pote/<int:pote_id>', methods = ['PUT'])
def update_pote(pote_id):
    """
    UPDATE any field of a pote
    curl -X PUT http://localhost:5000/potes/api/v1.0/pote/1 -d '{"nome":"Coche","limite":2000.22,"prioridade":1,"moeda":"R$","saldo":1500.54}' --header "Content-Type: application/json"
    """
    pote = Pote.query.get(pote_id)

    nome = request.json['nome']
    limite = request.json['limite']
    prioridade = request.json['prioridade']
    moeda = request.json['moeda']
    # saldo = request.json['saldo']

    pote.nome = nome
    pote.limite = limite
    pote.prioridade = prioridade
    pote.moeda = moeda
    #pote.saldo = saldo

    db.session.commit()
    result = pote_schema.dump(pote).data
    return jsonify({'pote': result})


@app.route('/potes/api/v1.0/pote/credit/<int:pote_id>', methods = ['PUT'])
def credit(pote_id):
    """
    UPDATE pote to credit a value
    curl -X PUT http://localhost:5000/potes/api/v1.0/credit/1 -d '{"value":1500.54}' --header "Content-Type: application/json"
    """
    pote = Pote.query.get(pote_id)
    value = request.json['value']
    pote.saldo += round(Decimal(float(value)),2)
    db.session.commit()
    result = pote_schema.dump(pote).data

    # Save credit transaction   
    transaction = Transaction(result['id'], Transaction.CREDIT, value)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({'pote': result})


@app.route('/potes/api/v1.0/pote/debit/<int:pote_id>', methods = ['PUT'])
def debit(pote_id):
    """
    UPDATE a pote to debit a value
    curl -X PUT http://localhost:5000/potes/api/v1.0/debit/1 -d '{"value":1500.54}' --header "Content-Type: application/json"
    """
    pote = Pote.query.get(pote_id)
    value = request.json['value']
    pote.saldo -= round(Decimal(float(value)),2)
    db.session.commit()
    result = pote_schema.dump(pote).data

    # Save debit transaction   
    transaction = Transaction(result['id'], Transaction.DEBIT, value)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({'pote': result})

@app.route('/potes/api/v1.0/pote/delete/<int:pote_id>', methods = ['DELETE'])
def delete_pote(pote_id):
    '''
    DELETE implementation: deleting an existing pote
    curl -X DELETE http://localhost:5000/potes/api/v1.0/pote/delete/40
    '''
    pote = Pote.query.get(pote_id)
    db.session.delete(pote)
    db.session.commit()

    # Save debit transaction   
    transaction = Transaction(pote_id, Transaction.DELETE)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({'status':200})
 

if __name__ == '__main__':
     app.run()
