#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import socketserver
from datetime import datetime, date, time, timedelta


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    dicc = {}

    def register2json(self):
        with open('registered.json', 'w') as json_file:
            json.dump(self.dicc, json_file, indent=3)

    def handle(self):

        lista = []
        client = {'address':'', 'expires':''}
        IP = self.client_address[0]
        PORT = self.client_address[1]
        address = IP + ':' + str(PORT)
        for line in self.rfile:
            lista.append(line.decode('utf-8'))
        
        message = lista[0].split()
        method = message[0].split()[0]
        if method == 'REGISTER':
            user = message[1].split(':')[1]
            message = lista[1].split()
            sec = message[1].split('\r\n')[0]
            expires = time.time() + int(sec)
            expired = 
        if int(sec) == 0:
            try:
                del self.dicc[user]
                print('User', user, 'in', address, 'deleted\n')
            except KeyError:
                print('User', user, 'not found\n')
        else:
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            self.dicc[user] = (client)
            print('User', user, 'in', address)
            print('Expires in', expires, 'seconds\n')
        self.register2json()
           
if __name__ == "__main__":
    LISTEN_PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', LISTEN_PORT), SIPRegisterHandler) 

    print('Lanzando servidor UDP de eco...\n')
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
	print("Finalizado servidor")

esto es una prueba
