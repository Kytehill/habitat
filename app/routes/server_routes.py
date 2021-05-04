from app import app, db
from app.views import ServerForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app.models import Environment, Server, Command


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
    commands = Command.query.filter_by(server_id_fk=server.id).all()
    for command in commands:
        db.session.delete(command)
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