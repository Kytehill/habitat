from app import app, db, run_environment_ssh
from app.views import LoginForm, RegistrationForm, EnvironmentForm, ServerForm, CommandForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Environment, Server, Command
from werkzeug.urls import url_parse
from datetime import datetime


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    The code associated with the Login has been derived from a Flask tutorial
    provided by Miguel Grinberg

    Grinberg, M., 2017. The Flask Mega Tutorial [Online Programming Tutorial]. Available
        from: https://miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
        [Accessed 22 March 2021]
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/run_environment/<env_id>')
@login_required
def run_environment(env_id):
    environment = Environment.query.filter_by(id=env_id).first()
    servers = Server.query.filter_by(env_id_fk=env_id).all()
    environment.status_timestamp = datetime.now()
    db.session.commit()
    run_environment_ssh.execute_commands(servers, environment)
    return redirect(url_for('environments', id=current_user.id))


@app.route('/run_all_environments')
@login_required
def run_all_environments():
    environments = Environment.query.filter_by(user_id_fk=current_user.id)
    for environment in environments:
        environment.status_timestamp = datetime.now()
        db.session.commit()
        servers = Server.query.filter_by(env_id_fk=environment.id).all()
        run_environment_ssh.execute_commands(servers, environment)
    return redirect(url_for('environments', id=current_user.id))