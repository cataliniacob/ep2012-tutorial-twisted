from twisted.internet import endpoints, protocol, reactor
from twisted.protocols import basic
from twisted.web.client import getPage

import time

class ProxyProtocol(basic.LineReceiver):
    def lineReceived(self, line):
        if not line.startswith('http://'):
            return

        start = time.time()

        print 'Fetching {}'.format(line)
        def gotPage(data):
            print 'Fetched {} in {} sec'.format(line, time.time() - start)
            self.transport.write(data)

        def errGettingPage(reason):
            print 'Error while fetching {}: {}'.format(line, reason.getErrorMessage())

        d = getPage(line)
        d.addCallback(gotPage)
        d.addErrback(errGettingPage)

if __name__ == '__main__':
    factory = protocol.ServerFactory()
    factory.protocol = ProxyProtocol
    endpoints.serverFromString(reactor, 'tcp:8000').listen(factory)

    reactor.run()
