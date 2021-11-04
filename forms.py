from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect, CSRFError
from wtforms.fields import TextField, StringField, TextField, IntegerField, PasswordField, SelectField, SubmitField

class Connection_forms(FlaskForm):
    
    host = StringField('Host')
    user = StringField('Usuario')
    password = PasswordField('Contraseña')
    name_db = StringField('Nombre Base de datos')
    submit = SubmitField('Conectar')

# Utilizar solamente si quieren usar Flask form para los campos
class QueryFormExecute(FlaskForm):
    esp_sql = StringField('SQL en Español')
    translate = StringField('Traslado')
    submit = SubmitField('Convertir')