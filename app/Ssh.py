import paramiko
import logging
import os
from app import db
from app.models import User, Environment, Server, Command
import time, threading, sched
from time import time, sleep
from datetime import datetime


class Ssh:

    # Establish Connection
    # Create thread
    # Execute commands
    # Kill thread
    # Wait for required time
    # Repeat

    def execute_commands(self, ip, username, env_id):
        servers = self.get_servers(env_id)
        timing = self.get_timing(env_id)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key_file = os.path.expanduser('~/.ssh/id_rsa')
        privatekeyfile = paramiko.RSAKey.from_private_key_file(key_file)
        ssh.connect(hostname=ip, username=username, pkey=privatekeyfile)
        stdin, stdout, stderr = ssh.exec_command("lscpu | grep \"Model name:\"")
        lines = stdout.readlines()
        for line in lines:
            final_line = line.strip('\n')
            for server in servers:
                self.compare(server.id, final_line)
                print("Comparison")
                print(datetime.now())
        threading.Timer(timing, self.execute_commands, args=(ip, username, env_id)).start()

    def get_servers(self, env_id):
        servers = Server.query.filter_by(env_id_fk=env_id).all()
        return servers

    def get_timing(self, env_id):
        timing_query = Environment.query.filter_by(id=env_id).first()
        timing = int(timing_query.__dict__['timing'])
        return timing

    def multithread(self, env_id):
        final_servers = {}
        servers = self.get_servers(env_id)
        for server in servers:
            ip_address = server.__dict__["ip_address"]
            username = server.__dict__["username"]
            final_servers.update({ip_address: username})
        thread_list = list()
        for ip, username in final_servers.items():
            print("Main    : create and start thread %d.", ip)
            t = threading.Thread(target=self.execute_commands, args=(ip, username, env_id))
            thread_list.append(t)
            t.start()
        for index, thread in enumerate(thread_list):
            print("Main    : before joining thread %d.", index)
            print(thread)
            thread.join()
            print("Main    : thread %d done", ip)

    def compare(self, server_id, live_output):
        command_query = Command.query.filter_by(server_id_fk=server_id).all()
        for command in command_query:
            expected_output = command.expectation
            if expected_output == live_output:
                command.command_status = 2
                db.session.commit()
            else:
                command.command_status = 0
                db.session.commit()

ssh = Ssh()
ssh.multithread(5)
# ssh.compare(1, 'blah')

