import json
from os import environ
from flask import request

from app import app
from models import db, Hero, Power, HeroPower

class TestApp:
    '''Flask application in app.py'''

    def test_gets_heroes(self):
        '''retrieves heroes with GET requests to /heroes.'''

        with app.app_context():
            superman = Hero(name="Clark Kent", super_name="Superman")
            db.session.add(superman)
            db.session.commit()

            response = app.test_client().get('/heroes').json
            heroes = Hero.query.all()
            assert [hero['id'] for hero in response] == [hero.id for hero in heroes]
            assert [hero['name'] for hero in response] == [hero.name for hero in heroes]
            assert [hero['super_name'] for hero in response] == [hero.super_name for hero in heroes]

    def test_gets_hero_by_id(self):
        '''retrieves one hero using its ID with GET request to /heroes/<int:id>.'''

        with app.app_context():
            batman = Hero(name="Bruce Wayne", super_name="Batman")
            db.session.add(batman)
            db.session.commit()

            response = app.test_client().get(f'/heroes/{batman.id}').json
            assert response['name'] == batman.name
            assert response['super_name'] == batman.super_name

    def test_gets_powers(self):
        '''retrieves powers with GET requests to /powers.'''

        with app.app_context():
            invisibility = Power(name="invisibility", description="makes the wielder impossible to see")
            db.session.add(invisibility)
            db.session.commit()

            response = app.test_client().get('/powers').json
            powers = Power.query.all()
            assert [power['id'] for power in response] == [power.id for power in powers]
            assert [power['name'] for power in response] == [power.name for power in powers]
            assert [power['description'] for power in response] == [power.description for power in powers]

    def test_gets_power_by_id(self):
        '''retrieves one power using its ID with GET request to /powers/<int:id>.'''

        with app.app_context():
            laser_vision = Power(name="laser vision", description="allows the wielder to shoot powerful beams from their eyes")
            db.session.add(laser_vision)
            db.session.commit()

            response = app.test_client().get(f'/powers/{laser_vision.id}').json
            assert response['name'] == laser_vision.name
            assert response['description'] == laser_vision.description

    def test_patches_power_by_id(self):
        '''updates one power using its ID and JSON input for its fields with a PATCH request to /powers/<int:id>.'''

        with app.app_context():
            supergenius = Power(name="supergenius", description="allows the wielder to solve complex problems in an instant")
            db.session.add(supergenius)
            db.session.commit()

            response = app.test_client().patch(
                f'/powers/{supergenius.id}',
                json={
                    'name': 'super smarts',
                    'description': 'allows the wielder to be very smart',
            }).json

            super_smarts = Power.query.filter(Power.id == supergenius.id).first()

            assert response['name'] == 'super smarts'
            assert response['description'] == 'allows the wielder to be very smart'
            assert super_smarts.name == 'super smarts'
            assert super_smarts.description == 'allows the wielder to be very smart'

    def test_validates_power_description(self):
        '''returns an error message if a PATCH request to /powers/<int:id> contains a "description" value that is not a string of 20 or more characters.'''

        with app.app_context():

            supergenius = Power(name="supergenius", description="allows the wielder to solve complex problems in an instant")
            db.session.add(supergenius)
            db.session.commit()

            response = app.test_client().patch(
                f'/powers/{supergenius.id}',
                json={
                    'description': '',
            }).json

            assert response['error']

    def test_creates_hero_power(self):
        '''creates one hero_power using a strength, a hero_id, and a power_id with a POST request to /hero_powers.'''

        with app.app_context():

            hero = Hero(name="John Hero", super_name="Hero Man")
            power = Power(name="nothing", description="allows the wielder to do nothing of note")
            db.session.add_all([hero, power])
            db.session.commit()

            response = app.test_client().post(
                'hero_powers',
                json={
                    'strength': 'Weak',
                    'hero_id': hero.id,
                    'power_id': power.id,
                }
            ).json

            assert response['name'] == hero.name
            assert response['super_name'] == hero.super_name
            assert response['hero_powers'][0]['strength'] == 'Weak'
            assert response['hero_powers'][0]['hero_id'] == hero.id
            assert response['hero_powers'][0]['power_id'] == power.id
            assert hero.super_name == hero.super_name
            assert hero.hero_powers[0].strength == 'Weak'
            assert hero.hero_powers[0].hero_id == hero.id
            assert hero.hero_powers[0].power_id == power.id

    def test_validates_hero_power_strength(self):
        '''returns an error message if a POST request to /hero_powers contains a "strength" value other than "Strong", "Weak", or "Average".'''

        with app.app_context():

            hero = Hero(name="John Hero", super_name="Hero Man")
            power = Power(name="nothing", description="allows the wielder to do nothing of note")
            db.session.add_all([hero, power])
            db.session.commit()

            response = app.test_client().post(
                'hero_powers',
                json={
                    'strength': 'Cheese',
                    'hero_id': hero.id,
                    'power_id': power.id,
                }
            ).json

            assert response['error']