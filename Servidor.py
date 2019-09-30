#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 07:16:39 2019

@author: Juan Daniel
"""

import socket, threading
import os
import hashlib
import git
import datetime

#Local repo on your computer
repo = git.Repo( './' )
x = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
nameFile="./Servidor/Logs/"+"C-"+x+".txt"
f= open(nameFile,"w+")

print ('¿Qué archivo quiere transferir?')
print ('1. Foto 100MB')
print ('2. Video 250MB')
archivo = int(input())
cliente = 1;
nom = 'test01.txt';

if archivo == 1:
    nom = 'test01.txt'
else:
    nom = 'test02.jpg'
    


hasher = hashlib.md5()

with open(nom, 'rb') as afile:
    buf = afile.read()
    hasher.update(buf)
    hashen = hasher.hexdigest()

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
        sizefile = (os.stat(nom).st_size)/1000000
        print (str(sizefile))
        num = sizefile/1024
        num = round(num)
        data = "hola"
        while len(data):
            data = self.socket.recv(1024)
            print (data)
            break
        
        print ('Enviando ID+Nombre del Archivo')
        self.socket.sendall((str(cliente)+'-'+nom).encode())
        
        print ('Enviando INICIO ENVIO')
        self.socket.sendall(("INICIOENVIO-"+str(sizefile)).encode())
        
        
        contador=1;
        with open(nom, 'rb') as file:
            data = file.read(1024)
            self.socket.send(data)
            #while data != bytes(''.encode()):
            for i in range(num):
                print('Enviando archivo '+str(contador)+' de '+str(num))
                contador+=1
                f.write(x+"-Sending data-Paquete "+str(contador)+" de "+str(num)+'\n') 
                f.write('')
                data = file.read(1024)
                self.socket.send(data)
        
        print ('Enviando palabra HASH')
        f.write(x+"-Enviando palabra HASH "+'\n') 
        self.socket.sendall(('HASH').encode())
        
        print('Enviando HASH')
        hola = str(hasher)
        f.write(x+"-Enviando HASH: "+hola+'\n') 
        self.socket.sendall((hashen).encode())
        print(hasher)
        
        while len(data):
            data = self.socket.recv(1024)
            print (data)

        print ("Client disconnected...")
        f.write(x+" Finaliza conexión con el cliente "+str(cliente)+'\n') 

host = "0.0.0.0"
port = 1420

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcpsock.bind((host,port))
threads = []


while True:
    tcpsock.listen(20)
    print ("\nListening for incoming connections...")
    (clientsock, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsock)
    newthread.start()
    cliente += 1;
    threads.append(newthread)

for t in threads:
    t.join()
    