#!/usr/bin/env python
import subprocess
import time
import socket
import select
addr = ('localhost',9999)
def get_ipv6():
    cmd = "ip -6 addr | grep 'inet6'"
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    return p.stdout.read()
def main():
    myipv6 = get_ipv6()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while s.connect_ex(addr) != 0:
        print("""can not connect to {0}:{1}
                try to connect in 5 seconds""".format(addr[0],addr[1]))
        time.sleep(5)
    s.setblocking(False)
    s.sendall(myipv6)
    inputlist = []
    inputlist.append(s)
    while True:
        stdinput, stdoutput, stderr = select.select(inputlist,[],[])
        if any((stdinput, stdoutput, stderr)):
            data = s.recv(1000)
            if data.decode() == 'require':
                s.sendall(myipv6)

        

if __name__ == '__main__':
    main()
