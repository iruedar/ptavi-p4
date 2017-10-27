#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):

    dicc = {}
    def handle(self):
        lista = []
        for line in self.rfile:
            lista.append(line.decode('utf-8'))
        
        IP = self.client_address[0]
        PORT = self.client_address[1]
        CLIENT = IP + ':' + str(PORT)
        message = lista[0].split(':')
        user = message[1].split(' ')[0]
        method = message[0].split(' ')[0]
        expires = lista[1].split('\r\n')[0]
        expires = expires.split(' ')[1]
        if method == 'REGISTER':
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            self.dicc[user] = (CLIENT + str(expires))
        if int(expires) == 0:
            try:
                del self.dicc[user]
                print('User', user, 'in', CLIENT, 'deleted\n')
            except KeyError:
                print('User', user, 'not found\n')
        else:
            print('User', user, 'in', CLIENT)
            print('Expires in', expires, 'seconds\n')
           
if __name__ == "__main__":
    LISTEN_PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', LISTEN_PORT), SIPRegisterHandler) 

    print('Lanzando servidor UDP de eco...\n')
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
