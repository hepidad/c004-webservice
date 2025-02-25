from flask import Flask, jsonify
from peewee import *
from flask_restful import Resource, Api, reqparse 

app = Flask(__name__)
api = Api(app)

db = SqliteDatabase('carsweb.db')

class BaseModel(Model):
    class Meta:
        database = db

class TBCarsWeb(BaseModel):
    carname = TextField()
    carbrand = TextField() 
    carmodel = TextField()
    carprice = TextField()

def create_tables():
    with db:
        db.create_tables([TBCarsWeb])

@app.route('/')
def masukkeindeks():
    return "Server Ready"

@app.route('/read')
def readdata():
    rows = TBCarsWeb.select()    
    datas=[]

    for row in rows:
        datas.append({
            'id':row.id,
            'carname':row.carname,
            'carbrand':row.carbrand,
            'carmodel':row.carmodel,
            'carprice':row.carprice
        })
    return jsonify(datas)

class CAR(Resource):
    def get(self):
        rows = TBCarsWeb.select()    
        datas=[]

        for row in rows:
            datas.append({
            'id':row.id,
            'carname':row.carname,
            'carbrand':row.carbrand,
            'carmodel':row.carmodel,
            'carprice':row.carprice
        })
        return jsonify(datas)

    def post(self):
        parserData = reqparse.RequestParser()
        parserData.add_argument('carname')
        parserData.add_argument('carbrand')
        parserData.add_argument('carmodel')
        parserData.add_argument('carprice')

        parserAmbilData = parserData.parse_args()

        fName = parserAmbilData.get('carname')
        fBrand = parserAmbilData.get('carbrand')
        fModel = parserAmbilData.get('carmodel')
        fPrice = parserAmbilData.get('carprice')

        car_simpan = TBCarsWeb.create(
            carname = fName,
            carbrand = fBrand, 
            carmodel = fModel,
            carprice = fPrice
            )

        rows = TBCarsWeb.select()    
        datas=[]
        for row in rows:
            datas.append({
                'id':row.id,
                'carname':row.carname,
                'carbrand':row.carbrand,
                'carmodel':row.carmodel,
                'carprice':row.carprice
            })
        return jsonify(datas)

    def delete(self):
        parserData = reqparse.RequestParser()
        parserData.add_argument('carname')

        parserAmbilData = parserData.parse_args()

        fName = parserAmbilData.get('carname') 

        car_delete = TBCarsWeb.delete().where(TBCarsWeb.carname==fName)
        car_delete.execute()

        rows = TBCarsWeb.select()    
        datas=[]
        for row in rows:
            datas.append({
                'id':row.id,
                'carname':row.carname,
                'carbrand':row.carbrand,
                'carmodel':row.carmodel,
                'carprice':row.carprice
            })
        return jsonify(datas)

api.add_resource(CAR, '/cars/', endpoint="cars/")

if __name__ == '__main__':
    create_tables()
    app.run(
        host = '0.0.0.0',
        debug = 'True',
        port=5012
        )