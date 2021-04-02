import paramiko
import os
from app import db
from app.models import User, Environment, Server, Command
import time, threading, sched


class Ssh:

    # dictionary of server_hostname and username
    # commands
    # timing
    # compare live against expectation
    # Class updates db to pass/fail dependent on result
    def execute_commands(self, ip, username):
        # self.get_servers()
        print(username)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key_file = os.path.expanduser('~/.ssh/id_rsa')
        privatekeyfile = paramiko.RSAKey.from_private_key_file(key_file)
        ssh.connect(hostname=ip, username=username, pkey=privatekeyfile)
        stdin, stdout, stderr = ssh.exec_command("lscpu | grep \"Model name:\"")
        lines = stdout.readlines()
        for line in lines:
            final_line = line.strip('\n')
            print(final_line)

    def get_servers(self, env_id):
        servers = Server.query.filter_by(env_id_fk=env_id).all()
        return servers

    # def check_expectation(self):

    def multithread(self, env_id):
        final_servers = {}
        servers = self.get_servers(env_id)
        for server in servers:
            ip_address = server.__dict__["ip_address"]
            username = server.__dict__["username"]
            final_servers.update({ip_address: username})
        thread_list = []
        for ip, username in final_servers.items():
            t = threading.Thread(target=self.execute_commands, args=(ip, username))
            t.start()
            thread_list.append(t)
            for thread in thread_list:
                thread.join()


ssh = Ssh()
ssh.multithread(4)