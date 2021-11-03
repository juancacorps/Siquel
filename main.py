from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect, CSRFError
from forms import Connection_forms
    
app = Flask(__name__)
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

    forms = Connection_forms()
    if forms.validate_on_submit():
        #execute_query(values)
        host = forms.host.data
        user = forms.host.data
        password =  forms.host.data
        s = translate(host,user,password)
        return redirect('traslate')
        return render_template('query', )
        
    context = {'forms': forms}

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
