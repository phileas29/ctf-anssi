#!/bin/python3

import socket
import os
import enum
import subprocess
import pexpect
import requests
import time
import random

class Section(enum.Enum):
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

def guessMe():
    mini = -1
    maxi = 2e20
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("challenges.france-cybersecurity-challenge.fr", 2001))
    res = 2
    count = 0
    while count < 16 :
        test = int( ( mini + maxi ) // 2 )
        #print("r="+str(res)+",a="+str(mini)+",b="+str(maxi)+",d="+str(maxi-mini)+",t="+str(test))
        #print("r="+str(res)+",d="+str(maxi-mini)+",t="+str(test)+",c="+str(count))
        s.send( ( str( test ) + '\n' ).encode("utf-8") )
        time.sleep(0.15)
        #deadline = time.time() + 20.0
        #while True :
            #data = s.recv(2048)
            #if len(data) != 0 :
                #break
            #elif time.time() >= deadline:
                #break
        #while 1:
            #data = s.recv(1024)
            #if len(data) == 0:
                #break
            #print("Received:", repr(data))
        #data = data.decode("utf-8")
        
        try:
            data = s.recv(4096)
        except socket.error as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                sleep(1)
                print('No data available')
                continue
            else:
                print(e)
                sys.exit(1)
        else:
            #print("Received:", repr(data))
            data = data.decode("utf-8")
            
        #if maxi-mini < 10 :
            #print("Received : |"+str(data)+"|")

        if data.find('found') != -1 or maxi-mini <= 0 :
            res = 0
            count += 1
            print("############# success !!! #############")
            if data.find('found') != -1 :
                print("Received : |"+str(data)+"|")
            print("c="+str(count))
            print("maxi-mini="+str(maxi-mini))
            print("test="+str(test))
            mini = -1
            maxi = 2e20
        elif data.find('+1') != -1 :
            mini = test + 1
            res = 1
        elif data.find('-1') != -1 :
            maxi = test - 1
            res = -1
        else:
            print("???????????????????????????????????????")
            print("Received : |"+str(data)+"|")
            res = 2
        if count == 15 :
            print("Received : |"+str(data)+"|")
            print("r="+str(res)+",a="+str(mini)+",b="+str(maxi)+",d="+str(maxi-mini)+",t="+str(test))
    if count == 16 :
        deadline = time.time() + 20.0
        while True :
            data = s.recv(2048)
            if len(data) != 0 :
                break
            elif time.time() >= deadline:
                break
        data = data.decode("utf-8")
        print("last attempt")
        print(data)
    print("Connection closed.")
    s.shutdown(socket.SHUT_WR)
    s.close()
    
class Shuffle(object):
    @classmethod
    def __randbelow(cls,n):
        k = n.bit_length()  # don't use (n-1) here because n can be 1
        r = random.getrandbits(k)          # 0 <= r < 2**k
        while r >= n:
            r = random.getrandbits(k)
        return r

    @classmethod
    def __shuffle(cls,x):
        for i in reversed(range(1, len(x))):
            j = cls.__randbelow(i+1)
            x[i], x[j] = x[j], x[i]
      
    @classmethod      
    def __reverseShuffle(cls,x,seed):
        random.seed(seed)
        l = []
        for i in reversed(range(1, len(x))):
            l.append(cls.__randbelow(i+1))
        for i in range(1, len(x)):
            x[i], x[l[-i]] = x[l[-i]], x[i]
         
    @classmethod 
    def shuffle(cls):
        CHOICE = 1

        if CHOICE == 0 :
            o = "____________________________________________________________F_________"

            flag = list(open("res/crypto/flag.txt", "rb").read().strip())
            #print(repr(flag))
            #print(bytes(flag).decode())
            print(o)
            for i in range(256):
                random.seed(i)
                #cls.__shuffle(flag)
                cls.__shuffle(flag)
                #print(bytes(flag).decode())
                flagDecode = bytes(flag).decode()
                if flagDecode == o :
                    print(i)
                    print(bytes(flag).decode())
        elif CHOICE == 1 :
            output = list(open("res/crypto/output.txt", "rb").read().strip())
            for i in range(256):
                cls.__reverseShuffle(output,i)
                print(bytes(output).decode())

    #flag = list(open("flag.txt", "rb").read().strip())
    #random.seed(random.randint(0, 256))
    #random.shuffle(flag)
    #print(bytes(flag).decode())

    #f668cf029d2dc4234394e3f7a8S9f15f626Cc257Ce64}2dcd93323933d2{F1a1cd29db
    #____________________________________________}______________{__________
    #__________________________S________C____C___________________F_________
    #____________________________________________________________F_________

class QuiEstCe(object):
    N = 63
        
    @classmethod
    def __getBinFromDec(cls,x):
        tmp = bin(int(x))[2:][::-1]
        xBit = [0] * cls.N
        i = 0
        while i < len(tmp) :
            xBit[i] = int(tmp[i])
            i += 1
        return xBit
        
    @classmethod
    def __getBinFromBin(cls,x):
        return "".join(str(e) for e in x[::-1])
        
    @classmethod
    def __getDecFromBin(cls,x):
        return sum([ x[i] * 2 ** i for i in range(cls.N) ])
        
    @classmethod
    def __uFF(cls,x,y,z):
        return ( x & ( not y ) ) ^ z
        
    @classmethod
    def __uF(cls,x):
        y = [0] * cls.N
        for i in range(cls.N):
            y[i] = cls.__uFF(x[(i-2)%cls.N],x[(i-1)%cls.N],x[i])
        return y
        
    @classmethod
    def quiEstCeSimu(cls):
        ##s="11110110101001"
        ##s="1010010101010010101011101"
        #s="101010001001010001"
        #for i in range(2**len(s)):
            #xBit = cls.__getBinFromDec(i)
            #yBit = cls.__uF(xBit)
            #if cls.__getBinFromBin(yBit).find(s) != -1 :
                #print("found!")
                #print(cls.__getBinFromBin(xBit))
        ##r1="1|1100110001101"
        ##r2="10000100010000100011001"
        ##r3="1000101101000101"
                
        
        
        #for i in range(64):
            #xBit = cls.__getBinFromDec(i)
            #yBit = cls.__uF(xBit)
            #print(cls.__getBinFromBin(yBit)+" "+str(i))
        #print()
        #x ="000000000000000000000000000000000000000000000000000000000000000"#0
        x = "110011000110100000100001000100001000110010000001000101101000101"#8549048879922979409
        xBit = [ int(i) for i in x[::-1] ]
        #print(cls.__getBinFromBin(xBit))
        yBit = cls.__uF(xBit)
        print("x_e="+cls.__getBinFromBin(xBit))
        print("x_e="+str(cls.__getDecFromBin(xBit)))
        print("y_e="+cls.__getBinFromBin(yBit))
        #print(cls.__getDecFromBin(yBit))
        print("y_e="+str(cls.__getDecFromBin(yBit)))
        y = 8549048879922979409#=> 111011010100100010100101010100101010111010000101010001001010001
        yBit = cls.__getBinFromDec(y)
        print("y_r="+cls.__getBinFromBin(yBit))
        print("y_r="+str(cls.__getDecFromBin(yBit)))
        
        #for j in range(cls.N):
            #for i in range(cls.N):
                #if i == j :
                    #xBit[i] = 1
                #else:
                    #xBit[i] = 0
            #yBit = cls.__uF(xBit)
            #print(cls.__getBinFromBin(yBit))
            
        #print()
        #for i in range(cls.N):
            #if i % 2 == 0 :
                #xBit[i] = 1
            #else:
                #xBit[i] = 0
        #yBit = cls.__uF(xBit)
        #print(cls.__getBinFromBin(xBit))
        #print(cls.__getBinFromBin(yBit))

    @classmethod
    def quiEstCe(cls):
        x = input("entrer un nbre : ")
        xBit = cls.__getBinFromDec(x)
            
        yBit = cls.__uF(xBit)
            
        print(cls.__getBinFromBin(xBit))
        print(cls.__getBinFromBin(yBit))
        print(cls.__getDecFromBin(xBit))
        print(cls.__getDecFromBin(yBit))
    
if __name__ == "__main__":
    choice = Section.CRYPTO
    
    if choice == Section.INTRO :
        #aLEnvers()
        #depassementDeTampon()
        header()
    elif choice == Section.MISC :
        guessMe()
    elif choice == Section.HARDWARE :
        QuiEstCe.quiEstCeSimu()
    elif choice == Section.CRYPTO :
        Shuffle.shuffle()
        
    exit(0)
