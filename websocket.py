""""
Install: pip install twisted txws

Run: twistd -ny streamer.py

Visit http://localhost:8080/
"""
import time
from twisted.application import strports # pip install twisted
from twisted.application.service import Application
from twisted.internet.protocol import Factory, Protocol
from twisted.python import log

from txws import WebSocketFactory # pip install txws

from xlib import XClass
recording = []

class Dispatcher(Protocol):
    """Echo uppercased."""
    start_time = None
    def dataReceived(self, data):
        #log.msg("Got %r" % (data,))
        #self.transport.write(data.upper())
        action = data.split(':')[0].strip()
        value = data.split(':')[1] if len(data.split(':')) > 1 else ''
        handler_name = '_hander_%s' % action
        log.msg('handler: %s' % handler_name)
        if hasattr(self, handler_name):
            handler_func = getattr(self, handler_name)
            response = handler_func()
            if response:
                self.transport.write(response)
        else:
            self.transport.write(dir(self))
            #self.transport.write('Cant find handler for %s' % handler_name)
    def _handler_start_record(self,value):
        global recording
        recording = []
        self.transport.write('Recording..')

    def _handler_track(self, data_str):
        recording.append(data_str.split(','))

    def _handler_stop_record(self, value):
        _x = XClass()
        self.transport.write('Recording stopped...')
        time.sleep(3)
        for x, y in recording:
            _x.set_pointer(x,y)
            time.sleep(0.1)



application = Application("ws-streamer")

echofactory = Factory()
echofactory.protocol = Dispatcher # use Factory.buildProtocol()
service = strports.service("tcp:8076:interface=127.0.0.1",
                           WebSocketFactory(echofactory))
service.setServiceParent(application)

from twisted.web.server import Site
from twisted.web.static import File

resource = File('.') # serve current directory
webservice = strports.service("tcp:8081:interface=127.0.0.1",
                              Site(resource))
webservice.setServiceParent(application)
