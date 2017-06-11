 #!/usr/bin/python
 # -*- coding:utf-8 -*-
 # cp@chenpeng.info
 
import os
import paramiko 
def MAIN(): 
    host = "200.200.1.237"
    port = 22     
    user = "zzy"
    pswd = "1"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, user, pswd)
    stdin, stdout, stderr = ssh.exec_command('ifconfig')
    print (stdout.read())
    ssh.close()
if __name__=='__main__':
    try:
        MAIN()
    except Exception as e:
        print (e) 
