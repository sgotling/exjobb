# -*- coding: utf-8 -*-
# Spionprogram som försöker lista ut vad meddelandet som skickats betyder.
import os
import collections
from socket import *

def hackSubstitution(data):
    """
    Knäcker ett substitutionsshiffer genom att byta ut ett tecken i taget.
    """
    oldPrintString = data
    print(collections.Counter(data).most_common(10))
    while True:
        substitutionKeys = {}
        charInput = input("Sign to replace: ")
        replacer = input("Replace with: ")
        substitutionKeys[charInput] = replacer
        substitutionKeys[replacer] = charInput
        newPrintString = ""
        for char in oldPrintString:
            if char in substitutionKeys:
                newPrintString += substitutionKeys[char]
            else:
                newPrintString += char
        print(newPrintString)
        if charInput == 999:
            break
        print(collections.Counter(newPrintString).most_common(10))
        oldPrintString = newPrintString

def start():
    host = ""
    port = 13000
    buf = 1024
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    UDPSock.bind(addr)
    print("HACKING TIME!!! ")
    while True:
        (data, addr) = UDPSock.recvfrom(buf)
        data = data.decode()
        print("Received message: " + data)
        hackSubstitution(data)
        if data == "exit":
            break
    UDPSock.close()
    os._exit(0)

start()
