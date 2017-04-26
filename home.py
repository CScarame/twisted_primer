from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor

class MyConnection(Protocol):

    def connectionMade(self):
        print "new connection made" 



class MyConnectionFactory(ServerFactory):
    def __init__(self):
        self.myconn = MyConnection()

    def buildProtocol(self, addr):
        return self.myconn


reactor.listenTCP( 40001, MyConnectionFactory())

reactor.run()
