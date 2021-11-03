from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect, CSRFError
from werkzeug.wrappers import request
from forms import Connection_forms
from flask_mysqldb import MySQL

    
app = Flask(__name__)

# mysql connection



SECRET_KEY = 'super_secreto'
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    '''Esta parte es el home de nuestra aplicacion, donde estara el navbar para el servidor
        para redirigir a la documentacion y conexion (Utilizar url_for)
        por favor meterle un diseño increible con html y css
        para dar una buena impresion del proyecto, es opcional si la persona acargo de esto
        quiere apoyar en diseño a las demas rutas.
        Tambien tiene que tomar en cuanta la creacion de las rutas y los errores
        404 y 500'''
    return render_template('base.html')


@app.route('/conections', methods=['GET', 'POST'])
def conection():
    '''Crear los campos para hacer la conexion con la base de datos
       *Campos obligatorios: Gestor de base de datos, host, user, password
       Tambien escribir el codigo para manejar condicionales de gestores:
       Es decir cuando seleccione Mysql hacer la conexion para mandarla a la funcion
       query'''

    formas= Connection_forms()

    
    host= formas.host.data
    user= formas.user.data
    passw=formas.password.data
    nameDB=formas.name_db.data
    if formas.validate_on_submit():


        app.config['MYSQL_HOST'] = host
        app.config['MYSQL_PORT'] = 3306
        app.config['MYSQL_USER'] = user
        app.config['MYSQL_PASSWORD'] = passw
        app.config['MYSQL_USE_UNICODE'] =  True
        app.config['MYSQL_CONNECT_TIMEOUT'] = 10
        app.config['MYSQL_DATABASE_SOCKET'] = None
        app.config['MYSQL_UNIX_SOCKET'] = None
        app.config['MYSQL_CHARSET'] =  'utf8'
        app.config['MYSQL_SQL_MODE'] =  None
        app.config['MYSQL_CURSORCLASS'] =  None
        app.config['MYSQL_READ_DEFAULT_FILE'] =  None
        app.config['MYSQL_DB'] = nameDB
        mysql =MySQL(app)

        cur = mysql.connection.cursor()
        if cur:
        
          return redirect(url_for('traslate'))
        else :
            context = {'forms': formas}
            return render_template('conection.html', **context)

    context = {'forms': formas}
    return render_template('conection.html', **context)

    

   



    
    
@app.route('/traslate')
def traslate():
    '''Codigo para ejecutar la query
        Basicamente seria de tener un cuadro donde la persona
        Escriba su codigo en Español, usar un try y except para manejar en
        los errores de sintaxis y con la funcion replace sustituir lo de español
        a ingles para ejecutar la query.
        La persona acargo de la ruta conection te tiene que pasar
        los datos de la conexion, solo para recibirlo y ejecutarlo'''
    return render_template('execute_query.html')

if __name__ == '__main__':
    app.run(debug=True, host = 'localhost')