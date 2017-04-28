from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor

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

class DataConnection(Protocol):
    def connectionMade(self):
        print "Data Connection Established"

class ServiceConnection(Protocol):
    def connectionMade(self):
        print "Service Connection Established"
        

class WorkConnectionFactory(ClientFactory):
    def __init__(self, connection_type):
	self.connection_type = connection_type
	self.myconn = MyConnection()
        self.command_conn = CommandConnection()
        self.data_conn    = DataConnection()
        self.service_conn = ServiceConnection()
    def buildProtocol(self, addr):
        if self.connection_type == "test":
            return self.myconn
        elif self.connection_type == "command":
            return self.command_conn
        elif self.connection_type == "data":
            return self.data_conn
        elif self.connection_type == "service":
            return self.service_conn

reactor.connectTCP("10.25.247.41", 40052, WorkConnectionFactory("command"))

reactor.run()
