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
repo = git.Repo( './' )
x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
nameFile="./Cliente/Logs/"+"C-"+x+".txt"
f= open(nameFile,"w+")


hasher = hashlib.md5()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# Conecta el socket en el puerto cuando el servidor esté escuchando
server_address = ('localhost', 1420)
print (sys.stderr, 'conectando a %s puerto %s' % server_address)
sock.connect(server_address)
x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
f.write(x+"-Cliente conectado puerto")
men1="INICIOENVIO"
num=0
hashfileserver=""
datacontent=""
try:
     
    # Enviando datos

    message = 'LISTO'
    print (sys.stderr, 'enviando "%s"' % message)
    sock.send(message.encode())
    x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
    f.write(x+"-Enviado LISTO")
    temp= sock.recv(12)
    datadec=temp.decode()
    nameFilear="./Cliente/Archivos/Cliente-"+x+"--"+datadec
    far= open(nameFilear,"w+")
    
    while True:
        data = sock.recv(12)
        datadec=data.decode()
        if ("INICIOENVIO-" in datadec):
            num= sock.recv(5).decode()
            print ('Recibiendo ' +num)
            
            num=int(num)
            x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
            f.write(x+"-Inicio Envio"+str(num))
            print ('Recibiendo "%s"' % data)
            break
            
    j=num
    m=1024
    instanteInicial = datetime.datetime.now()
    
    while 0<j:
        print('receiving data...')
        if(j<1024):
            m=j
        data = sock.recv(m)
        datadec=data.decode()
        far.write(datadec)
        print('data=%s', (data))
        x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
        f.write(x+"-Receiving data-Paquete "+str(j)+" de "+str(num))
        datacontent=data
        hasher.update(data)
        j=j- 1024
    instanteFinal = datetime.datetime.now()
    tiempo = instanteFinal - instanteInicial # Devuelve un objeto timedelta
    segundos = tiempo.seconds
    x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
    message = 'RECIBIDO'
    sock.send(message.encode())
    f.write(x+"-Se recibio archivo de  "+str(len(datacontent))+" B .En "+str(segundos)+" segundos")
    far.close()
     
    while True:
        data = sock.recv(4)
        datadec=data.decode()
        if ("HASH" in datadec):
            
            hashfileserver= sock.recv(1024)
            datadec=hashfileserver.decode()
            x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
            f.write(x+"-Recibe hash de servidor : "+datadec)
            print ('Recibiendo "%s"' % datadec)
            break
finally:
    hashfile=hasher.hexdigest()
    x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
    f.write(x+"-Este es el hash calculado por el cliente: "+hashfile)
    
    if(hashfile==hashfileserver):
        x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
        f.write(x+"-Se recibio correctamente el archivo.")
    else:
        x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
        f.write(x+"-No se recibio correctamente el archivo.")
    print(sys.stderr, 'cerrando socket')
    x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
    f.write(x+"-Socket cerrado")
    f.close()
sock.close()
origin = repo.remote('origin')
origin.pull()
repo.git.add(u=True)
repo.git.commit(m='Adding logs via python')
origin.push()