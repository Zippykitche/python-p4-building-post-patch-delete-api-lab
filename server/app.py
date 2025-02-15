#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>', methods = ['GET', 'PATCH'])
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()

    if request.method == 'GET':
        return make_response ( bakery_serialized, 200  )
    
    elif request.method == 'PATCH':
        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))

            db.session.add(bakery)
            db.session.commit()

            response = make_response(
                bakery.to_dict(),
                200
            )

            return response


@app.route('/baked_goods', methods = ['GET', 'POST'])
def baked_goods():

    if request.method == 'GET':
        baked_goods = BakedGood.query.all()
        baked_goods_list = [baked_good.to_dict() for baked_good in baked_goods]
        response = make_response(
            baked_goods_list,
            200
        )

        return response
    
    elif request.method == 'POST':
        new_baked_goods = BakedGood(
            name=request.form.get("name"),
            price=request.form.get("price")
        )
        db.session.add(new_baked_goods)
        db.session.commit()

        response = make_response(
            new_baked_goods.to_dict(),
            201
        )

        return response
    
@app.route('/baked_goods/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def baked_goods_by_id(id):
    baked_goods_by_id = BakedGood.query.filter(BakedGood.id==id).first()

    if not baked_goods_by_id:
        return {"error": "Baked good not found"}, 404
    
    if request.method == 'GET':
       
        response = make_response(
            baked_goods_by_id.to_dict(),
            200
        )

        return response
    
    elif request.method == 'PATCH':
        for attr in request.form:
            setattr(baked_goods_by_id, attr, request.form.get(attr))

            db.session.add(baked_goods_by_id)
            db.session.commit()

            response = make_response(
                baked_goods_by_id.to_dict(),
                200
            )

            return response
        
    elif request.method == 'DELETE':
        db.session.delete(baked_goods_by_id)
        db. session.commit()

        response = make_response(
            {"message": "baked good deleted successfully"},
            200

        )

        return response
 

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

if __name__ == '__main__':
    app.run(port=5555, debug=True)