#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 15:46:01 2019

@author: laura
"""

import socket
import sys
import git
import datetime
import hashlib                   # Import socket module

port = 12000                    # Reserve a port for your service.
s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(2) 

repoLocal = git.Repo( '/' )
x = datetime.datetime.now()
nameFile="/Servidor/Logs/"+x+".txt"
f= open(nameFile,"w+")                    # Now wait for client connection.

print ('Server listening....')

while True:
    conn, addr = s.accept()     # Establish connection with client.
    print ('Got connection from', addr)
    data = conn.recv(5)
    x = datetime.datetime.now()
    f.write(x+"-Recibido listo conexion, ")
    
    print('Server received', repr(data))

    filename='mytext.txt'
    f = open(filename,'rb')
    l = f.read(1024)
    while (l):
       conn.send(l)
       print('Sent ',repr(l))
       l = f.read(1024)
    f.close()

    print('Done sending')
    conn.send('Thank you for connecting')
    conn.close()