#!/usr/bin/env python3
# -*- coding: utf-8 -*-
      
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
        f.write(x+"-Cliente conectado puerto: "+str(port)+' Con ip: '+ip+' Con ID: '+str(cliente))

    def run(self):    
        print ("Connection from : "+ip+":"+str(port)+' '+str(cliente))
        sizefile = os.stat(nom).st_size
        num = sizefile/1024
        num = round(num)
        data = "dummydata"
        while len(data):
            data = self.socket.recv(1024)
            print (data)
            break
        
        print ('Enviando ID+Nombre del Archivo')
        self.socket.sendall((str(cliente)+'-'+nom).encode())
        
        print ('Enviando INICIO ENVIO')
        self.socket.sendall(("INICIOENVIO-"+str(sizefile)).encode())
        
        
        i=1;
        with open(nom, 'rb') as file:
            data = file.read(1024)
            self.socket.send(data)
            #while data != bytes(''.encode()):
            for i in range(num):
                print('Enviando archivo'+str(i)+' de '+str(num))
                i+=1
                f.write(x+"-Sending data-Paquete "+str(i)+" de "+str(num))
                f.write('')
                data = file.read(1024)
                self.socket.send(data)
        
        print ('Enviando palabra HASH')
        self.socket.sendall(('HASH').encode())
        
        print('Enviando HASH')
        self.socket.sendall((hashen).encode())
        print(hasher)
        
        while len(data):
            data = self.socket.recv(1024)
            print (data)

        print ("Client disconnected...")

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
    
    """
Created on Sun Sep 29 15:46:01 2019

@author: Juan


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

repoLocal = git.Repo( './' )
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
    
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 15010)
print (sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

#Logs
import logging



# create logger
module_logger = logging.getLogger('server_logger')

class Auxiliary:
    def __init__(self):
        self.logger = logging.getLogger('server_logger.auxiliary.Auxiliary')
        self.logger.info('creating an instance of Auxiliary')

    def do_something(self):
        self.logger.info('doing something')
        a = 1 + 1
        self.logger.info('done doing something')

def some_function():
    module_logger.info('received a call to "some_function"')

# create logger with 'server-log'
logger = logging.getLogger('server_logger')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('server.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('creating an instance of auxiliary_module.Auxiliary')
a = Auxiliary()
logger.info('created an instance of auxiliary_module.Auxiliary')
logger.info('calling auxiliary_module.Auxiliary.do_something')
a.do_something()
logger.info('finished auxiliary_module.Auxiliary.do_something')
logger.info('calling auxiliary_module.some_function()')
some_function()
logger.info('done with auxiliary_module.some_function()')
#FINLOG

while True:
    # Wait for a connection
    print (sys.stderr, 'waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print (sys.stderr, 'connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print (sys.stderr, 'received "%s"' % data)
            if data:
                print (sys.stderr, 'sending data back to the client')
                connection.sendall(data)
            else:
                print (sys.stderr, 'no more data from', client_address)
                break
            
    finally:
        # Clean up the connection
        connection.close()"""