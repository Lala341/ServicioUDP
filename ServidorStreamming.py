import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import time


MCAST_GRP = "224.0.0.1"
MCAST_PORT = 10000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

cap=cv2.VideoCapture("./test02.mp4")


while(True):
   ret, frame = cap.read()
   cv2.imshow('frame',frame)
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   d = frame.flatten ()
   s = d.tostring ()
   for i in range(20):
        try:
            sock.sendto (s[i*46080:(i+1)*46080],(MCAST_GRP, MCAST_PORT))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except OSError:
            print("espera1")
            time.sleep(0.1)
            
        

cap.release()
cv2.destroyAllWindows()
