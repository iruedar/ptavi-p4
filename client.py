#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""
import sys
import socket


USAGE = 'client.py ip port register sip_address expires_value'
try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    METHOD = str.upper(sys.argv[3])
    USER = sys.argv[4]
    EXPIRES = int(sys.argv[5])
    REGISTERSIP = METHOD + ' sip:' + USER + ' SIP/2.0\r\n'
    EXPIRESSIP = 'Expires: ' + str(EXPIRES) + '\r\n\r\n'
except IndexError:
    sys.exit('Usage: ' + USAGE)


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    print('Enviando: ' + REGISTERSIP + EXPIRESSIP)
    my_socket.send(bytes(REGISTERSIP + EXPIRESSIP, 'utf-8'))
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))


print("Socket terminado.")
