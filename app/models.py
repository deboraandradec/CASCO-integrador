from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def current_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(84), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return self.name

class Turtle(db.Model):
    __tablename__ = "turtles"
    id = db.Column(db.Integer, primary_key=True)
    especie = db.Column(db.String(84), nullable=False)
    tamanho = db.Column(db.String(84), nullable=False)
    localizacao = db.Column(db.String(84), nullable=False)
    data_registro = db.Column(db.String(84), nullable=False)