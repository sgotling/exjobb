# -*- coding: utf-8 -*-

import random

# import unicodedata
from socket import *
from fractions import gcd

def caesarCoder(data):
    """
    Tar en textrad och krypterar den med caesarshiffer så att den blir svårare att läsa
    """
    shift = 1;
    utf8TableSetLength = 256
    ceasarCipher = ""
    for char in data:
        ceasarCipher += chr((ord(char) + shift) % utf8TableSetLength)
    return ceasarCipher


def makeKey(alphabet):
    """
    Genererar en substitut-nyckel genom att slumpa alfabetet
    """
    alphabet = list(alphabet)
    random.shuffle(alphabet)
    return ''.join(alphabet)

def substituteEncoder(data):
    """
    Använder en substitut-nyckel för att kryptera en textrad
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyzåäö.,! '
    #key = makeKey(alphabet)
    #print key
    key = "tcasznjxurpvqfmwåäöikdlo,b yh.e!g"
    keyMap = dict(zip(alphabet, key))
    return ''.join(keyMap.get(c.lower(), c) for c in data)



def rsaEncoder(data):
    """
    Översätter och krypterar en textrad till numerärt värde med hjälp av RSA-metod
    """
    #Generera publik-, privat nyckel samt (publik) talbas
    e, d, n = rsaKeyGen()
    #Översätt in-sträng till sträng av motsvarande ascii-tecken
    asciiStr = strToAscii(data)

    chunkLen = len(str(n))-1    #Tillåten längd på data att kryptera
    #Dela upp strängen i krypterbara bitar
    #asciiList = reverseRead(
    asciiList = cunningPlan(asciiStr, chunkLen)

    rsaEncrypted = ""
    for chunk in asciiList:
        rsaChunk = str(pow(int(chunk), e)%n)      #Kryptera med nyckel e och bas n..
        while len(rsaChunk)<chunkLen+1:
            rsaChunk="0"+rsaChunk                 #..fyll på med nollor för att försäkra avkrypterbara bitar..
        rsaEncrypted+=rsaChunk       #..och spara till färdigkrypterad sträng
    return rsaEncrypted

def cunningPlan(strIn, chunkLen):
    """
    Lägger till "0" först i strIn tills dess att det är jämt delbart med chunkLen. Delar sedan upp strIn till array med element av längd chunkLen.
    """
    while len(strIn)%chunkLen!=0:
        strIn=0+strIn

    element = ""
    returnList = []
    for i in range(0, len(strIn), chunkLen):
        for j in range(i, i+chunkLen):
            element += strIn[j]
        returnList.append(element)
        element = ""

    return returnList


def strToAscii(strIn):
    """
    Omvandlar en strängs tecken till dess motsvarande (tresiffriga) asciivärden
    """
    strOut=""
    for i in strIn:
        j = str(ord(i))
        if len(j)<3:
            j="0"+j #Fyll på med nollor till vänster s.a. alla tecken har 3-siffrigt block
        strOut+=j
    return strOut

def reverseRead(strIn, chunkLen):
    """
    Läser av en sträng av siffror bakifrån och fyller på med nollor för att skapa lika långa 'chunks' i en lista.
    Listan vänds för att ge rätt ordning och returneras.
    """
    chunk = ""               #Tillfällig sträng att konstruera bitar i
    i=len(strIn)-chunkLen      #Startposition för att läsa av strängen bakifrån
    returnList=[]              #Lista för alla bitar krypterbar längd
    goOn = True
    while goOn:
        for j in range(i, i+chunkLen):      #Läs av hela strängen...
            if j<0:
                goOn=False
            else:
                chunk+=strIn[j]
        i-=chunkLen                         #...clip för clip
        if len(chunk)>0:
            returnList.append(chunk)
        chunk=""

    returnList.reverse()
    return returnList      #Vänd rätt listan


def rsaKeyGen():
    """
    Tar in två primtal från användaren och generar talbas, publik och privat nyckel
    """

    #p,q = input("Enter first and second prime (p!=q) divided by one space (' '): ").split(' ')
    #p,q = int(p),int(q)
    p,q=43, 53 #19, 53

    #OBS n måste vara större än 1000
    n = p*q #=1007
    m = (p-1)*(q-1)


    #Välj publik nyckel e
    while True:
        e = int(input("Choose an e s.t. gcd(e, {m})=1 and 3<e<{m}. e=".format(m=m)))

        if gcd(e, m)==1 and e>3 and e<m:
            break
        print("e does not satisfy: ", end="")
        if e<=3 or e>=m:
            print("3<e<{} ".format(m), end="")
        if gcd(e, m)!=1:
            print("gcd(e, {})=1".format(m), end="")
        print()

    #Finn d=inversen till e
    d = multInverse(e, m)

    print("!!OBS!! e: {}, d: {}, n: {} !!OBS!!".format(e, d, n))
    return e, d, n


def multInverse(e, m):
    """
    Använder Euklides algoritm för att finna talet e's invers i bas m
    """
    g, d, _ = egcd(e, m)
    if g == 1:
        return d%m

def egcd(e, m):
    """
    'Extended Euklidian algorithm'
    """
    if e == 0:
        return(m, 0, 1)
    else:
        g, x, y = egcd(m%e, e)
        return (g, y - (m // e) * x, x)



host = "127.0.0.1" # set to IP address of target computer
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
while True:
    data = input("Enter message to send or type 'exit': ")

    #data = caesarCoder(data)
    # data = data.lower()
    # data = substituteEncoder(data)
    # UDPSock.sendto(data.encode(), addr)

    data = rsaEncoder(data)
    data = data.encode()
    UDPSock.sendto(data, addr)
    if data == "exit":
        break
UDPSock.close()
os._exit(0)
