import paramiko
from paramiko import BadHostKeyException, AuthenticationException, SSHException
import socket
from app import db
import os
from app.models import Environment, Server, Command
import threading
from datetime import datetime

"""
This module was set up with a view to using a multithreaded approach to executing commands
This module is not in use at the moment and will need to be executed as a separate long running 
background process alongside the flask application

This will form part of future work for the application 
"""

# Create thread
# Open Connection for Ip Address
# Run all commands for that server
# Compare all outputs and qrite to DB
# Kill thread
# Wait for required time
# Repeat

def execute_commands(environment, server, commands):
    # servers = self.get_servers(env_id)
    # timing = self.get_timing(env_id)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key_file = os.path.expanduser('~/.ssh/id_rsa')
    privatekeyfile = paramiko.RSAKey.from_private_key_file(key_file)

    try:
        ssh.connect(hostname=server.ip_address, username=server.username, pkey=privatekeyfile)
        server.connection_status = 0
        print("Updating to connection status of " + str(server.connection_status) + " for" + server.ip_address)
        db.session.commit()
        print('Connected ' + server.ip_address)
        print(datetime.now())
        for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command.command)
            output = stdout.readlines()
            for line in output:
                final_line = line.strip('\n')
                compare(command.id, command.expectation, final_line)
    except (BadHostKeyException, AuthenticationException,
            SSHException, socket.error) as e:
        print(e)
        print('There is an issue with the connection in server: ' + server.ip_address)
        print('Please ensure SSH Keys are set up and connection is live')
        print(server.ip_address + " " + str(server.connection_status))
        server.connection_status = 1
        print(server.ip_address + " " + str(server.connection_status))
        print("Updating to connection status of " + str(server.connection_status) + " for" + server.ip_address)
        db.session.commit()


def get_servers(env_id):
    servers = Server.query.filter_by(env_id_fk=env_id).all()
    return servers


def get_timing(env_id):
    timing_query = Environment.query.filter_by(id=env_id).first()
    timing = int(timing_query.__dict__['timing'])
    return timing


def multithread():
    thread_list = list()
    environments = Environment.query.all()
    event = threading.Event
    while True:
        for environment in environments:
            servers = get_servers(environment.id)
            for server in servers:
                commands = Command.query.filter_by(server_id_fk=server.id).all()
                # time.sleep(int(environment.timing))
                # t = threading.Thread(target=self.execute_commands, args=(environment, server, commands))
                print(environment.name)
                print(environment.timing)
                t = threading.Timer(int(environment.timing), execute_commands, args=(environment, server, commands))
                # time.sleep(int(environment.timing))
                t.daemon = True
                t.start()
                thread_list.append(t)
                # print("Thread for " + server.ip_address + " started")
                # print(t)
        for index, thread in enumerate(thread_list):
            # print(index)
            # print(thread)
            thread.join()
        print("All threads Finished")


def compare(command_id, expectation, live_output):
    command = Command.query.filter_by(id=command_id).first()
    if expectation == live_output:
        command.command_status = 2
        db.session.commit()
    else:
        command.command_status = 0
        db.session.commit()


# def stop_validation():
#     sys._exit('Exited')

# def main():
#     multithread()
#
#
# if __name__ == "__main__":
#     main()
