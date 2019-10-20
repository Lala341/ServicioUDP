import pickle
import socket
import struct
import numpy
import cv2
from datetime import date
from datetime import datetime
import time

MCAST_GRP = "224.0.0.1"
MCAST_PORT = 10000
IS_ALL_GROUPS = True

print ('A que puerto se quiere conectar (Canal)?')
print ('1. Canal Rita Ora Music-10000')
print ('2. Canal CharliePuth Music-12000')
archivo = int(input())

if archivo == 1:
    MCAST_PORT = 10000
else:
    MCAST_PORT = 12000
    
print ('Ingrese su usuario para autenticarse')
user = int(input())
print ('Ingrese su contraseña para autenticarse')
contra = int(input())

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if IS_ALL_GROUPS:
    # on this port, receives ALL multicast groups
    sock.bind(('', MCAST_PORT))
else:
    # on this port, listen ONLY to MCAST_GRP
    sock.bind((MCAST_GRP, MCAST_PORT))

mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((MCAST_GRP, MCAST_PORT))
run=False

#Día actual
now = datetime.now()
now=str(now).replace("/","-")
frame_width = 480
frame_height = 640

def nothing(x):
    pass

s= b''
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

out = cv2.VideoWriter('./Cliente/Streamming/test'+now+'.mp4', fourcc , 15.0, (640,480))
run = True
while True:
    if(run==True):
        data, addr = sock.recvfrom(46080)
        s+= data
        if len(s) == (46080*20):
            print("Recibiendo datos.")
            frame = numpy.fromstring (s, dtype=numpy.uint8)
            frame = frame.reshape(480,640,3)
            out.write(frame)
            cv2.imshow("frame",frame)

            s= b''
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Cerrando streamming-STOP")
    
            break
        if cv2.waitKey(1) & 0xFF == ord('v'):
            print("Pausar streamming-PAUSE")
            run= not run
    if cv2.waitKey(1) & 0xFF == ord('v'):
        print("Pausar streamming-PAUSE")
        run= not run
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Cerrando streamming-STOP")
        break

    
out.release()