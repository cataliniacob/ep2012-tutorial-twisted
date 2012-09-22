from twisted.internet import endpoints, protocol, reactor

class UpperProtocol(protocol.Protocol):
    def connectionMade(self):
        self.transport.write('Hi! Send me some text to convert to uppercase\n')

        self.factory.client_count += 1
        print 'New connection from {0.host}:{0.port}, have {1} clients'.format(self.transport.getPeer(), self.factory.client_count)

    def connectionLost(self, reason):
        self.factory.client_count -= 1

        print 'Lost connection from {0.host}:{0.port}'.format(self.transport.getPeer())

    def dataReceived(self, data):
        self.transport.write(data.upper())

class CountingServerFactory(protocol.ServerFactory):
    protocol = UpperProtocol
    client_count = 0

factory = CountingServerFactory()
endpoints.serverFromString(reactor, 'tcp:8000').listen(factory)

reactor.run()
