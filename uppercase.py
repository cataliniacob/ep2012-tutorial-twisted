from twisted.internet import endpoints, protocol, reactor

class UpperProtocol(protocol.Protocol):
    def connectionMade(self):
        self.transport.write('Hi! Send me some text to convert to uppercase\n')

    def dataReceived(self, data):
        self.transport.write(data.upper())

factory = protocol.ServerFactory()
factory.protocol = UpperProtocol

endpoints.serverFromString(reactor, 'tcp:8000').listen(factory)
reactor.run()
