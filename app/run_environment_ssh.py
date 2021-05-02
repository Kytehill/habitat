import paramiko
from paramiko import BadHostKeyException, AuthenticationException, SSHException
import socket
from app import db
import os
from app.models import Environment, Server, Command
import threading
from datetime import datetime
from flask import flash


def execute_commands(servers, environment):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key_file = os.path.expanduser('~/.ssh/id_rsa')
    privatekeyfile = paramiko.RSAKey.from_private_key_file(key_file)
    for server in servers:
        commands = Command.query.filter_by(server_id_fk=server.id).all()
        try:
            ssh.connect(hostname=server.ip_address, username=server.username, pkey=privatekeyfile)
            # environment.connection_status = 0
            environment.status_timestamp = datetime.now()
            server.connection_status = 0
            server.status_timestamp = datetime.now()
            db.session.commit()
            for command in commands:
                print(command)
                stdin, stdout, stderr = ssh.exec_command(command.command)
                output = stdout.readlines()
                print(output)
                for line in output:
                    final_line = line.strip('\n')
                    print(command.id)
                    print(command.expectation)
                    print(final_line)
                    compare(command.id, command.expectation, final_line)
        except (BadHostKeyException, AuthenticationException,
                SSHException, socket.error) as e:
            server.connection_status = 1
            server.status_timestamp = datetime.now()
            db.session.commit()
            flash('Connection not established on Server: ' + server.ip_address + ' in  Environment: ' + environment.name)
    check_server_status(server, commands)
    check_environment_status(environment, servers)


def compare(command_id, expectation, live_output):
    command = Command.query.filter_by(id=command_id).first()
    if expectation == live_output:
        command.command_status = 2
        db.session.commit()
    else:
        command.command_status = 0
        db.session.commit()


def check_environment_status(environment, servers):
    failing_servers = []
    for server in servers:
        if server.server_status == 0:
            failing_servers.append(server.ip_address)
    if len(failing_servers) > 0:
        environment.connection_status = 1
        db.session.commit()
    else:
        environment.env_status = 0
        db.session.commit()


def check_server_status(server, commands):
    failing_commands = []
    for command in commands:
        if command.command_status == 0:
            failing_commands.append(command.command)
    if len(failing_commands) > 0:
        server.server_status = 0
        db.session.commit()
    else:
        server.server_status = 2
        db.session.commit()