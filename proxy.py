from twisted.internet import defer, endpoints, protocol, reactor
from twisted.protocols import basic
from twisted.web.client import getPage

import time

class ProxyProtocol(basic.LineReceiver):
    def lineReceived(self, line):
        if not line.startswith('http://'):
            return

        self.getPage(line)

    @defer.inlineCallbacks
    def getPage(self, line):
        start = time.time()

        print 'Fetching {}'.format(line)
        try:
            data = yield getPage(line)
        except Exception as e:
            print 'Error while fetching {}: {}'.format(line, e)
        else:
            print 'Fetched {} in {} sec'.format(line, time.time() - start)
            self.transport.write(data)

if __name__ == '__main__':
    factory = protocol.ServerFactory()
    factory.protocol = ProxyProtocol
    endpoints.serverFromString(reactor, 'tcp:8000').listen(factory)

    reactor.run()
