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
        print "command connection made"


class DataConnection(Protocol):
    

class WorkConnectionFactory(ClientFactory):
    def __init__(self, connection_type):
	self.connection_type = connection_type
	self.myconn = MyConnection()
        self.command_conn = CommandConnection()
    def buildProtocol(self, addr):
        if self.connection_type = "test":
            return self.myconn
        elif self.connection_type = "command":
            return self.command_conn

reactor.connectTCP("localhost", 40052, MyConnectionFactory("command"))

reactor.run()
