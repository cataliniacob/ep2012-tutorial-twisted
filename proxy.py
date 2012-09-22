from twisted.internet import endpoints, protocol, reactor
from twisted.protocols import basic
from twisted.web.client import getPage

import time

class ProxyProtocol(basic.LineReceiver):
    def gotPage(self, data, line, start):
        print 'Fetched {} in {} sec'.format(line, time.time() - start)
        self.transport.write(data)

    def errGettingPage(self, reason, line):
        print 'Error while fetching {}: {}'.format(line, reason.getErrorMessage())

    def lineReceived(self, line):
        if not line.startswith('http://'):
            return

        start = time.time()
        print 'Fetching {}'.format(line)
        d = getPage(line)

        d.addCallback(self.gotPage, line, start)
        d.addErrback(self.errGettingPage, line)

if __name__ == '__main__':
    factory = protocol.ServerFactory()
    factory.protocol = ProxyProtocol
    endpoints.serverFromString(reactor, 'tcp:8000').listen(factory)

    reactor.run()
