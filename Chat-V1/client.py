import socket, select,keyboard

class client(object):
    def __init__(self):
        self.client = socket.socket()
        self.host = "127.0.0.1"
        self.port = 4320
        self.client.connect((self.host,self.port))
        self.inputs = [self.client]
    def main(self):
        while 4320:
            readable, writable, errorororable = select.select(self.inputs, self.inputs, [])
            if len(readable) != 0:
                data = self.client.recv(1024)
                if len(data) != 0:
                    print 'receive data:', data
            if len(writable) != 0:
                self.client.send("client")
            if keyboard.is_pressed('q'):
                break
        self.client.send("exit")
        self.client.close()
        print("exit")
if __name__ == "__main__":
    c = client()
    c.main()
