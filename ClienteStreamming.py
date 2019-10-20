import pickle
import socket
import struct

import cv2

MCAST_GRP = "224.0.0.1"
MCAST_PORT = 10000
IS_ALL_GROUPS = True

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

s=""

while True:
    print("I'm in while loop")
    data, addr = sock.recvfrom(46080)
    s+= data
    if len(s) == (46080*20):
        frame = numpy.fromstring (s, dtype=numpy.uint8)
        frame = frame.reshape(480,640,3)
        cv2.imshow("frame",frame)

        s=""
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
