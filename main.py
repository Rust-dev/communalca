# -*- coding: utf-8 -*-
from __future__ import print_function

from kivy.support import install_twisted_reactor

install_twisted_reactor()

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

from twisted.internet import reactor, protocol

import os

__version__ = '1.0.0'
#main_file_dir = os.path.dirname(os.path.abspath(__file__))
#gui = Builder.load_file((main_file_dir + '/communalca.kv'))

class CommunalcaClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connect(self.transport)


class CommunalcaClientFactory(protocol.ClientFactory):
    protocol = CommunalcaClient

    def __init__(self, app):
        self.app = app


class CommunalcaApp(App):

    #def build(self):
        #return gui
    def build_config(self, config):
        config.setdefaults('section1', {
            'key1': 'value1'})
    def change_config(self):
        with open('communalca.ini', 'w') as f:
            print('[section1]', file=f)
            print('key1 = ' + self.root.ids.server.text, file=f, end='')
        
    def connect_to_server(self):
        host = self.root.ids.server.text
        reactor.connectTCP(host, 8000,
                           CommunalcaClientFactory(self))

    def disconnect_from_server(self):
        if self.conn:
            self.conn.loseConnection()
            del self.conn
        self.root.current = 'login'
    
    def send_data_to_server(self, *args):
        msg = {'T1': self.root.ids.T1.text,
        'T2': self.root.ids.T2.text,
        'T3': self.root.ids.T3.text,
        'W1': self.root.ids.W1.text,
        'W2': self.root.ids.W2.text,
        'W3': self.root.ids.W3.text,
        'W4': self.root.ids.W4.text}
        if msg and self.conn:
            self.conn.write(str(msg))

    def on_connect(self, conn):
        self.conn = conn
        self.root.current = 'svet'

    def switch_to_svet(self):
        self.root.current = 'svet'
    
    def switch_to_voda(self):
        self.root.current = 'voda'
    
    def switch_to_main(self):
        self.root.current = 'main'
    
    def clear_IP(self):
        self.root.ids.server.text = ''  

if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('#1f7763')
    CommunalcaApp().run()
