from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor

class MyConnection(Protocol):

    def connectionMade(self):
        print "new connection made" 



class MyConnectionFactory(ClientFactory):
    def __init__(self):
        self.myconn = MyConnection()

    def buildProtocol(self, addr):
        return self.myconn


reactor.connectTCP("ash.campus.nd.edu", 40052, MyConnectionFactory())

reactor.run()
