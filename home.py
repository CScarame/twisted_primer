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

class HomeConnectionFactory(Factory):
    def __init__(self, connection_type):
        self.connection_type = connection_type
        self.input_conn = InputConnection()
        self.add1_conn = Add1Connection()
	self.command_conn = CommandConnection()
    def buildProtocol(self, addr):
        if self.connection_type == "input":
            return self.input_conn
        elif self.connection_type == "add1":
            return self.add1_conn
        elif self.connection_type == "command":
	    return self.command_conn
reactor.listenTCP( 40052, HomeConnectionFactory("command"))

reactor.run()
