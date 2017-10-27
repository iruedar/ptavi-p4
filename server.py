#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    diccserv = {}
    def handle(self):
        lista = []
        for line in self.rfile:
            lista.append(line.decode('utf-8'))
        
        messaje = lista[0].split(':')
        user = messaje[1].split(' ')[0]
        method = mensaje[0].split(' ')[0]
        if method == 'REGISTER':
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            IP = self.client_address[0]
            PORT = self.client_address[1]
            self.diccserv[user] = (IP + ':' + str(PORT))
            print(self.diccserv)
           

if __name__ == "__main__":
    LISTEN_PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', LISTEN_PORT), SIPRegisterHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
