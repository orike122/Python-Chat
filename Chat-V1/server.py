import socket,select

class server(object):

    def __init__(self):
        self.server = socket.socket()
        self.host = '0.0.0.0'
        self.port = 4320
        self.maxConn = 5
        self.server.bind((self.host,self.port))
        self.server.listen(self.maxConn)
        self.inputs = [self.server]
    def main(self):
        ok = True
        while 4320 and ok:
            readables,writables,_ = select.select(self.inputs,self.inputs,[])
            if len(readables):
                for s in readables:
                    if s is self.server:
                        client_soc, client_addr = self.server.accept()
                        self.inputs.append(client_soc)
                    else:
                        data = s.recv(1024)
                        if not data:
                            self.inputs.remove(s)
                        elif data == "exit":
                            s.close()
                            self.inputs.remove(s)
                            writables.remove(s)
                        else:
                            print data
            if len(writables):
                for s in writables:
                    s.send("server")
if __name__ == "__main__":
    s = server()
    s.main()
