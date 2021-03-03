#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Save as server.py
# Message Receiver
import os
from socket import *

def caesarDecoder(data):
    """
    Tar en texrad och avkrypterar den med ett caesarshiffer så att texten går att läsa.
    """
    shift = 1;
    utf8TableSetLength = 256
    decodedString = ""
    for char in data:
        decodedString += chr((ord(char) - shift) % utf8TableSetLength)
    return decodedString

def substituteDecoder(data):
    """
    Använder en substitut-nyckel för att avkryptera en textrad
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz.,! '
    #key = input("Enter key: ")
    key = "tcasznjxurpvqfmwåäöikdlo,b yh.e!g"

    keyMap = dict(zip(key, alphabet))
    return ''.join(keyMap.get(c.lower(), c) for c in data)


def rsaDecoder(data):
    """
    Avkodar ett RSA-krypterat meddelande mha en privat nyckel (d) och bas (n)
    """
    while True:
        d, n = input("Ange privat nyckel (d): "), input("Ange bas (n): ")
        if (input("Nyckel={}, bas={} - Stämmer det? [y/n] :".format(d, n))=="y"):
            d, n = int(d), int(n)
            break

    chunkLen = len(str(n))  #Längden på avkrypterbara strängar
    dataList = linearRead(data, chunkLen)

    rsaList = []
    for bite in dataList:
        rsaBite = str(pow(int(bite), d)%n)  #Avkryptera med nyckel d och bas n..
        rsaList.append(chr(int(rsaBite)))   #..och översätt till motsvarande tecken
    stringOut = ''.join(rsaList)            #Slå samman listan till en sträng

    return stringOut

def linearRead(strIn, chunkLen):
    """
    Läser av och delar upp en sträng i bitar av bestämd maxlängd
    """
    strList = []       #Lista för alla bitar i avkrypterbar längd
    for i in range(0, len(strIn), chunkLen):
        chunk = ""           #Tillfällig sträng att konstruera bitar i
        for j in range(i, i+chunkLen):
            chunk+=strIn[j]
        if(len(chunk)>0):
            strList.append(chunk)
    return strList

host = ""
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)

print("Waiting to receive messages...")
while True:
    (data, addr) = UDPSock.recvfrom(buf)
    data=data.decode()
    #data = caesarDecoder(data)
    #data = substituteDecoder(data)

    data = rsaDecoder(data)
    print("Received message: " + data)
    if data == "exit":
        break
UDPSock.close()
os._exit(0)
