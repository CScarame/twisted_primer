from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import sys


class InputConnection(Protocol):

    def connectionMade(self):
        print "Sending data:"
        self.transport.write("This is the data")

    def dataReceived(self, data):
        print data
        n = raw_input(">")
        if n == "exit":
            reactor.stop()
            
        else:
            self.transport.write(n)
        
class Add1Connection(Protocol):

    def connectionMade(self):
        print "Connection Made"
        self.transport.write("1")

    def dataReceived(self,data):
        print data
        self.transport.write(str(int(data) + 1))

class CommandConnection(Protocol):
    def connectionMade(self):
        print "Command Connection Received"

class ClientConnection(Protocol):
    def __init__(self, command_conn):
        self.command_conn = command_conn
    def connectionMade(self):
        print "Client Connection Established"

class DataConnection(Protocol):
    def __init__(self, command_conn):
        self.command_conn = command_conn
    def connectionMade(self):
        print "Data Connection Established"

class HomeConnectionFactory(Factory):
    def __init__(self, connection_type):
        self.connection_type = connection_type
	self.command_conn = CommandConnection()
        self.client_conn  = ClientConnection(self.command_conn)
        self.data_conn    = DataConnection(self.command_conn)
    def buildProtocol(self, addr):
        if self.connection_type == "command":
	    return self.command_conn
        elif self.connection_type == "client":
            return self.client_conn
        elif self.connection_type == "data":
            return self.data_conn
reactor.listenTCP( 40052, HomeConnectionFactory("command"))

reactor.run()
