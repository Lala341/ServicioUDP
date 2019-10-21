import cv2
import numpy as np
import socket, threading
import sys
import pickle
import struct
import time


class ClientThread(threading.Thread):

    def __init__(self,MCAST_GRP,MCAST_PORT, MCAST_V):
        threading.Thread.__init__(self)
        self.MCAST_GRP = MCAST_GRP
        self.MCAST_PORT = MCAST_PORT
        self.MCAST_V = MCAST_V
        print ("[+] New thread started for canal "+MCAST_V+"")
        
    def run(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

        cap=cv2.VideoCapture(self.MCAST_V)
        
        while(True):
            ret, frame = cap.read()
            #cv2.imshow('frame',frame)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            d = frame.flatten ()
            s = d.tostring ()
            for i in range(20):
                    try:
                        sock.sendto(s[i*46080:(i+1)*46080],(self.MCAST_GRP, self.MCAST_PORT))
                        time.sleep(0.009)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    except OSError:
                        print("espera1")
                        time.sleep(0.1)
                        

        cap.release()
        cv2.destroyAllWindows()



MCAST_GRP = "224.0.0.1"
MCAST_PORTS=[]
MCAST_VIDEOS=[]
print ('A continuacion definira que videos se añaden a la lista de emision')
print (' Desea agregar el Canal Rita Ora Music- puerto 10000')
print (' 1. Si')
print (' 2. No')
archivo = int(input())
if archivo == 1:
    MCAST_PORT = 10000
    MCAST_PORTS.append([MCAST_PORT,"./test01.mp4"])
    MCAST_VIDEOS.append("./test01.mp4")

print ('2. Desea agregar el Canal CharliePuth Music- puerto 12000')
print (' 1. Si')
print (' 2. No')
archivo = int(input())

if archivo == 1:
    MCAST_PORT = 12000
    MCAST_PORTS.append([MCAST_PORT,"./test02.mp4"])
    MCAST_VIDEOS.append("./test02.mp4")




threads = []
for t in MCAST_PORTS:
    print ("\nListening for incoming connections...")
    newthread = ClientThread("224.0.0.1", t[0], t[1])
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()

if(len(MCAST_PORTS)==0):
    print ("\nNo se eligio ningun canal, conexion cerrada...")




