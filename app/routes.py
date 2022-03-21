from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from app import db
from app.models import User, Turtle

from app.forms import RegisterTurtleForm, RegisterUserForm, LoginUserForm


def init_app(app):

    @app.route("/")
    def index():

        if current_user.is_active:
            return render_template('home.html')
        return render_template("index.html")

    @app.route('/login/', methods=('GET', 'POST'))
    def login():
        form = LoginUserForm()

        if form.validate_on_submit():

            user = User.query.filter_by(email=form.email.data).first()

            if not user:
                flash("Email incorreto", category="danger")
                return redirect(url_for('login'))

            if user.password != form.password.data:
                flash("Email correto", category='success')
                flash("Senha incorreta", category='danger')
                return redirect(url_for('login'))

            login_user(user)
            return redirect(url_for('index'))


        return render_template('login.html', form=form)

    @app.route('/registro/', methods=('GET', 'POST'))
    def registrar_usuario():
        form = RegisterUserForm()

        if form.validate_on_submit():

            if User.query.filter_by(email=form.email.data).first():
                flash("O email já está registrado", category="danger")
                return redirect(url_for('registrar_usuario'))

            user = User()

            user.name = form.username.data
            user.email = form.email.data
            user.password = form.password.data

            db.session.add(user)
            db.session.commit()

            login_user(user)

            return redirect(url_for('index'))

        return render_template('registro.html', form=form)

    @app.route('/logout/', methods=('GET', 'POST'))
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/usuarios/')
    def usuarios():
        users = User.query.all()
        return render_template('usuarios.html', users=users)

    # perfil

    @app.route('/perfil/')
    def profile():
        user = User.query.filter_by(id=current_user.id).first()
        return render_template('profile.html', user=user)

    @app.route('/perfil/edicao/', methods=('GET', 'POST'))
    def edit_profile():
        user = User.query.filter_by(id=current_user.id).first()
        form = RegisterUserForm()

        form.username.data = user.name
        form.email.data = user.email

        return render_template('edit_profile.html', form=form)

    @app.route('/perfil/edicao/enviar/', methods=('GET', 'POST'))
    def submit_profile_edit():
        user = User.query.filter_by(id=current_user.id).first()
        form = RegisterUserForm()

        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                if form.email.data != user.email:
                    flash("O email já está registrado", category="danger")
                    return redirect(url_for("edit_profile"))

            user.name = form.username.data
            user.email = form.email.data
            
            db.session.commit()

            return redirect(url_for('profile'))

    @app.route('/perfil/deletar/')
    def delete_profile():
        user = User.query.filter_by(id=current_user.id).first()

        db.session.delete(user)
        db.session.commit()

        logout_user()

        return redirect(url_for('index'))
    
    # tartarugas

    @app.route('/tartarugas/')
    def turtles_view():
        turtles = Turtle.query.all()
        return render_template('turtles.html', turtles=turtles)

    @app.route('/tartaruga/<id>')
    def turtle(id):
        turtle = Turtle.query.filter_by(id=id).first()
        return render_template('turtle.html', turtle=turtle)

    @app.route('/tartaruga/criar/', methods=('GET', 'POST'))
    def new_turtle():
        
        form = RegisterTurtleForm()

        if form.validate_on_submit():

            turtle = Turtle()

            turtle.especie = form.especie.data
            turtle.tamanho = form.tamanho.data
            turtle.localizacao = form.localizacao.data
            turtle.data_registro = form.data_registro.data

            db.session.add(turtle)
            db.session.commit()

            flash('Tartaruga registrada com sucesso', category='success')

        form.especie.data = ''
        form.tamanho.data = ''
        form.localizacao.data = ''
        form.data_registro.data = ''

        return render_template('new_turtle.html', form=form)

    @app.route('/tartaruga/<id>/editar/', methods=('GET', 'POST'))
    def turtle_edit(id):
        turtle = Turtle.query.filter_by(id=id).first()
        form = RegisterTurtleForm()

        form.especie.data = turtle.especie
        form.tamanho.data = turtle.tamanho
        form.localizacao.data = turtle.localizacao

        return render_template('edit_turtle.html', form=form, turtle=turtle)

    @app.route('/tartaruga/<id>/editar/submit/', methods=('GET', 'POST'))
    def submit_turtle_edit(id):
        turtle = Turtle.query.filter_by(id=id).first()
        form = RegisterTurtleForm()

        if form.validate_on_submit():
            turtle.especie  = form.especie.data
            turtle.tamanho = form.tamanho.data
            turtle.localizacao = form.localizacao.data
            turtle.data_registro = form.data_registro.data

            db.session.commit()
            
            return redirect(url_for('turtle', id=id))

    @app.route('/tartaruga/<id>/deletar/')
    def detele_turtle(id):
        turtle = Turtle.query.filter_by(id=id).first()

        db.session.delete(turtle)
        db.session.commit()

        return redirect(url_for('turtles_view'))