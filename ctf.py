#!/bin/python3

import socket
import os
from enum import Enum
import subprocess
import pexpect
import requests

class Section(Enum):
    WELCOME = 0
    INTRO = 1
    MISC = 2
    WEB = 3
    PWN = 4
    CRYPTO = 5
    SIDE_CHANNEL_AND_FAULT_ATTACKS = 6
    REVERSE = 7
    HARDWARE = 8
    FORENSICS = 9

#def depassementDeTampon():
    ##os.system("./pwn")
    #p = subprocess.Popen("./pwn", stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    #stdout = p.communicate()
    #print(stdout)
    #stdout = p.communicate(input=b'5')[0]
    ##print(stdout.decode())

def depassementDeTampon():
    f = open("depassementDeTampon.log", "a")
    for i in range(500):
        analyzer = pexpect.spawn('./pwn', encoding='utf-8')
        analyzer.expect('=')
        #print(analyzer.before)
        #print(analyzer.after)
        a = int(analyzer.before.split(' ')[1])
        b = int(analyzer.before.split(' ')[3])
        analyzer.sendline(str(a+b))
        out = analyzer.read()
        f.write(out)
        #if out.find('Yes') != -1 :
            ##print(1, end='')
            ##None
            #f.write(out)
        #elif out.find('No') != -1 :
            ##print(0, end='')
            #f.write(out)
        #else:
            ##print(out)
            #f.write(out)
    f.close()

def aLEnvers():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("challenges.france-cybersecurity-challenge.fr", 2000))
    while True :
        data = s.recv(1024)
        if len(data) == 0:
            break
        print("Received : |"+str(data)+"|")
        if data.decode("utf-8").find('>>>') != -1 :
            dataOut = str(data.decode("utf-8")).strip().split(' ')[-1][::-1] + '\n'
            print("Submitted : |"+dataOut+"|")
            s.send(dataOut.encode())
    print("Connection closed.")
    s.shutdown(socket.SHUT_WR)
    s.close()
    
def header():
    headers = {'X-FCSC-2022','Can I get a flag, please?'}
    getdata = requests.get('https://header.france-cybersecurity-challenge.fr/', headers=headers)
    print(getdata)
    
if __name__ == "__main__":
    choice = Section.INTRO
    
    if Section.INTRO :
        #aLEnvers()
        #depassementDeTampon()
        header()
    elif Section.MISC :
        None
        
    exit(0)
