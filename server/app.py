#!/usr/bin/env python3
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        return make_response({ "message": "Welcome to the Super Hero page!" }, 200)

api.add_resource(Home, '/')

class Heroes(Resource):
    def get(self):
        hero_dicts = [hero.to_dict() for hero in Hero.query.all()]

        return make_response(
            jsonify(hero_dicts),
            200
        )
    
api.add_resource(Heroes, '/heroes')

class HeroById(Resource):
    def get(self, id):
        hero = Hero.query.filter(Hero.id == id).first()
        
        if not hero:
            return make_response({ "error": "Hero not found" }, 404)
        
        hero_dict = hero.to_dict(rules=('powers',))

        return make_response(
            jsonify(hero_dict),
            200
        )
    
api.add_resource(HeroById, '/heroes/<int:id>')

class Powers(Resource):
    def get(self):
        power_dicts = [power.to_dict() for power in Power.query.all()]

        return make_response(
            jsonify(power_dicts),
            200
        )
    
api.add_resource(Powers, '/powers')

class PowerById(Resource):
    def get(self, id):
        power = Power.query.filter(Power.id == id).first()
        
        if not power:
            return make_response({ "error": "Power not found" }, 404)
        
        power_dict = power.to_dict(rules=('heroes',))

        return make_response(
            jsonify(power_dict),
            200
        )
    
    def patch(self, id):
        power = Power.query.filter(Power.id == id).first()
        
        if not power:
            return make_response({ "error": "Power not found" }, 404)
        try:
            for attr in request.get_json():
                setattr(power, attr, request.get_json()[attr])

            db.session.add(power)
            db.session.commit()

        except:
            return make_response({ "error": "Invalid input"}, 403)

        power_dict = power.to_dict()

        return make_response(
            jsonify(power_dict),
            200
        )
    
api.add_resource(PowerById, '/powers/<int:id>')

class HeroPowers(Resource):
    def post(self):
        try:
            new_hero_power = HeroPower(
                strength=request.get_json()['strength'],
                hero_id=request.get_json()['hero_id'],
                power_id=request.get_json()['power_id']
            )

            db.session.add(new_hero_power)
            db.session.commit()

        except:
            return make_response({ "error": "Invalid input" }, 403)
        
        hero_power_dict = new_hero_power.hero.to_dict(rules=('powers', 'hero_powers'))

        return make_response(
            jsonify(hero_power_dict),
            201
        )
    
api.add_resource(HeroPowers, '/hero_powers')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
