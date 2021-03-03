#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Spionprogram som försöker lista ut vad meddelandet som skickats betyder.
import os
from socket import *

def hackCaesar(data):
    """
    Knäcker ett caesarshiffer genom att testa att förskjuta med olika steg som matas in av användaren.
    Mata in 999 för att avsluta.
    """
    while True:
        shift = int(raw_input("Enter caesar shift: "))
        utf8TableSetLength = 256
        text = ""
        for char in data:
            text += chr((ord(char) + shift) % utf8TableSetLength)
        print text
        if shift == 999:
            break

def hackCaesarAll(data):
    """
    Knäcker ett caesarshiffer genom att testa alla möjliga kombinationer.
    """
    for shift in range(257):
        utf8TableSetLength = 256
        text = ""
        for char in data:
            text += chr((ord(char) + shift) % utf8TableSetLength)
        print text

host = ""
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)
print "HACKING TIME!!! "
while True:
    (data, addr) = UDPSock.recvfrom(buf)
    print "Received message: " + data
    hackCaesar(data)
    if data == "exit":
        break
UDPSock.close()
os._exit(0)
