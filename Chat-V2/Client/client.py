import socket,select,ClientConfig,threading
"""
Protocol Description:
every client assigned unique id when connecting
client --------> server - connection
server --------> client - connection confirmation + id
client --------> server - msg details(dst,content)
server --------> client - msg details(src,content)
client --------> server - close request
"""
class client(object):
    def __init__(self):
        self.__id = None
        self.__server_ip = ClientConfig.SERVER_IP
        self.__server_port = ClientConfig.SERVER_PORT
        self.__server_addr = (self.__server_ip,self.__server_port)
        self.__connected = False
        self.__client = socket.socket()
        self.__alive = True
        self.__buffer = None
        #self.__client.setblocking(ClientConfig.CONN_TIMEOUT)
    def setbuffer(self,buff):
        self.__buffer = buff
    def isConnected(self):
        return self.__connected
    def isAlive(self):
        return self.__alive
    def getid(self):
        return self.__id
    def getserveraddr(self):
        return self.__server_addr
    def isConnected(self):
        return self.__connected
    def getclientsoc(self):
        return self.__client
    def __connect(self):
        self.__client.connect(self.__server_addr)
        #self.__client.setblocking(ClientConfig.CONN_TIMEOUT) # sets the time out for blocking operations of the socket
        data = self.__client.recv(ClientConfig.CONN_CONFIRM_SIZE) # get connection confirmation and id from server
        #self.__client.setblocking(1) # return to blocking mode
        confirm , soc_id = data.split('$') #spliting the information that is seperated by '$' char
        if confirm == ClientConfig.CONN_CONFIRM:
            self.__id = soc_id
            self.__connected = True
    def __close(self):
        self.__client.send(ClientConfig.CLOSE_MSG)
        self.__client.close()
        self.__connected = False
        self.__id = None
    def __recv(self,size = 1024):
        data = self.__client.recv(size)
        src , msg = data.split('$')
        return src + ':' + msg
    def __send(self,msg,soc_id):
        self.__client.send(str(soc_id) +'$'+ msg)
    def run(self):
        while self.__alive:
            #self.__client.setblocking(0)
            self.__connect()
            readables , writables , exceptionals = select.select([self.__client],[self.__client],[self.__client])
            if self.isConnected():
                if len(readables):
                    print self.__recv()
                print writables,readables
                if len(writables): #and self.__buffer is not None:
                    #soc_id = self.__buffer[0]
                    self.__send("hi",1)#self.__buffer)
                    #self.__buffer = None
"""
c = client()
def start():
    c.run()
"""
if __name__ == "__main__":
    c = client()
    c.run()
