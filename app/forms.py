from flask_wtf import FlaskForm
from wtforms.fields import (EmailField, PasswordField, StringField, SubmitField, DateField)


class LoginUserForm(FlaskForm):
  email = EmailField("E-mail")
  password = PasswordField("Senha")
  submit = SubmitField("Entrar")

class RegisterUserForm(FlaskForm):
  username = StringField("Nome")
  email = EmailField("E-mail")
  password = PasswordField("Senha")
  submit = SubmitField("Criar conta")


class RegisterTurtleForm(FlaskForm):
  especie = StringField('Espécie')
  tamanho = StringField('Tamanho')
  localizacao = StringField('Localização')
  data_registro = DateField('Data do registro')
  submit = SubmitField("Registrar Tartaruga")
