# coding=utf-8
import paramiko
from time import sleep

class Check:
    """
    Return the factorial of n, an exact integer >= 0.
    If the result is small enough to fit in an int, return an int.
    Else return a long.

    >>> ip = "100.1.22.1"
    
    >>> host = "100.1.22.170"
      
    >>> user = "root"
    
    >>> pwd = "admin123"
    
    >>> iip = "192.168.0.71"
    
    >>> ckip = Check(host = ip, user = 'root', pwd = 'Admin12345sangfornetwork')
    
    b'        inet 192.168.0.11  netmask 255.255.255.0  broadcast 192.168.0.255\\n'
    >>> ckip.shutdownInner(host, 22, user, pwd)
    True
    """        
    def __init__(self, host = '100.1.22.1', user = 'root', pwd = 'Admin12345sangfornetwork'):
        self.host = host
        self.port = 22
        self.user = user
        self.pwd = pwd
        
        cmds = [
                "set +H",
                "echo -e \"#!/bin/bash     \\nPING=\`ping -c 3 \$1 | grep '0 received' | wc -l\`    \\necho \$PING\" > ping.sh",
                "chmod +x ping.sh"
                ]
        
        stdout = []
        stderr = []
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.host, self.port, self.user, self.pwd)
            
            for cmd in cmds: 
                ret = ssh.exec_command(cmd)
                out = ret[1].read()
                if out != b'':
                    stdout.append(out)
                err = ret[2].read()
                if err != b'':
                    stderr.append(err)
            ssh.close()
            if len(stderr) != 0 or len(stdout) != 0:
                return None
        except:
            print('init Check object, fail to create ping.sh in %s, out = %s, error = %s' %(host, stdout, stderr))
            return None
    
    def ping(self, ip):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.host, self.port, self.user, self.pwd)
            
            ret = ssh.exec_command("./ping.sh %s" %(ip))
            out = ret[1].read()
            err = ret[2].read()
            ssh.close()
            
            if out == b'0\n':
                return True
            elif err != b'':
                print ('excute shell ping.sh error')
                return False
            else:
                return False
        except:
            print('check ip[%s] error' %(ip))
            return False
    
    def checkInnerIP(self, host, port, user, pwd, iip):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, user, pwd)
            cmd = "ifconfig | grep " + iip
            ret = ssh.exec_command(cmd)
            out = ret[1].read()
            ssh.close()
            if out == b'':
                return False
            else:
                return True
        except:
            return False
            
    def restartInner(self, ip, port, user, pwd):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port, user, pwd)
            ret = ssh.exec_command("reboot")
            out = ret[1].read()
            error = ret[2].read()
            ssh.close()
            if out != b'' or error != b'':
                return False
            return True
        except:
            print('inner restart instance fail')
            return False
        
    def shutdownInner(self, ip, port, user, pwd):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port, user, pwd)
            ssh.exec_command("shutdown -h 0")
            ssh.close()
#             ret = ssh.exec_command("shutdown -h 0")
#             ssh.close()
#             out = ret[1].read()
#             error = ret[2].read()
#             if out != b'' or (error != b'' and "Shutdown scheduled" not in error):
#                 return False
            return True
        except:
            print('fail to shutdown in shutdownInner')
            return False
        
    def writeLine(self, ip, user, pwd, line = 'aaaaaaaaaaa', file = 'aaa.txt'):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, 22, user, pwd)
            ret = ssh.exec_command("echo %s > %s" %(line, file))
            ssh.close()
            out = ret[1].read()
            error = ret[2].read()
            if out != b'' or error != b'':
                return False
            return True
        except:
            print('fail to write into file')
            return False
    
    def readLine(self, ip, user, pwd, file = 'aaa.txt'):
        out = ''
        error = ''
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, 22, user, pwd)
            ret = ssh.exec_command("cat aaa.txt")
            sleep(0.5)
            ssh.close()
            out = ret[1].read()
            error = ret[2].read()
            if error != b'':
                return None
            return out
        except:
            print('fail to read from file[%s], out = [%s], error = [%s]' %(file, out, error))
            return None
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
