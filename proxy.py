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

        data = self.factory.cache.get(line, None)
        if data is not None:
            print 'Using cache for {}'.format(line)
        else:
            print 'Fetching {}'.format(line)
            try:
                data = yield getPage(line)
            except Exception as e:
                print 'Error while fetching {}: {}'.format(line, e)
            else:
                print 'Fetched {} in {} sec'.format(line, time.time() - start)
                self.factory.cache[line] = data

        if data is not None:
            self.transport.write(data)

class CachingProxyServerFactory(protocol.ServerFactory):
    protocol = ProxyProtocol
    cache = {}

if __name__ == '__main__':
    factory = CachingProxyServerFactory()
    endpoints.serverFromString(reactor, 'tcp:8000').listen(factory)

    reactor.run()
