from twisted.internet import protocol, reactor

factory = protocol.ServerFactory()
factory.protocol = protocol.Protocol

reactor.listenTCP(8000, factory)
reactor.run()
