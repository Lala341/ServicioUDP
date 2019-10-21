#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 08:54:53 2019

@author: juan
"""

import socket
import struct
import sys
import hashlib
import math
import git
import datetime
import os

multicast_group = '224.3.29.71'
server_address = ('', 10220)
buf = 1024
CHUNK_SIZE = 1024
# Create the socket

# Create the datagram socket
x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
nameFile="./Servidor/Logs/"+"C-"+x+".txt"
f= open(nameFile,"w+")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)
# Tell the operating system to add the socket to
# the multicast group on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    mreq)
#Archivo de prueba

x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
nameFile="./"+"C-"+x+".txt"
f= open(nameFile,"w+")

print ('que archivo quiere transferir?')
print ('1. Texto 100MB')
print ('2. Imagen 250MB')
archivo = int(input())
cliente = 0;

if archivo == 1:
    nom = 'test01.mov'
else:
    nom = 'test02.jpg'
    
f.write(x+" El servidor va a enviar archivos con el nombre: "+nom+'\n')
    
hasher = hashlib.md5()

with open(nom, 'rb') as afile:
    buf = afile.read()
    hasher.update(buf)
    hashen = hasher.hexdigest()
    
afile.close()
direcciones = []
sizefile = (os.stat(nom).st_size)
#f=open(file_name,"rb")
#arch = f.read(buf)
# Receive/respond loop
while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(18)        
    if data == 'LISTO-PARA-RECIBIR':               
        sock.sendto(str(len(str(hashen))),address)
        if cliente == 1 or cliente==2 or cliente==3 or cliente==4 or cliente==5 or cliente==6 or cliente==7 or cliente==8 or cliente==9:
                cl = '0'+str(cliente)
        sock.sendto(str(cliente)+'-'+nom+'-'+str(sizefile)+'-'+str(hashen),address)
        print(str(cliente)+'-'+nom+'-'+str(sizefile)+'-'+str(hashen),address)
        with open(nom, "rb") as f:        
            arch = f.read(CHUNK_SIZE)
            while arch:
                sock.sendto(arch, address)
                arch = f.read(CHUNK_SIZE)
