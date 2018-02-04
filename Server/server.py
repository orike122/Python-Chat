import socket,select,ServerConfig
"""
Protocol Description:
every client assigned unique id when connecting
client --------> server - connection
server --------> client - connection confirmation + id
client --------> server - msg details(dst,content)
server --------> client - msg details(src,content)
client --------> server - close request
"""
class server(object):
    def __init__(self):
        self.__ip = ServerConfig.IP
        self.__port = ServerConfig.PORT
        self.__addr = (self.__ip,self.__port)
        self.__maxConn = ServerConfig.MAX_CONN
        self.__server = socket.socket()
        self.__server.bind(self.__addr)
        self.__server.listen(self.__maxConn)
        self.__connections = {0:self.__server}
        self.__connectedName = {}
        self.__next_id = 0
        self.__alive = True
        self.__msg_lst = []
    def getaddr(self):
        return self.__addr
    def __getnextid(self):
        self.__next_id += 1
        return self.__next_id
    def getconns(self):
        return self.__connections
    def getserversoc(self):
        return self.__server
    def isAlive(self):
        return self.__alive
    def __isValid(self,data):
        splt = data.split('$')
        try:
            return (type(int(splt[0])) is int and type(splt[1]) is str)
        except:
            return True
    def __push_msg(self,msg):
        self.__msg_lst.append(msg)
    def __wrap_msg(self,src,data):
        splt = data.split('$')
        msg = (src,int(splt[0]),splt[1])
        return msg# format - (int: src id , int: dst id, str: msg)
    def __format_msg(self,msg):
        src , _ , m = msg
        return str(src) + "$" + m
    def __handle_conn(self):
        soc , addr = self.__server.accept()
        soc_id = self.__getnextid()
        self.__connections[soc_id] = soc
        
        soc.send(ServerConfig.CONN_CONFIRM + '$' + str(soc_id))
        print "accept"
        data = soc.recv(ServerConfig.RECV_SIZE)
        self.__connectedName[str(soc_id)] = str(data)
        print "got name"
        print "%s is connected" % self.__connectedName[str(soc_id)]
        
        self.__broadcast_ls()
    def __broadcast_ls(self):
        print "br"
        for soc_id in self.__connectedName.keys():
            print self.__connectedName
            print "sent to %s"%self.__connections[int(soc_id)]
            soc = self.__id_to_soc(soc_id)
            self.__sendls(soc)
    def __id_to_soc(self,soc_id):
        return self.__connections[int(soc_id)]
    def __sendls(self,soc):
        dic = self.__connectedName.copy()
        send_msg = "&"+'$'.join(dic.keys())+"*"+'$'.join(dic.values())
        print send_msg
        soc.send(send_msg)
        """
        soc.send("&"+"0"*(1023 - len('$'.join(self.__connectedName.keys())))+str(len('$'.join(self.__connectedName.keys()))))
        soc.send('$'.join(self.__connectedName.keys()))
        print '$'.join(self.__connectedName.keys())
        soc.send("0"*(1024 - len('$'.join(self.__connectedName.values())))+str(len('$'.join(self.__connectedName.values()))))
        soc.send('$'.join(self.__connectedName.values()))
        print '$'.join(self.__connectedName.values())
        """
    def __handle_close(self,soc_id):
        
        self.__connections[soc_id].close()
        name = self.__connectedName[str(soc_id)]
        del self.__connections[soc_id]
        del self.__connectedName[str(soc_id)]
        print "%s (%d) disconnected" % (name, soc_id)
        self.__broadcast_ls()

    def __handle_income(self,soc):
        data = soc.recv(ServerConfig.RECV_SIZE)
        print data
        soc_id = self.__connections.keys()[self.__connections.values().index(soc)]
        if data[0] == "~":
            if self.__isValid(data[1:]):
                for soc_id in self.__connections.keys():
                    self.__push_msg(self.__wrap_msg(soc_id,data[1:]))
        if data == "BYE":
            self.__handle_close(soc_id)
            return
        if not data:
            self.__handle_close(soc_id)
            print 
        else:
            if self.__isValid(data):
                self.__push_msg(self.__wrap_msg(soc_id,data))
    def __handle_outcome(self,soc):
        soc_id = self.__connections.keys()[self.__connections.values().index(soc)]
        for m in self.__msg_lst:
            _,dst_id,_ = m
            if soc_id == dst_id:
                soc = self.__connections[dst_id]
                print self.__format_msg(m)
                soc.send(self.__format_msg(m))
                self.__msg_lst.remove(m)
    #need to add send client names
    def run(self):
        while self.__alive:            
            inputs = self.__connections.values()
            readables , writables , exceptionals = select.select(inputs, inputs, inputs)
            if len(readables):
                for soc in readables:
                    if soc is self.__server:
                        self.__handle_conn()
                    else:
                        self.__handle_income(soc)
            inputs = self.__connections.values()
            readables , writables , exceptionals = select.select(inputs, inputs, inputs)
            if len(writables):
                for soc in writables:
                    self.__handle_outcome(soc)
                    
            
            

if __name__ == "__main__":
    s = server()
    s.run()
