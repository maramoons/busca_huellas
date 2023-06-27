from flask import Flask, request, redirect, url_for,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, UserMixin, login_required, login_user, current_user, logout_user
from twilio.rest import Client
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['SECRET_KEY']='Nomehackeenxfa'
db = SQLAlchemy(app)

class Animal_Encontrados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raza = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.String(50), nullable=False)
    tamanho = db.Column(db.String(50), nullable=False)
    ciudad = db.Column(db.String(140),nullable=False)
    barrio = db.Column(db.String(140),nullable=False)
    otrascaract = db.Column(db.String(240),nullable=False)
    telefono = db.Column(db.String(50),nullable=False)
    latitud = db.Column(db.Integer)
    longitud = db.Column(db.Integer)



class Animales_Perdidos(db.Model): # poner en mayusculas la primera letra`
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(255), nullable=False)
    raza = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(255), nullable=False)
    edad = db.Column(db.String(255), nullable=False)
    tamaño = db.Column(db.String(255), nullable=False)
    ciudad = db.Column(db.String(255), nullable=False)
    barrio = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.Integer)
    otras_caracteristicas = db.Column(db.String(255), nullable=False)
    latitud = db.Column(db.Integer)
    longitud = db.Column(db.Integer)



@app.route('/')
def index():
    animales_encontrados = Animal_Encontrados.query.all()
    diccionario_de_animales = {

        "animales":[]
    }
    for animal in animales_encontrados:
        diccionario_de_animales['animales'].append({
            'raza': animal.raza,
            'color':animal.color,
            'edad': animal.edad,
            'tamanho': animal.tamanho,
            'ciudad': animal.ciudad,
            'barrio':animal.barrio,
            'telefono': animal.telefono,
            'otrascaract': animal.otrascaract,
            'latitud':animal.latitud,
            'longtitud':animal.longitud})

    return render_template('index.html', animales_encontrados = json.dumps(diccionario_de_animales))






@app.route('/mascotasperdidas', methods=["POST", "GET"])
def form():
    if (request.method == "POST"):
        nombre = request.form['nombre']
        raza = request.form['raza']
        color = request.form['color']
        edad = request.form['edad']
        tamaño = request.form['tamaño']
        ciudad = request.form['ciudad']
        barrio = request.form['barrio']
        telefono = request.form['telefono']
        otras_caracteristicas = request.form['otras_caracteristicas']
        latitud = request.form['latitud']
        longitud = request.form['longitud']

        animal_perdido = Animales_Perdidos(nombre=nombre, raza=raza, color=color, edad=edad, tamaño=tamaño, ciudad=ciudad,barrio=barrio, telefono=telefono, otras_caracteristicas=otras_caracteristicas, latitud=latitud, longitud=longitud)

        db.session.add(animal_perdido)
        db.session.commit()

        animales_parecidos = Animal_Encontrados.query.filter(Animal_Encontrados.raza==animal_perdido.raza, Animal_Encontrados.color==animal_perdido.color).all()
        print(len(animales_parecidos))

        
        if animales_parecidos:
            account_sid = 'AC2736df3dbf65cf3450d6c44f1f55aeeb'
            auth_token = 'bc68581f30acf9b5068e8293dd26cbaa'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                from_='+14849699516',
                body='puto',
                to=f'+595{animal_perdido.telefono}'
            )
            return render_template('listamascotasperdidas.html', animales_parecidos = animales_parecidos)

        return "Datos ingresados exitosamente"

    else:
            MascoPerdi = Animales_Perdidos.query.all()

            return render_template('mascotasperdidas.html', mascotasPerdi = MascoPerdi)


@app.route('/mascotasencontradas', methods = ['GET', 'POST'])
def formulario():
    # todos_las_tareas_del_usuario = app.query.filter_by().first()
    if (request.method == 'POST'):
        raza = request.form['RazaAnimal']
        color = request.form['ColorAnimal']
        edad = request.form['edad']
        tamanho = request.form['tamanho']
        ciudad = request.form['CiudadEncontrado']
        barrio = request.form['BarrioEncontrado']
        otrascaract = request.form['CaractAnimalEncontr']
        telefono = request.form['TelefonoRescatista']
        latitud = request.form['latitud']
        longitud = request.form['longitud']

        perro_encontrado = Animal_Encontrados(raza=raza, color = color, edad = edad, tamanho=tamanho, ciudad=ciudad,barrio=barrio,otrascaract=otrascaract,telefono= telefono, latitud=latitud, longitud=longitud)
        

        db.session.add(perro_encontrado)
        db.session.commit()

        return "cargado a la db"
    else:
        MascoEnco = Animal_Encontrados.query.all()
        
        return render_template('mascotasencontradas.html', mascotasEnco = MascoEnco)


with app.app_context():
    db.create_all()


