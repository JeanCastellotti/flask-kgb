from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = EmailField(
        'Adresse e-mail',
        validators=[DataRequired('Ce champs est obligatoire.'),
                    Email()])
    password = PasswordField(
        'Mot de passe',
        validators=[DataRequired('Ce champs est obligatoire.')])
    submit = SubmitField('Se connecter')