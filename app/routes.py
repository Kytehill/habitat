from app import app, db
from app.views import LoginForm, RegistrationForm, EditEnvironmentForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Environment, Server, Command
from werkzeug.urls import url_parse


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


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


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


@app.route('/environments/<id>')
@login_required
def environments(id):
    user = User.query.filter_by(id=id).first_or_404()
    environments = Environment.query.filter_by(user_id_fk=id).all()
    return render_template('environments.html', user=user, environments=environments)


@app.route('/servers/<env_id>')
@login_required
def servers(env_id):
    print(env_id)
    servers = Server.query.filter_by(env_id_fk=env_id).all()
    return render_template('servers.html', servers=servers)


@app.route('/commands/<server_id>')
@login_required
def commands(server_id):
    print(server_id)
    commands = Command.query.filter_by(server_id_fk=server_id).all()
    return render_template('commands.html', commands=commands)


@app.route('/edit_environment/<env_id>', methods=['GET', 'POST'])
@login_required
def edit_environment(env_id):
    form = EditEnvironmentForm()
    environment = Environment.query.filter_by(id=env_id).first()
    servers_in_env = Server.query.filter_by(env_id_fk=env_id).all()
    if form.validate_on_submit():
        environment.name = form.name.data
        environment.timing = form.timing.data
        servers_in_env = form.servers.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_environment', env_id=env_id))
    elif request.method == 'GET':
        form.name.data = environment.name
        form.timing.data = environment.timing
        form.servers.data = servers_in_env
        return render_template('edit_environment.html', title='Edit Environment', form=form)
