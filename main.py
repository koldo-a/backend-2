from flask import Flask, request, jsonify
from flask_cors import CORS
import os 
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['MYSQL_URL']
CORS(app)
db = SQLAlchemy(app)

class User(db.Model):
    idusers = db.Column(db.Integer, primary_key=True)
    email_users = db.Column(db.String(100), unique=True, nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    itemiduser = db.Column(db.Integer, db.ForeignKey('user.idusers'), nullable=False)
    user = db.relationship('User', backref=db.backref('items', lazy=True))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    
    # Verifica si el usuario ya está registrado
    user = User.query.filter_by(email_users=email).first()
    
    if user is not None:
        return jsonify({'message': 'El usuario ya está registrado'}), 400
    
    # Inserta el nuevo usuario en la base de datos
    new_user = User(email_users=email)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'Registro exitoso'}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    
    # Verifica si el usuario existe en la base de datos
    user = User.query.filter_by(email_users=email).first()
    if user is None:
        unsuccess_message = f'Usuario con el email: {email} no se ha encontrado'
        return jsonify({'message': unsuccess_message}), 404
    else: 
        idusers = user.idusers
        success_message = f'Inicio de sesión exitoso para el usuario con id: {idusers} y el email:{email}'
        # Retornar el mensaje de éxito junto con el idusers en la respuesta JSON
        return jsonify({'message': success_message, 'idusers': idusers}), 200

# Resto del código para las demás rutas y operaciones CRUD

if __name__ == '__main__':
    app.run()
