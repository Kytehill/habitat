import paramiko
import os

vm_host = "192.168.1.31"
pi_host = "192.168.1.30"
aws_host = "18.189.186.66"
aws_username = "ssh -i \"~/Downloads/bonnie.pem\" ec2-user@ec2-3-15-5-76.us-east-2.compute.amazonaws.com"
vm_username = "docker"
pi_username = "pi"
command = "lscpu"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
key_file = os.path.expanduser('~/.ssh/id_rsa')
privatekeyfile = paramiko.RSAKey.from_private_key_file(key_file)
ssh.connect(hostname=aws_host, username=aws_username, pkey=privatekeyfile)
stdin, stdout, stderr = ssh.exec_command(command)
lines = stdout.readlines()
print(lines)
for line in lines:
    final_line = line.strip('\n')
    print(final_line)
