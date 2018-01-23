import socket,select,ClientConfig,threading
__author__ = "Cyben AKA as Benash, orike122 AKA as the guy with no cool nicknames(like Cyben)"
"""
Protocol Description:
every client assigned unique id when connecting
client --------> server - connection
server --------> client - connection confirmation + id
client --------> server - msg details(dst,content)
server --------> client - msg details(src,content)
client --------> server - close request
"""
"""
TODO:
- add try/except blocks, even a light square won't save us if it crashes.
- add a methods that connects usernames to id's
- add nice and easy txt ui
- go on Toby's checklist and make sure we've got it all working
- kick some asses
Counting on Benash!
if it dosen't work we can always shut down the internet and say we can't download from github.
by the way maybe we should just to simple tkinter instead kivy?
if you can do it it'll be graet but FIRST(inspires) let finish the basics.
"""
class client(object):
    def __init__(self):
        self.__writables = 1
        self.__id = None
        self.__server_ip = ClientConfig.SERVER_IP
        self.__server_port = ClientConfig.SERVER_PORT
        self.__server_addr = (self.__server_ip,self.__server_port)
        self.__connected = False
        self.__client = socket.socket()
        self.__alive = True
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
    def connect(self):
        self.__client.connect(self.__server_addr)
        data = self.__client.recv(ClientConfig.CONN_CONFIRM_SIZE)
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
    def __send(self):
        while self.__alive:
            if self.__writables:
                msg = raw_input("Enter message: ")
                soc_id = msg[0]
                #need to check if soc_id in writables otherwise there will be an error
                #don't ignore it ben, im counting on you to check it :)
                msg = msg[1:]
                self.__client.send(soc_id +'$'+ msg)
    def run(self):
        input_thread = threading.Thread(target = self.__send)
        input_thread.start()
        while self.__alive:
            self.__readables , self.__writables , exceptionals = select.select([self.__client],[self.__client],[self.__client])
            if self.isConnected():
                if len(self.__readables):
                    print '\t'+self.__recv()#fix this ugly formating. make the text gui fuckin' awosome , as just you can do!
            
"""
c = client()
def start():
    c.run()
"""
if __name__ == "__main__":
    c = client()
    c.connect()
    c.run()
