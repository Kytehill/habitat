from app import app, db
from app.views import CommandForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from app.models import Server, Command


@app.route('/commands/<server_id>', methods=["GET", "POST"])
@login_required
def commands(server_id):
    """
    Commands on specified server
    :param server_id: ID for the selected server
    :return: renders template for commands based on server ID
    """
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
    """
    Deletes command
    :param server_id: ID for server
    :param command_id: ID for command
    :return: redirects command template
    """
    command = Command.query.filter_by(id=command_id).first()
    db.session.delete(command)
    db.session.commit()
    flash('Command ' + command.command + ' has been successfully deleted')
    return redirect(url_for('commands', server_id=server_id, id=command_id))


@app.route('/edit_command/<server_id>/<command_id>', methods=['GET', 'POST'])
@login_required
def edit_command(server_id, command_id):
    """
    Edits requested command
    :param server_id: ID of server command sits on
    :param command_id: ID of command
    :return: Renders edit command template, Redirects to commands if form submitted
    """
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
