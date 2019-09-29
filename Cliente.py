#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 07:16:39 2019

@author: laura
"""

import socket
import sys
 
# Creando un socket TCP/IP

import git
#Local repo on your computer
repoLocal = git.Repo( '/' )

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# Conecta el socket en el puerto cuando el servidor esté escuchando
server_address = ('localhost', 12000)
print (sys.stderr, 'conectando a %s puerto %s' % server_address)
sock.connect(server_address)

try:
     
    # Enviando datos
    message = 'Este es el mensaje.  Se repitio.'
    print (sys.stderr, 'enviando "%s"' % message)
    sock.sendall(message)
 
    # Buscando respuesta
    amount_received = 0
    amount_expected = len(message)
     
    while amount_received < amount_expected:
        data = sock.recv(19)
        amount_received += len(data)
        print (sys.stderr, 'recibiendo "%s"' % data)
 
finally:
    print(sys.stderr, 'cerrando socket')
    sock.close()
    repo.git.add(".")
    repo.git.commit(m='Adding cambios via python')