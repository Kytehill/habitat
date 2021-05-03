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


@app.route('/environments/<id>', methods=["GET", "POST"])
@login_required
def environments(id):
    user = User.query.filter_by(id=id).first_or_404()
    environments = Environment.query.filter_by(user_id_fk=id).all()
    environment_id = environments[0].__dict__["id"]
    servers = Server.query.filter_by(env_id_fk=environment_id).all()
    form = EnvironmentForm()
    if form.validate_on_submit():
        environment = Environment(name=form.name.data, timing=form.timing.data, user_id_fk=id)
        db.session.add(environment)
        db.session.commit()
        flash('Congratulations, your environment has been added!')
        return redirect(url_for('environments', id=id))
    return render_template('environments.html', user=user, environments=environments, servers=servers, form=form)


@app.route('/edit_environment/<env_id>', methods=['GET', 'POST'])
@login_required
def edit_environment(env_id):
    form = EnvironmentForm()
    environment = Environment.query.filter_by(id=env_id).first()
    if form.validate_on_submit():
        environment.name = form.name.data
        environment.timing = form.timing.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('environments', id=current_user.id))
    elif request.method == 'GET':
        form.name.data = environment.name
        form.timing.data = environment.timing
        return render_template('edit_environment.html', title='Edit Environment', form=form)


@app.route('/delete_environment/<env_id>', methods=['GET','POST'])
@login_required
def delete_environment(env_id):
    environment = Environment.query.filter_by(id=env_id).first()
    db.session.delete(environment)
    db.session.commit()
    flash('Environment ' + environment.name + ' has been successfully deleted')
    return redirect(url_for('environments', id=current_user.id))


@app.route('/servers/<env_id_fk>', methods=["GET", "POST"])
@login_required
def servers(env_id_fk):
    environment = Environment.query.filter_by(id=env_id_fk).first()
    user = current_user
    servers = Server.query.filter_by(env_id_fk=env_id_fk).all()
    form = ServerForm()
    if form.validate_on_submit():
        server = Server(ip_address=form.ip_address.data, username=form.username.data, env_id_fk=env_id_fk)
        db.session.add(server)
        db.session.commit()
        return redirect(url_for('servers', env_id_fk=env_id_fk))
    return render_template('servers.html', servers=servers, user=user, environment=environment, form=form)


@app.route('/delete_server/<environment_id>/<server_id>')
@login_required
def delete_server(environment_id, server_id):
    server = Server.query.filter_by(id=server_id).first()
    db.session.delete(server)
    db.session.commit()
    flash('Server with username: ' + server.username + ' has been successfully deleted')
    return redirect(url_for('servers', env_id_fk=environment_id, id=server_id))


@app.route('/edit_server/<environment_id>/<server_id>', methods=['GET', 'POST'])
@login_required
def edit_server(environment_id, server_id):
    form = ServerForm()
    server = Server.query.filter_by(id=server_id).first()
    if form.validate_on_submit():
        server.ip_address = form.ip_address.data
        server.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('servers', env_id_fk=environment_id))
    elif request.method == 'GET':
        form.ip_address.data = server.ip_address
        form.username.data = server.username
        return render_template('edit_server.html', title='Edit Server', form=form)


@app.route('/commands/<server_id>', methods=["GET", "POST"])
@login_required
def commands(server_id):
    commands = Command.query.filter_by(server_id_fk=server_id).all()
    server = Server.query.filter_by(id=server_id).first()
    form = CommandForm()
    if form.validate_on_submit():
        command = Command(command=form.command.data, expectation=form.expectation.data, server_id_fk=server_id)
        db.session.add(command)
        db.session.commit()
        return redirect(url_for('commands', server_id=server_id))
    return render_template('commands.html', commands=commands, server=server, form=form)


@app.route('/delete_command/<server_id>/<command_id>')
@login_required
def delete_command(server_id, command_id):
    command = Command.query.filter_by(id=command_id).first()
    db.session.delete(command)
    db.session.commit()
    flash('Command ' + command.command + ' has been successfully deleted')
    return redirect(url_for('commands', server_id=server_id, id=command_id))


@app.route('/edit_command/<server_id>/<command_id>', methods=['GET', 'POST'])
@login_required
def edit_command(server_id, command_id):
    form = CommandForm()
    command = Command.query.filter_by(id=command_id).first()
    if form.validate_on_submit():
        command.command = form.command.data
        command.expectation = form.expectation.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('commands', server_id=server_id))
    elif request.method == 'GET':
        form.command.data = command.command
        form.expectation.data = command.expectation
        return render_template('edit_command.html', title='Edit Command', form=form)


# @app.route('/start_validation')
# @login_required
# def start_validation():
#     Ssh.multithread()
#     return redirect(url_for('environments', id=current_user.id))


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
