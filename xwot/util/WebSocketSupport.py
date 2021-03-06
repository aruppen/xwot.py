import sys
import logging
import time
import json

try:
    from twisted.web import resource
    from twisted.internet import reactor
    from twisted.python import log
    from twisted.web.server import Site
    from twisted.web.static import File
    from autobahn.twisted.resource import WebSocketResource, HTTPChannelHixie76Aware
    from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
except:
    print 'Some dependendencies are not met'
    print 'You need the following packages: twisted, autobahn, websocket'
    print 'install them via pip'
    sys.exit()


class xWoTStreamerProtocol(WebSocketServerProtocol):
    """
    Very basic WebSocket Protocol. All clients are accepted. Furthermore received messages are fowarded to all clients.
    """

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            msg = "{} from {}".format(payload.decode('utf8'), self.peer)
            self.factory.broadcast(msg)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class xWoTBroadcastFactory(WebSocketServerFactory):
    """
    Broadcasts the State at regular intervalls to all connected clients.
    """

    def __init__(self, url, model, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
        self.clients = []
        self.tickcount = 0
        self.lastbroadcast = 0
        self.olddata = ''
        self.model = model
        self.tick()
        self.acquiredata()
        

    def acquiredata(self):
        localdata = self.model.to_json()

        millis = int(round(time.time() * 1000))
        if (localdata != self.olddata) or (millis - self.lastbroadcast) > 10000:
            self.olddata = localdata
            self.lastbroadcast = millis
            try:
                self.broadcast(localdata)
            except TypeError, e:
                logging.error("no value")
                logging.error(e)
            except Exception:
                logging.error("Something bad happend: ")

        reactor.callLater(1, self.acquiredata)

    def tick(self):
        self.tickcount += 1
        self.broadcast("tick %d from server" % self.tickcount)
        reactor.callLater(299, self.tick)

    def register(self, client):
        if not client in self.clients:
            logging.debug('registered client ' + client.peer)
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            logging.debug("unregistered client " + client.peer)
            self.clients.remove(client)

    def broadcast(self, msg):
        logging.debug("broadcasting prepared message '{}'".format(msg))
        preparedMsg = self.prepareMessage(msg)
        for c in self.clients:
            c.sendPreparedMessage(preparedMsg)
            logging.debug("prepared message sent to {}".format(c.peer))


