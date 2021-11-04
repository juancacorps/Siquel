from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect, CSRFError
from werkzeug.wrappers import request
from forms import Connection_forms, QueryFormExecute
from flask_mysqldb import MySQL
from configurate import config
from deep_translator import GoogleTranslator

    
app = config()
mysql = MySQL(app)
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
        try:
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
            cur = mysql.connection.cursor()
            return redirect(url_for('traslate'))
        except Exception as e:
            e = str(e).replace('(','').replace(')','').replace('using password: YES','').split(',')
            translated = GoogleTranslator(source='auto', target='es').translate(e[1])
            flash(translated)
            context = {'forms': formas}
            return render_template('conection.html', **context)


    context = {'forms': formas}
 
    return render_template('conection.html', **context)

    

   
@app.route('/traslate', methods=['POST', 'GET'])
def traslate():
    trans = QueryFormExecute()
    sp_sql = trans.esp_sql.data
    translate = trans.translate.data
    context = {'trans_form': trans}


    if trans.validate_on_submit():
        sql_es = str(trans.esp_sql.data).upper()
        reservado = ["SELECT","FROM", "CREATE", "TABLE",
                    "UPDATE", "INSERT", "SET", "INTO", "VALUES", "BETWEEN",
                     "IN", "AND", "OR", "NOT", "PRIMARY", "KEY", "DELETE", "DROP",
                     "UNIQUE", "DEFAULT", "CASE", "FOREIGN", "GROUP", "BY", "MIN",
                     "MAX", "SUM", "AVG", "OFFSET", "WHERE", "NULL", "BEGIN", ]
        x = str(sql_es).upper().split()
        
        
        for i in x:
            try:
                ingles = GoogleTranslator(source='auto', target='en').translate(i)
                print(ingles)
                if ingles in reservado:
                    sql_es = sql_es.replace(i,ingles) 
                else:
                    sql_es = sql_es.replace("SELECCIONAR" or "seleccionar", "SELECT") 
                    sql_es = sql_es.replace("DENTRO" or "dentro", "INTO") 
                    sql_es = sql_es.replace("VALORES" or "valores", "VALUES")
                    sql_es = sql_es.replace("ELIMINAR" or "eliminar", "DELETE") 
                    sql_es = sql_es.replace("DONFROM" or "donfrom", "WHERE")
                    sql_es = sql_es.replace("FROMLETE"or "fromlete", "DELETE") 
                    sql_es = sql_es.replace("ACTUALIZAR"or "actualizar", "UPDATE") 
            
                         
            except:
                pass

        
        
        sql_es = sql_es.lower()
        print(sql_es)

        try:
            if "delete" in sql_es:
                print("Siuuuuuuuu")
                cur = mysql.connection.cursor()
                print(cur)
                cur.execute(sql_es)
                mysql.connection.commit()
                trans.translate.data = sql_es
                flash("Se ejecutó exitosamente")
            elif "insert" in sql_es:
                print("Siuuuuuuuu")
                cur = mysql.connection.cursor()
                print(cur)
                cur.execute(sql_es)
                mysql.connection.commit()
                trans.translate.data = sql_es
                flash("Se ejecutó exitosamente")
            elif "update" in sql_es:
                print("Siuuuuuuuu")
                cur = mysql.connection.cursor()
                print(cur)
                cur.execute(sql_es)
                mysql.connection.commit()
                trans.translate.data = sql_es
                flash("Se ejecutó exitosamente")

            else:
                print("Nouuuuuuuu")
                cur = mysql.connection.cursor()
                cur.execute(sql_es)
                rv = cur.fetchall()
                query = list(rv)
                query = str(query)
                query = query.replace(')','').replace('(','').replace("'",'').replace('[','').replace(']','')
                print(query)
                trans.translate.data = query
        except Exception as e:
            e = str(e).replace('(','').replace(')','').replace('using password: YES','').split(',')
            flash(e)
        
            '''hacer lista de querys para comparar la cadena x'''                    
            '''Enviar los querys a la bd'''
        
        
        return render_template('execute_query.html', **context)

    return render_template('execute_query.html', **context)

if __name__ == '__main__':
    app.run(debug=True, host = 'localhost')