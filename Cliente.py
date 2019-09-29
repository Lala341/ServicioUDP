#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 07:16:39 2019

@author: laura
"""

import socket
import sys
import git
import datetime
import hashlib


#Local repo on your computer
repoLocal = git.Repo( '/' )
x = datetime.datetime.now()
nameFile="/Cliente/Logs/"+x+".txt"
f= open(nameFile,"w+")


hasher = hashlib.md5()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# Conecta el socket en el puerto cuando el servidor esté escuchando
server_address = ('localhost', 12000)
print (sys.stderr, 'conectando a %s puerto %s' % server_address)
sock.connect(server_address)
x = datetime.datetime.now()
f.write(x+"-Cliente conectado puerto")
men1="INICIOENVIO"
num=0
hashfileserver=""
datacontent=""
try:
     
    # Enviando datos

    message = 'LISTO'
    print (sys.stderr, 'enviando "%s"' % message)
    sock.sendall(message)
    x = datetime.datetime.now()
    f.write(x+"-Enviado LISTO")
    nom= sock.recv(10)
    
    nameFilear="/Cliente/Archivos/"+x+"-"+nom
    far= open(nameFilear,"w+")
    
    while True:
        data = sock.recv(11)
        if ("INICIOENVIO-" in data):
            
            num= sock.recv(7)
            num=int(num)
            x = datetime.datetime.now()
            f.write(x+"-Inicio Envio"+num)
            print ('Recibiendo "%s"' % data)
            break
            
    j=num
    m=1024
    
    while 0<j:
        print('receiving data...')
        if(j<1024):
            m=j
        data = s.recv(m)
        far.write(data)
        print('data=%s', (data))
        x = datetime.datetime.now()
        f.write(x+"-Receiving data-Paquete "+i+" de "+num)
        datacontent=data
        hasher.update(data)
        j=j- 1024
    
    x = datetime.datetime.now()
    f.write(x+"-Se recibio archivo de  "+len(datacontent)+" B ")
        
    while True:
        data = sock.recv(4)
        if ("HASH" in data):
            
            hashfileserver= sock.recv(1024)
            x = datetime.datetime.now()
            f.write(x+"-Recibe hash de servidor : "+hashfileserver)
            print ('Recibiendo "%s"' % data)
            break
finally:
    hashfile=hasher.hexdigest()
    x = datetime.datetime.now()
    f.write(x+"-Este es el hash calculado por el cliente: "+hashfile)
    
    if(hashfile==hashfileserver):
        x = datetime.datetime.now()
        f.write(x+"-Se recibio correctamente el archivo.")
    else:
        x = datetime.datetime.now()
        f.write(x+"-No se recibio correctamente el archivo.")
    print(sys.stderr, 'cerrando socket')
    sock.close()
    x = datetime.datetime.now()
    f.write(x+"-Socket cerrado")
    far.close()
    f.close()
    repo.git.add(".")
    repo.git.commit(m='Adding logs via python')
    origin = repo.remote('origin')
    origin.push()