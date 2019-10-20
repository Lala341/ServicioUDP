import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import time


MCAST_GRP = "224.0.0.1"
MCAST_PORT = 10000
MCAST_PORTS=[]
MCAST_VIDEOS=[]
print ('A continuacion definira que videos se añaden a la lista de emision')
print (' Desea agregar el Canal Rita Ora Music- puerto 10000')
print (' 1. Si')
print (' 2. No')
archivo = int(input())
if archivo == 1:
    MCAST_PORT = 10000
    MCAST_PORTS.append(MCAST_PORT)
    MCAST_VIDEOS.append("./test01.mp4")

print ('2. Desea agregar el Canal CharliePuth Music- puerto 12000')
print (' 1. Si')
print (' 2. No')
archivo = int(input())

if archivo == 1:
    MCAST_PORT = 12000
    MCAST_PORTS.append(MCAST_PORT)
    MCAST_VIDEOS.append("./test02.mp4")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

cap=cv2.VideoCapture("./test02.mp4")


while(True):
   ret, frame = cap.read()
   #cv2.imshow('frame',frame)
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   d = frame.flatten ()
   s = d.tostring ()
   for i in range(20):
        try:
            sock.sendto(s[i*46080:(i+1)*46080],(MCAST_GRP, MCAST_PORT))
            time.sleep(0.009)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except OSError:
            print("espera1")
            time.sleep(0.1)
            

cap.release()
cv2.destroyAllWindows()
