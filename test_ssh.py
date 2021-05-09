import paramiko
import os

"""
Module set up to test command execution
"""

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
key_file = os.path.expanduser('~/.ssh/id_rsa')
privatekeyfile = paramiko.RSAKey.from_private_key_file(key_file)
ssh.connect(hostname='192.168.1.38', username='docker', pkey=privatekeyfile)
stdin, stdout, stderr = ssh.exec_command('lscpu | grep "L2 cache"')
output = stdout.readlines()
print(output)
for line in output:
    final_line = line.strip('\n')
    print(final_line)
