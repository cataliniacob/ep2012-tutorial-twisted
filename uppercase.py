from twisted.internet import endpoints, protocol, reactor

class UpperProtocol(protocol.Protocol):
    pass

factory = protocol.ServerFactory()
factory.protocol = UpperProtocol

endpoints.serverFromString(reactor, 'tcp:8000').listen(factory)
reactor.run()
