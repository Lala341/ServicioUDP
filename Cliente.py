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
import math

#Local repo on your computer
#repo = git.Repo( './' )
x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
nameFile="./Cliente/Logs/"+"C-"+x+".txt"
f= open(nameFile,"w+")


hasher = hashlib.md5()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
# Conecta el socket en el puerto cuando el servidor esté escuchando
server_address = ('localhost', 1420)
print (sys.stderr, 'conectando a %s puerto %s' % server_address)
sock.connect(server_address)
x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
f.write(x+"-Cliente conectado puerto"+'\n')
men1="INICIOENVIO"
num=0
hashfileserver=""
datacontent=""
try:
     
    # Enviando datos

    message = 'LISTO'
    print (sys.stderr, 'enviando "%s"' % message)
    message = message.encode()
    sock.send(message)
    
    x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
    f.write(x+"-Enviado LISTO")
    longitud = sock.recv(2)
    #53
    
    impro = 25 + int(longitud)
    
    temp= sock.recv(impro)
    print (temp)
    no = str(temp).split('-')
    cli = no[0]
    nomarchivo = no[1]
    tamano = no[2]
    hasr = no[3]
    print (no[0])
    print (no[1])
    print (no[2])
    print (no[3])
    #datadec=temp.decode()
    nameFilear="./Cliente/Archivos/Cliente-"+cli+"--"+nomarchivo
    sock.send('ARCHIVO-PREPARADO')
    far = open(nameFilear,'wb')
    while True:
        #with open(nameFilear, "wb") as far:
        #data = sock.recv(1024)
        
        cont = 1
        num = math.ceil(int(tamano)/1024.0)
        num = int(num)
        instanteInicial = datetime.datetime.now()
        f.write(x+"-Inicio Envio"+str(num))
        for i in range(num):
            print('Recibiendo archivo numero '+str(cont)+' de '+str(num))
            x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
            f.write(x+"-Receiving data-Paquete "+str(cont)+" de "+str(num)+'\n')
            cont += 1
            data = sock.recv(1024)
            far.write(data)
            
           
        far.close()
        instanteFinal = datetime.datetime.now()     
        tiempo = instanteFinal - instanteInicial
        f.write(x+"-Tiempo total de transferencia "+str(tiempo)+'\n')
        
    
     # Devuelve un objeto timedelta
    
        with open(nameFilear, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
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
        print ('MENSAJE RECIBIDO')
        sock.send(message)
        afile.close()
        sock.close()
        break
        
finally:
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