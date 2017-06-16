 #!/usr/bin/python
 # -*- coding:utf-8 -*-
 # cp@chenpeng.info
 
import os
import paramiko
import cmd


class Check:
    """
    Return the factorial of n, an exact integer >= 0.
    If the result is small enough to fit in an int, return an int.
    Else return a long.

    >>> host = "100.86.1.110"
      
    >>> user = "root"
    
    >>> pw = "admin123"
    
    >>> innerip = "192.168.0.11"
    
    >>> ckip = Check()
    
    b'        inet 192.168.0.11  netmask 255.255.255.0  broadcast 192.168.0.255\\n'
    >>> ckip.check_ip(host, 22, user, pw, innerip)
    True
    
    >>> ckip.check_oth(4)
    8
    >>> ckip.restart_inner(host, 22, user, pw)
    True
    """        
    def __init__(self):        
        pass
    
    def check_ip(self, host, port, user, pwd, iip):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, pwd)
#         cmd = "ifconfig | grep" + iip
        cmd = "ifconfig | grep " + iip
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read()
        ssh.close()
        if out == b'':
            return False
        else:
            return True
        
    def check_oth(self, num):
        """
        >>> check = Check()
        >>> check.check_oth(4)
        8
        """
        print(num * 2)
    
    def shutdown_inner(self, ip, port, user, pwd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, user, pwd)
#         cmd = "ifconfig | grep" + iip
        cmd = "shutdown -h 0"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read()
        ssh.close()
        print(cmd)
        print(out)
        return True

    def restart_inner(self, ip, port, user, pwd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, user, pwd)
        cmd = "reboot"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read()
        ssh.close()
        return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()