from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import sys


class InputConnection(Protocol):

    def connectionMade(self):
        #print "Sending data:"
        self.transport.write("This is the data")

    def dataReceived(self, data):
        #print data
        n = raw_input(">")
        if n == "exit":
            reactor.stop()
            
        else:
            self.transport.write(n)

class CommandConnection(Protocol):
    def connectionMade(self):
        #print "Command Connection Received"
        # wait for client to connect
        reactor.listenTCP(42052, HomeConnectionFactory("client", self))
    #def dataReceived(self, data):
        #print "command: ",
        #print data

class ClientConnection(Protocol):
    def __init__(self, command_conn):
        self.command_conn = command_conn
        self.data_conn = None
        self.data = None
    def connectionMade(self):
        #print "Client Connection Established"
        # now set up data connection
        reactor.listenTCP(41052, HomeConnectionFactory("data", self.command_conn, self))
        self.command_conn.transport.write("connect")
    def dataReceived(self, data):
        #print "client: ",
        #print data
        if self.data_conn:
            self.data_conn.transport.write(data)
        #else:
            #print "client: Storing data until data connection finishes"
            
    def passData(self, data_connection):
        self.data_conn = data_connection
        
class DataConnection(Protocol):
    def __init__(self, command_conn, client_conn):
        self.command_conn = command_conn
        self.client_conn = client_conn
    def connectionMade(self):
        #print "Data Connection Established"
        self.client_conn.passData(self)
    def dataReceived(self,data):
        self.client_conn.transport.write(data)

class HomeConnectionFactory(ClientFactory):
    def __init__(self, connection_type, command = None, client = None):
        self.connection_type = connection_type
        if command:
            self.command_conn = command
        else:
            self.command_conn = CommandConnection()
        if client:
            self.client_conn = client
        else:
            self.client_conn  = ClientConnection(self.command_conn)
        self.data_conn    = DataConnection(self.command_conn, self.client_conn)
    def buildProtocol(self, addr):
        if self.connection_type == "command":
	    return self.command_conn
        elif self.connection_type == "client":
            return self.client_conn
        elif self.connection_type == "data":
            return self.data_conn

if __name__ == "__main__":
    reactor.listenTCP( 40052, HomeConnectionFactory("command"))

reactor.run()
