from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

URL = "ash.campus.nd.edu"


class MyConnection(Protocol):

    def connectionMade(self):
        print "new connection made"

    def dataReceived(self,data):
        print data
        if data == "quit":
            reactor.stop()
        else:
        	self.transport.write(data)
    def connectionLost(self, reason):
	print "connection lost"

class CommandConnection(Protocol):
    def connectionMade(self):
        print "Command Connection Established"
    def dataReceived(self,data):
        #print "command: ",
        #print data
        if data == "connect":
            #print "Connecting Data"
            reactor.connectTCP(URL, 41052, WorkConnectionFactory("data",self))

class DataConnection(Protocol):
    def __init__(self,command):
        self.command_conn = command
        self.service = None
        self.data = DeferredQueue()
    def connectionMade(self):
        #print "Data Connection Established"
        reactor.connectTCP("localhost", 22, WorkConnectionFactory("service", self.command_conn, self))
    def dataReceived(self,data):
        #print "data: ",
        #print data
        self.data.put(data)
    def setService(self, service):
        self.service_conn = service
        #print "Service Connected to data"
        self.data.get().addCallback(self.serveData)
    def serveData(self, data):
        #print "Data SERVED!"
        self.service_conn.transport.write(data)
        self.data.get().addCallback(self.serveData)

class ServiceConnection(Protocol):
    def __init__(self, command, data):
        self.command_conn = command
        self.data_conn = data
    def connectionMade(self):
        #print "Service Connection Established"
        self.data_conn.setService(self)
    def dataReceived(self,data):
        #print "service: ",
        #print data
        self.data_conn.transport.write(data)
        

class WorkConnectionFactory(ClientFactory):
    def __init__(self, connection_type, command_connection = None, data_connection = None):
	self.connection_type = connection_type
	self.myconn = MyConnection()
        if command_connection:
            self.command_conn = command_connection
        else:
            self.command_conn = CommandConnection()
        if data_connection:
                self.data_conn = data_connection
        else:
            self.data_conn    = DataConnection(self.command_conn)
        self.service_conn = ServiceConnection(self.command_conn, self.data_conn)
    def buildProtocol(self, addr):
        if self.connection_type == "test":
            return self.myconn
        elif self.connection_type == "command":
            return self.command_conn
        elif self.connection_type == "data":
            return self.data_conn
        elif self.connection_type == "service":
            return self.service_conn

if __name__ == "__main__":
    reactor.connectTCP(URL, 40052, WorkConnectionFactory("command"))

reactor.run()
