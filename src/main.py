"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuario
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

def swapi_to_localhost(swapi_url):
    return swapi_url.replace("http://www.swapi.tech/api/","http://localhost:3000/")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/usuarios', methods=['GET'])
def handle_usuarios():
    usuarios = Usuario.query.all()
    print(usuarios)
    response = []
    for usuario in usuarios:
        response.append(usuario.serialize())
    print(response)
    return jsonify(response),200

@app.route('/usuarios/<int:usuario_id>/favoritos/<string:nature>', methods=['POST'])
def handle_users_favorite(user_id,nature):
    uid = request.json['uid']
    nuevo_favorito = FavoritoUsuario (
        usuario_id = usuario_id,
        url = f"http://swapi.tech/api/{nature}/{uid} "
    )
    db.session.add(nuevo_favorito)
    try:
        db.session.commit()
        return jsonify(nuevo_favorito.serialize()),201
    except Exception as error:
        db.session.rollback()
        return jsonify(error.args),500

@app.route('/people',methods=['GET'])
def handle_people():
    limit = request.args.get("limit", "10")
    page = requests.args.get("page",1)
    response = request.get(f'https://swapi.dev/api/people?page={page}&limit={limit}')
    print(response.status_code)
    response = response.json()
    response.update(
        previous = swapi_to_localhost(response['previous']) if response['previous'] else None,
        next = swapi_to_localhost(response['next']) if response['next'] else None
    )

    
    return jsonify([]),200

@app.route('/planets', methods=['GET'])
def handle_planets():
    response = request.get(f'https://swapi.dev/api/planets?page=1&limit=80') #Tiene la respusta de la solicitud de esa url
    response = request.json() #Devuelve un diccionario
    print(response['results'])
    return jsonify([]),200 # Muestra la respuesta en formato json

    #response_body = {
     #   "msg": "Hello, this is your GET /user response "
    #}

   # return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
