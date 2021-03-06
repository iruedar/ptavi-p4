#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Servidor de eco en UDP simple con handle de registro."""

import sys
import json
import socketserver

from datetime import datetime, date, time, timedelta


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """SIP Register and save users in .json file."""

    dicc = {}

    def json2registered(self):
        """Ver si registered.json existe."""
        try:
            with open('registered.json', 'r') as json_file:
                self.dicc = json.load(json_file)
        except:
            pass

    def register2json(self):
        """Crea registered.json file."""
        with open('registered.json', 'w') as json_file:
            json.dump(self.dicc, json_file, indent=3)

    def handle(self):
        lista = []
        client = {'address': '', 'expires': ''}
        IP = self.client_address[0]
        PORT = self.client_address[1]
        FORMAT = '%Y-%m-%d %H:%M:%S'
        address = IP + ':' + str(PORT)
        for line in self.rfile:
            lista.append(line.decode('utf-8'))

        message = lista[0].split()
        method = message[0].split()[0]
        """Se comprueba que el primer campo sea REGISTER."""
        if method == 'REGISTER':
            user = message[1].split(':')[1]
            message = lista[1].split()
            sec = message[1].split('\r\n')[0]
            expires = datetime.now() + timedelta(seconds=int(sec))
            date = expires.strftime(FORMAT)
            client['address'] = address
            client['expires'] = date
            if int(sec) == 0:
                try:
                    del self.dicc[user]
                    print('User', user, 'in', address, 'deleted\n')
                except KeyError:
                    print('User', user, 'not found\n')
            else:
                self.dicc[user] = client
                print('User', user, 'in', address)
                print('Expires in', expires)
            Del_lista = []
            now = datetime.now().strftime(FORMAT)
            for user in self.dicc:
                if self.dicc[user]['expires'] <= now:
                    Del_lista.append(user)
            for user in Del_lista:
                del self.dicc[user]
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            self.register2json()

if __name__ == "__main__":
    try:
        LISTEN_PORT = int(sys.argv[1])
    except IndexError:
        sys.exit('Usage: server.py puerto')
    serv = socketserver.UDPServer(('', LISTEN_PORT), SIPRegisterHandler)
    print('Lanzando servidor UDP de eco...\n')

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
