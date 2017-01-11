import socket
import select
inlist = []
condic = {}
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(False)
s.bind(('',9999))
s.listen(5)
inlist.append(s)
while True:
    conin,conout,conerr = select.select(inlist,[],[])
    if any((conin, conout, conerr)) == True:
        for i in conin:
            if i is s:
                conn, addr = s.accept()
                print ("client {0} connected".format(addr))
                inlist.append(conn)
                condic.setdefault(conn, addr)
                conn.sendall('require')
            elif i in condic:
                try:
                    data = i.recv(1024)
                    if data:
                        print('recv {0} from client {1}'.format(data.decode(), condic[i]))
                        i.sendall(data)
                except ConnectionResetError:
                    inlist.remove(i)
                    print('client {0} disconnected'.format(condic[i]))


