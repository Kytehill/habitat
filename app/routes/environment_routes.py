from app import app, db
from app.views import EnvironmentForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app.models import User, Environment, Server, Command


@app.route('/environments/<id>', methods=["GET", "POST"])
@login_required
def environments(id):
    user = User.query.filter_by(id=id).first_or_404()
    environments = Environment.query.filter_by(user_id_fk=id).all()
    form = EnvironmentForm()
    if form.validate_on_submit():
        environment = Environment(name=form.name.data, timing=form.timing.data, user_id_fk=id)
        db.session.add(environment)
        db.session.commit()
        flash('Congratulations, your environment has been added!')
        return redirect(url_for('environments', id=id))
    return render_template('environments.html', user=user, environments=environments, form=form)


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
    servers = Server.query.filter_by(env_id_fk=env_id).all()
    db.session.delete(environment)
    for server in servers:
        commands = Command.query.filter_by(server_id_fk=server.id)
        for command in commands:
            db.session.delete(command)
        db.session.delete(server)
    db.session.commit()
    flash('Environment ' + environment.name + ' has been successfully deleted')
    return redirect(url_for('environments', id=current_user.id))