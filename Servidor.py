#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 07:16:39 2019

@author: Juan Daniel
"""

import socket, threading
import os
import hashlib
import math
import git
import datetime

#Local repo on your computer
#repo = git.Repo( './' )
x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
nameFile="./Servidor/Logs/"+"C-"+x+".txt"
f= open(nameFile,"w+")

print ('que archivo quiere transferir?')
print ('1. Texto 100MB')
print ('2. Imagen 250MB')
archivo = int(input())
cliente = 0;

if archivo == 1:
    nom = 'test01.rtf'
else:
    nom = 'test05.mov'
    
f.write(x+" El servidor va a enviar archivos con el nombre: "+nom+'\n')
    
hasher = hashlib.md5()

with open(nom, 'rb') as afile:
    buf = afile.read()
    hasher.update(buf)
    hashen = hasher.hexdigest()
    
afile.close()

class ClientThread(threading.Thread):

    def __init__(self,ip,port, socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        print ("[+] New thread started for "+ip+":"+str(port))
        f.write(x+"-Cliente conectado puerto: "+str(port)+' Con ip: '+ip+' Con ID: '+str(cliente)+'\n')

    def run(self):    
        print ("Connection from : "+ip+":"+str(port)+' '+str(cliente))
        sizefile = (os.stat(nom).st_size)
        print (str(sizefile))
        num = math.ceil(sizefile/1024.0)
        num = int(num)
        print(str(num))
        data = self.socket.recv(5)
        data = data.decode()
        if data == 'LISTO':
            print('ENVIANDO INICIO ENVIO')
            cl = str(cliente)
            
            #Improvisción
            self.socket.send(str(len(str(hashen))))
            
            if cliente == 1 or cliente==2 or cliente==3 or cliente==4 or cliente==5 or cliente==6 or cliente==7 or cliente==8 or cliente==9:
                cl = '0'+str(cliente)
            f.write(x+"-Enviando ID de cliente "+cl+'\n'+'Nombre del archivo: '+nom+'\n'+'Archivo de tamano: '+str(sizefile)+'\n'+'Con hash igual a: '+str(hashen)+'\n')
            self.socket.send((cl+'-'+nom+'-'+str(sizefile)+'-'+str(hashen)))
            print ('Enviando '+cl+' '+nom)
        
        data = self.socket.recv(1024)
        
        if data == 'ARCHIVO-PREPARADO':
            with open(nom, "rb") as ff:        
                arch = ff.read(1024)
                contador=1
                while arch:
                    print('Enviando archivo '+str(contador)+' de '+str(num))
                    contador += 1
                    self.socket.send(arch)
                    arch = ff.read(1024)
            ff.close()
                    
                    
        data = self.socket.recv(8)
        if data=='ERRORES!':
            print('CLIENTE PRESENTA ERRORES')
            f.write(x+"-!!!!!!EL ARCHIVO PRESENTA ERRORES"+'\n')
            f.write(x+"EL CLIENTE "+cl+' INFORMA QUE EL ARCHIVO PRESENTA ERRORES'+'\n')
        else:
            print('CLIENTE CONFIRMA')
            f.write(x+" EL CLIENTE "+cl+' CONFIRMA QUE EL ARCHIVO FUE TRASNFERIDO EN PERFECTO ESTADO'+'\n')
        #f.write(x+"-Enviando HASH: "+hola+'\n') 

        print ("Client disconnected...")
        f.write(x+" Finaliza conexion con el cliente "+str(cliente)+'\n')
        self.socket.close()

host = "0.0.0.0"
port = 1420

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcpsock.bind((host,port))
threads = []


while True:
    tcpsock.listen(25)
    print ("\nListening for incoming connections...")
    (clientsock, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsock)
    newthread.start()
    cliente += 1;
    threads.append(newthread)

for t in threads:
    t.join()
    

#Si esto no funciona acá, ponerlo dentro del run()
origin = repo.remote('origin')
origin.pull()
repo.git.add(u=True)
repo.git.commit(m='Adding logs via python')
origin.push()
    