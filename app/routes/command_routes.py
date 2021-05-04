from app import app, db, run_environment_ssh
from app.views import LoginForm, RegistrationForm, EnvironmentForm, ServerForm, CommandForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Environment, Server, Command
from werkzeug.urls import url_parse
from datetime import datetime


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
