from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pamejuly@localhost:3306/apiflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bdd = SQLAlchemy(app)
ma = Marshmallow(app)

# Este es el modelo contacto
class Contact(bdd.Model):
    __tablename__ = 'Contact'

    id = bdd.Column(bdd.Integer, primary_key=True, autoincrement=True)
    nombre = bdd.Column(bdd.String(120), nullable=False)
    apellido = bdd.Column(bdd.String(120), nullable=False)
    telefono = bdd.Column(bdd.String(15), nullable=False)
    correo = bdd.Column(bdd.String(120))
    favorito = bdd.Column(bdd.Boolean, default=False)

    def __init__(self, nombre, apellido, telefono, correo=None, favorito=False):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo
        self.favorito = favorito

class ContactSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Contact
        load_instance = True

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)

# Definir el endpoint para crear un nuevo contacto
@app.route('/contacto', methods=['POST'])
def agregar_contacto():
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    telefono = request.json['telefono']
    correo = request.json.get('correo')  # Para hacer que sea opcional
    favorito = request.json.get('favorito', False)  # El contacto favorito inicia en false o sea que no es favorito

    new_contact = Contact(nombre=nombre, apellido=apellido, telefono=telefono, correo=correo, favorito=favorito)
    bdd.session.add(new_contact)
    bdd.session.commit()

    return contact_schema.jsonify(new_contact), 201

if __name__ == '__main__':
    app.run(debug=True)