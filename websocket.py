# -*- test-case-name: test_streamer -*-
"""WebSocket Echo.

Install: pip install twisted txws

Run: twistd -ny streamer.py

Visit http://localhost:8080/
"""
from twisted.application import strports # pip install twisted
from twisted.application.service import Application
from twisted.internet.protocol import Factory, Protocol
from twisted.python import log

from txws import WebSocketFactory # pip install txws

class EchoUpper(Protocol):
    """Echo uppercased."""
    def dataReceived(self, data):
        log.msg("Got %r" % (data,))
        self.transport.write(data.upper())

application = Application("ws-streamer")

echofactory = Factory()
echofactory.protocol = EchoUpper # use Factory.buildProtocol()
service = strports.service("tcp:8076:interface=127.0.0.1",
                           WebSocketFactory(echofactory))
service.setServiceParent(application)

from twisted.web.server import Site
from twisted.web.static import File

resource = File('.') # serve current directory
webservice = strports.service("tcp:8081:interface=127.0.0.1",
                              Site(resource))
webservice.setServiceParent(application)
