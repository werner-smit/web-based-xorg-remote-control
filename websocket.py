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

class Router(Protocol):
    """Echo uppercased."""
    def dataReceived(self, data):
        #log.msg("Got %r" % (data,))
        #self.transport.write(data.upper())
        action = data.split(':')[0].strip()
        value = data.split(':')[1] if len(data.split(':')) > 1 else ''
        dispatcher.dispatch(self.transport, action, value)


class Dispatcher(object):
    
    klass = None
    def __init__(self, klass):
        self.klass = klass
        log.msg('starting dispatcher')

    def dispatch(self,transport, action, data):
        self.klass.set_transport(transport)
        handler_name = '_handler_%s' % action
        #log.msg('handler: %s' % handler_name)

        if hasattr(self.klass, handler_name):
            handler_func = getattr(self.klass, handler_name)
            response = handler_func(data)
            if response:
                transport.write(response)
        else:
            #transport.write(dir(self))
            transport.write('Cant find handler for %s' % handler_name)


class Recorder(object):
    trans = None
    
    def __init__(self):
        log.msg('Starting recorder.')
        self.x = XClass()
        pass

    def set_transport(self,transport):
        if not self.trans:
            self.trans = transport
    
    def _handler_move(self, data_str):
        x,y = data_str.split(',')
        self.x.set_pointer(int(x), int(y))

    def _handler_start_record(self, value):
        global recording
        recording = []
        self.trans.write('Recording..')

    def _handler_track(self, data_str):
        recording.append(data_str.split(','))

    def _handler_stop_record(self, value):
        log.msg("playing back %s movements" % len(recording))
        _x = XClass()
        self.trans.write('Recording stopped...')
        time.sleep(3)
        for x, y in recording:
            #log.msg('%s, %s' % (int(x),int(y)))
            _x.set_pointer(int(x), int(y))
            time.sleep(0.01)

dispatcher = Dispatcher(Recorder())

application = Application("ws-streamer")

echofactory = Factory()
echofactory.protocol = Router # use Factory.buildProtocol()
service = strports.service("tcp:8076:interface=127.0.0.1",
                           WebSocketFactory(echofactory))
service.setServiceParent(application)

from twisted.web.server import Site
from twisted.web.static import File
import os
resource = File(os.path.join(os.path.dirname(__file__))) #' serve current directory
webservice = strports.service("tcp:8081:interface=0.0.0.0",
                              Site(resource))
webservice.setServiceParent(application)
