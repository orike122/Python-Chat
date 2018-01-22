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
        self.__next_id = 0
        self.__alive = True
        #self.__msg_queue = Queue.Queue(10)
        #self.__server.setblocking(ServerConfig.CONN_TIMEOUT)
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
            print("shit")
            return True
    def __push_msg(self,msg):
        self.__msg_lst.append(msg)
    # def __pop_msg(self):
    #     return self.__msg_queue.get()
    def __wrap_msg(self,src,data):
        splt = data.split('$')
        print splt
        msg = (src,int(splt[0]),splt[1])
        print msg
        return msg# format - (int: src id , int: dst id, str: msg)
    def __format_msg(self,msg):
        src , _ , m = msg
        return str(src) + '$' + m
    def __handle_conn(self):
        #self.__server.setblocking(ServerConfig.CONN_TIMEOUT)
        soc , addr = self.__server.accept()
        #self.__server.setblocking(1)
        soc_id = self.__getnextid()
        self.__connections[soc_id] = soc
        soc.send(ServerConfig.CONN_CONFIRM + '$' + str(soc_id))
    def __handle_close(self,id):
        self.__connections[id].close()
        del self.__connections[id]
    def __handle_income(self,soc):
        data = soc.recv(ServerConfig.RECV_SIZE)
        print data + 'h'
        soc_id = self.__connections.keys()[self.__connections.values().index(soc)]
        if not data:
            self.__handle_close(soc_id)
        else:
            if self.__isValid(data):
                self.__push_msg(self.__wrap_msg(soc_id,data))
    def __handle_outcome(self,soc):
        soc_id = self.__connections.keys()[self.__connections.values().index(soc)]
        for m in self.__msg_lst:
            _,dst_id,_ = m
            if soc_id == dst_id:
                soc = self.__connections[dst_id]
                soc.send(self.__format_msg(m))
    def run(self):
        #self.__server.setblocking(0)
        while self.__alive:
            inputs = self.__connections.values()
            readables , writables , exceptionals = select.select(inputs, inputs, inputs)
            if len(readables):
                for soc in readables:
                    if soc is self.__server:
                        self.__handle_conn()
                    else:
                        self.__handle_income(soc)
            if len(writables):
                for soc in writables:
                    self.__handle_outcome(soc)

if __name__ == "__main__":
    s = server()
    s.run()
