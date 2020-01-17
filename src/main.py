"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db
from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/person', methods=['GET','POST'])
def handle_query():
    if request.method == 'GET':
        people_query = Person.query.all()
        all_people = list(map(lambda x: x.serialize(), people_query))
        return jsonify(all_people), 200
    if request.method =='POST':

        body = request.get_json()
        user1 = Person(username=body.get('username'), email=body.get('email'),address=body.get('address'),full_name=body.get('full_name'),phone=body.get('phone'))
        db.session.add(user1)
        db.session.commit()
        return jsonify(user1.id), 200

@app.route('/person/<int:id>', methods=['GET','PUT','DELETE'])
def handle_person(person_id):
    if request.method == 'GET':
        user1 = Person.query.get(person_id)
        return jsonify(all_people), 200

    if request.method == 'PUT':
        
        if user1 is None:
            raise APIException('User not found', status_code=404)

    if "username" in body:
        user1.username = body["username"]
    if "email" in body:
        user1.email = body["email"]
    if "phone" in body:
        user1.email = body["phone"]
    if "full_name" in body:
        user1.email = body["full_name"]
    if "address" in body:
        user1.email = body["address"]
    db.session.commit()
    
    if request.method =='DELETE':
        user1 = Person.query.get(person_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()
    return jsonify(user1), 200

@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
