import socket,select,ClientConfig,threading,os
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
        self.__scriptDir = os.path.dirname(__file__)
        self.__insidePath = "History\\"
        self.filePath = os.path.join(self.__scriptDir,self.__insidePath)
        self.__writables = 1
        self.__id = None
        self.__server_ip = None
        self.__server_port = None
        self.__connected = False
        self.__client = socket.socket()
        self.__alive = True
        self.__ok = False
        self.__src = ""
        self.name = ""
        self.__clientslv = []
        self.__aliveClients = {}
        self.__msg_lst =[]
    def isConnected(self):
        return self.__connected
    def isAlive(self):
        return self.__alive
    def getid(self):
        return self.__id
    def getserveraddr(self):
        return (self.__server_ip,self.__server_port)
    def isConnected(self):
        return self.__connected
    def getclientsoc(self):
        return self.__client
    def setname(self,name):
        self.name = name
    def popmsglst(self):
        a = self.__msg_lst[-1]
        del self.__msg_lst[-1]
        return a
    def getaliveclients(self):
        return self.__aliveClients
    def connect(self,ip,port):
        self.__server_ip = ip
        self.__server_port = port
        self.__server_addr = (self.__server_ip,self.__server_port)
        self.__client.connect(self.__server_addr)
        data = self.__client.recv(ClientConfig.CONN_CONFIRM_SIZE) # get connection confirmation and id from server
        confirm , soc_id = data.split('$') #spliting the information that is seperated by '$' char
        if confirm == ClientConfig.CONN_CONFIRM:
            self.__id = soc_id
            self.__connected = True
            self.__client.send(self.name)
            self.make_aDir(soc_id)   
        
    def make_aDir(self,soc_id):
        with open(self.filePath+'%s.txt'%str(soc_id),'w') as his:
            his.write("")

    def __getList_Clients(self,msg):

        keys,values = msg.split("*")
        self.__clientslv = zip(keys.split('$'),values.split('$'))
        self.__aliveClients = dict(self.__clientslv)
        """
        keys_info = self.__client.recv(int(key_length))
        val_length = self.__client.recv(1024)
        values_info = self.__client.recv(int(val_length))
        self.__clientslv = zip(keys_info.split('$'),values_info.split('$'))
        self.__aliveClients = dict(self.__clientslv)
        print self.__aliveClients
        """
    def get_aliveClients(self):
        return self.__aliveClients
    def name_to_id(self,name):
        return self.__aliveClients.keys()[self.__aliveClients.values().index(name)]
    def close(self):
        self.__client.send(ClientConfig.CLOSE_MSG)
        self.__client.close()
        self.__connected = False
        self.__id = None
        self.__init__()
    def send(self,soc_id,msg):
        if self.__writables:
            self.__client.send(soc_id +'$'+ msg)
            with open(self.filePath+'%s.txt'%str(soc_id),'a+') as his:
                his.write('\n'+msg)
              
    def recv(self):
        
        if self.isConnected():
            if len(self.__readables):
                print "recvd"
                messg = self.__client.recv(1024)
                
                if messg[0] != "&":
                    print "\n"
                    print messg
                    soc_id, msg = messg.split('$')
                    with open(self.filePath+'%s.txt'%str(soc_id),'a+') as his:
                        his.write('\n'+msg)
                else:
                    print "\n"
                    print "got msg"
                    print messg
                    self.__getList_Clients(messg[1:])
                    
    def run(self):
        
        self.__readables , self.__writables , exceptionals = select.select([self.__client],[self.__client],[self.__client])        
        self.recv()
