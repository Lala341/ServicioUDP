#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 08:54:36 2019

@author: juan
"""

import socket
import struct
import sys
import math
import datetime
import time, hashlib

message = 'LISTO-PARA-RECIBIR'
addr = ('224.3.29.71', 10220)
buf = 1024
CHUNK_SIZE = 1024
# Create the datagram socket
x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
nameFile="./Cliente/Logs/"+"C-"+x+".txt"
f= open(nameFile,"w+")

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
sock.settimeout(0.2)

# Set the time-to-live for messages to 1 so they do not
# go past the local network segment.
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
f.write(x+"-Cliente conectado puerto"+'\n')

#Archivo
hasher = hashlib.md5()

#resultado = "resultado.jpg"
cont=1
try:
    # Send data to the multicast group
    print('sending {!r}'.format(message))
    sent = sock.sendto(message, addr)
    # Look for responses from all recipients
    
    while True:
        print('Requesting info')
        try:
            #data, server = sock.recvfrom(buf)
            
            
            #with open(resultado, "wb") as f:  
                
            
            longitud = sock.recv(2)
            impro = 25 + int(longitud)
            print(str(longitud))
            temp, server= sock.recvfrom(impro)
            no = str(temp).split('-')
            cli = no[0]
            nombrea = no[1]
            tamano = no[2]
            hasr = no[3]
            cont = 1
            num = math.ceil(int(tamano)/1024.0)
            num = int(num)
            nameFilear="./Cliente/Archivos/"+cli+"--"+nombrea
            far = open(nameFilear,'wb')
            print (hasr)
            instanteInicial = datetime.datetime.now()
            for i in range(num):
                print('Recibiendo archivo numero '+str(cont)+' de '+str(num))
                x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
                f.write(x+"-Receiving data-Paquete "+str(cont)+" de "+str(num)+'\n')
                cont += 1
                data = sock.recv(1024)
                far.write(data)
            instanteFinal = datetime.datetime.now()     
            tiempo = instanteFinal - instanteInicial
            f.write(x+"-Tiempo total de transferencia "+str(tiempo)+'\n')
            far.close()
            
            data, server = sock.recvfrom(CHUNK_SIZE)
            print (data)
            while data:
                f.write(data)
                data, server = sock.recvfrom(CHUNK_SIZE)
        except socket.timeout:
            print('timed out, no more responses')
            
            with open(nameFilear, 'rb') as afile:
                aa = afile.read()
                hasher.update(aa)
                hashene = hasher.hexdigest()
                f.write(x+"-Este es el hash calculado por el servidor: "+hasr+'\n')
                print (hasr)
                f.write(x+"-Este es el hash calculado por el cliente: "+hashene+'\n')
                print (hashene)
            if hasr == hashene:
                print("COINCIDEN LOS HASH")
                f.write(x+"-EL ARCHIVO ESTA SIN ERRORES"+'\n')
                message = 'RECIBIDO'
            
            else:
               print('NO COINCIDEN - ERRORES EN EL ENVIO')
               f.write(x+"-!!!!!!EL ARCHIVO PRESENTA ERRORES"+'\n')
               message = 'ERRORES!' 
            break
        else:
            print('received {!r} from {}'.format(
                data, server))

finally:
    print('closing socket')
    sock.close()