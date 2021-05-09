import paramiko
from paramiko import BadHostKeyException, AuthenticationException, SSHException
import socket
from app import db
import os
from app.models import Command
from datetime import datetime
from flask import flash


def execute_commands(servers, environment):
    """
    Executes commands for given servers in a given environment
    :param servers: Servers on which commands to execute
    :param environment: Environment where servers sit
    """
    for server in servers:
        commands = Command.query.filter_by(server_id_fk=server.id).all()
        try:
            run_commands(server, commands)
        except (BadHostKeyException, AuthenticationException,
                SSHException, socket.error) as e:
            server.connection_status = 1
            server.status_timestamp = datetime.now()
            for command in commands:
                command.command_status = 0
                command.actual_output = None
            db.session.commit()
            flash('Connection not established on Server: ' + server.ip_address + ' in  Environment: ' + environment.name)
        update_server_status(server, commands)
    update_environment_status(environment, servers)
    update_connection_status(environment, servers)


def run_commands(server, commands):
    """
    Runs commands via SSH on server
    :param server: Target server for commands to be run
    :param commands: Commands to be run on server
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key_file = os.path.expanduser('~/.ssh/id_rsa')
    privatekeyfile = paramiko.RSAKey.from_private_key_file(key_file)
    ssh.connect(hostname=server.ip_address, username=server.username, pkey=privatekeyfile)
    server.connection_status = 0
    server.status_timestamp = datetime.now()
    db.session.commit()
    for command in commands:
        stdin, stdout, stderr = ssh.exec_command(command.command)
        command.status_timestamp = datetime.now()
        output = stdout.readlines()
        if output:
            for line in output:
                final_line = line.strip('\n')
                compare(command.id, command.expectation, final_line)
                command.actual_output = final_line
                db.session.commit()
        else:
            compare(command.id, command.expectation, None)
            command.actual_output = None
            db.session.commit()


def compare(command_id, expectation, live_output):
    """
    Compare the expected output with the live output on server
    :param command_id: ID for command
    :param expectation: Expected output for command
    :param live_output: Live ouput returned for command from server
    """
    command = Command.query.filter_by(id=command_id).first()
    if expectation == live_output:
        command.command_status = 2
        db.session.commit()
    else:
        command.command_status = 0
        db.session.commit()


def update_environment_status(environment, servers):
    """
    Updates environment status based on status of servers sat within environment
    :param environment: Environment
    :param servers: Servers within environment
    """
    failing_servers = []
    if servers:
        for server in servers:
            if server.server_status == 0:
                failing_servers.append(server.ip_address)
        if len(failing_servers) > 0:
            environment.env_status = 0
            db.session.commit()
        else:
            environment.env_status = 2
            db.session.commit()
    else:
        environment.env_status = 0
        db.session.commit()


def update_server_status(server, commands):
    """
    Updates server status based on status of commands sat on server
    :param server: Server
    :param commands: Commands sat on server
    """
    failing_commands = []
    for command in commands:
        if command.command_status == 0 or command.command_status == 1:
            failing_commands.append(command.command)
    if len(failing_commands) > 0:
        server.server_status = 0
        db.session.commit()
    else:
        server.server_status = 2
        db.session.commit()


def update_connection_status(environment, servers):
    """
    Updates connection status of environment based on servers sat in environment
    :param environment: Environment
    :param servers: Servers within environment
    """
    failed_connections = []
    if servers:
        for server in servers:
            if server.connection_status == 1:

                failed_connections.append(server.ip_address)
        if len(failed_connections) > 0:
            environment.connection_status = 1
            db.session.commit()
        else:
            environment.connection_status = 0
            db.session.commit()
    else:
        environment.connection_status = 1
        db.session.commit()


