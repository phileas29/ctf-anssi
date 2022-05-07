#!/bin/python3

import socket
import os
import enum
import subprocess
import pexpect
import requests
import time
import random
import pwn
import numpy as np
import base64
import math as m
import pyModbusTCP.client


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
    mini = 0
    maxi = 1e20
    analyzer = pexpect.spawn('python3 res/misc/guessme.py', encoding='utf-8')
    #print(analyzer.before)
    #print(analyzer.after)
    #a = int(analyzer.before.split(' ')[1])
    #b = int(analyzer.before.split(' ')[3])
    #analyzer.sendline(str(a+b))
    count = 0
    data = ""
    x = ''
    while count < 16 :
        test = int( ( mini + maxi ) // 2 )
        #analyzer.expect('>>> ')
        analyzer.sendline(str(test))
        while True:
            x = str(analyzer.read(2))
            if x != '\r' or x != '\n' :
                data += x
                print(x,end='')
            if data[-4:] == '>>> ' :
                break
        #print(data)
        exit(0)
        #print(str(maxi-mini)+",", end='')

        if data.find('+1') != -1 :
            mini = test
        elif data.find('-1') != -1 :
            maxi = test
        elif data.find('0') != -1 :
            count += 1
            print("success")
            print(test)
            mini = -1
            maxi = 2e20
    
    exit(0)
    
    
    HOST = "challenges.france-cybersecurity-challenge.fr"
    PORT = 2001
    
    mini = 0
    maxi = 1e20
    c = pwn.remote(HOST, PORT)
    count = 0
    while count < 16 :
        test = int( ( mini + maxi ) // 2 )
        c.recvuntil(b">>> ")
        c.sendline( str(test).encode("utf-8") )
        time.sleep(0.15)
        data = c.recvline().decode("utf-8")
        #data = data
        #print(data[:2], end='')
        print(str(maxi-mini)+",", end='')

        if data.find('+1') != -1 :
            mini = test
            
            if maxi-mini <= 0 :
                mini = -1
                maxi = 2e20
        elif data.find('-1') != -1 :
            maxi = test
            
            if maxi-mini <= 0 :
                mini = -1
                maxi = 2e20
        elif data.find('0') != -1 :
            count += 1
            print("############# success !!! #############")
            print(data)
            print("c="+str(count))
            print("maxi-mini="+str(maxi-mini))
            print("test="+str(test))
            mini = -1
            maxi = 2e20
        elif maxi-mini <= 0 :
            count += 1
            print("############# success ??? #############")
            print(data)
            print("c="+str(count))
            print("maxi-mini="+str(maxi-mini))
            print("test="+str(test))
            mini = -1
            maxi = 2e20
        else:
            print("???????????????????????????????????????")
            print("Received : |"+str(data)+"|")
    if count == 16 :
        data = c.recvline()
        data = data.decode("utf-8")
        print("last attempt")
        print(data)
    print("Connection closed.")
    c.close()
    
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

class DaddyMorse(object):
    HOST = "challenges.france-cybersecurity-challenge.fr"
    PORT_AM = 2251
    PORT_FM = 2252
    
    SAMP_RATE = 24e3
    MAX_LEN = 256000

    FREQ = { 'l' : 1e3 , 'h' : 5e3 }

    TIMING_DOT = 1/1000
    TIMING_DASH = 5/1000
    TIMING_SEP_LETTER = 5/1000
    TIMING_SPACE = 20/1000

    alphabet = { 'A':'.-', 'B':'-...',
                'C':'-.-.', 'D':'-..', 'E':'.',
                'F':'..-.', 'G':'--.', 'H':'....',
                'I':'..', 'J':'.---', 'K':'-.-',
                'L':'.-..', 'M':'--', 'N':'-.',
                'O':'---', 'P':'.--.', 'Q':'--.-',
                'R':'.-.', 'S':'...', 'T':'-',
                'U':'..-', 'V':'...-', 'W':'.--',
                'X':'-..-', 'Y':'-.--', 'Z':'--..',
                '1':'.----', '2':'..---', '3':'...--',
                '4':'....-', '5':'.....', '6':'-....',
                '7':'--...', '8':'---..', '9':'----.',
                '0':'-----', ', ':'--..--', '.':'.-.-.-',
                '?':'..--..', '/':'-..-.', '-':'-....-',
                '(':'-.--.', ')':'-.--.-'}

    rev_alphabet = {k:v for k,v in alphabet.items()}
    
    @classmethod
    def __morseEncode(cls,msg):
        data = ""
        for word in msg.split(" "):
            for i,letter in enumerate(word):
                if letter in cls.rev_alphabet:
                    data += cls.rev_alphabet[letter]
                elif letter == "":
                    continue
                else:
                    return "error"
                if i != len(word) - 1:
                    data += "_"
            data += " "
        return data

    @classmethod
    def __getLastPadding(cls,s):
        i = 0
        while i < len(s) and s[-1-i] < 0.1 :
            i += 1
        return i
        
    @classmethod
    def __getComplex(cls,fType,tn):
        return np.complex64( \
            m.cos(2*m.pi*cls.FREQ[fType]*tn) + \
            m.sin(2*m.pi*cls.FREQ[fType]*tn)*1j )
        
    @classmethod
    def __encodeSampleFM(cls,data,s):
        signal = []
        
        if data == ".":
            for _ in range(int(cls.TIMING_DOT*cls.SAMP_RATE)):
                signal.append(cls.__getComplex('h',(len(s)+len(signal))/cls.SAMP_RATE))
            for _ in range(int(cls.TIMING_DOT*cls.SAMP_RATE)):
                signal.append(cls.__getComplex('l',(len(s)+len(signal))/cls.SAMP_RATE))
        elif data == "-":
            for _ in range(int(cls.TIMING_DASH*cls.SAMP_RATE)):
                signal.append(cls.__getComplex('h',(len(s)+len(signal))/cls.SAMP_RATE))
            for _ in range(int(cls.TIMING_DOT*cls.SAMP_RATE)):
                signal.append(cls.__getComplex('l',(len(s)+len(signal))/cls.SAMP_RATE))
        elif data == '_' :
            for _ in range(int((cls.TIMING_SEP_LETTER-cls.TIMING_DOT)*cls.SAMP_RATE)):
                signal.append(cls.__getComplex('l',(len(s)+len(signal))/cls.SAMP_RATE))
        elif data == " ":
            for _ in range(int((cls.TIMING_SPACE-cls.TIMING_DOT)*cls.SAMP_RATE)):
                signal.append(cls.__getComplex('l',(len(s)+len(signal))/cls.SAMP_RATE))
            
        s += signal
        
    @classmethod
    def __encodeSampleAM(cls,data,s):
        signal = []
        
        if data == ".":
            for _ in range(int(cls.TIMING_DOT*cls.SAMP_RATE)):
                signal.append(np.complex64(1+1j))
            for _ in range(int(cls.TIMING_DOT*cls.SAMP_RATE)):
                signal.append(np.complex64(0+0j))
        elif data == "-":
            for _ in range(int(cls.TIMING_DASH*cls.SAMP_RATE)):
                signal.append(np.complex64(1+1j))
            for _ in range(int(cls.TIMING_DOT*cls.SAMP_RATE)):
                signal.append(np.complex64(0+0j))
        elif data == '_' :
            for _ in range(int((cls.TIMING_SEP_LETTER-cls.TIMING_DOT)*cls.SAMP_RATE)):
                signal.append(np.complex64(0+0j))
        elif data == " ":
            for _ in range(int((cls.TIMING_SPACE-cls.TIMING_DOT)*cls.SAMP_RATE)):
                signal.append(np.complex64(0+0j))
            
        s += signal

    @classmethod
    def __fmEncode(cls,data):
        signal = []
        
        for d in data:
            cls.__encodeSampleFM(d,signal)
        
        return signal

    @classmethod
    def __amEncode(cls,data):
        signal = []
        
        for d in data:
            cls.__encodeSampleAM(d,signal)
        
        return signal
    
    @classmethod
    def __stringToComplex(cls,x):
        
        return y
    
    @classmethod
    def daddyMorse(cls,mode='am'):
        if mode == 'am' :
            c = pwn.remote(cls.HOST, cls.PORT_AM)
        elif mode == 'fm' :
            c = pwn.remote(cls.HOST, cls.PORT_FM)
        np.set_printoptions(threshold=np.inf)
        message = "CAN I GET THE FLAG"
        #message = "HELLO"
        data = cls.__morseEncode(message)
        #print(data)
        if mode == 'am' :
            signal = np.asarray(cls.__amEncode(data))
        elif mode == 'fm' :
            signal = np.asarray(cls.__fmEncode(data))
        np.save('signal_fm_001.iq', signal)
        #print(len(signal))
        #print(signal)
        encodedSignal = base64.b64encode(signal.tobytes())
        #print(encodedSignal[:50])
        
        c.recvuntil(b"> ")
        c.sendline(encodedSignal)
        print(c.recvline())
        
        c.close()
        
class ColorPlant(object):
    HOST = "challenges.france-cybersecurity-challenge.fr"
    PORT = 502
    
    @classmethod
    def colorPlant(cls):
        c = pyModbusTCP.client.ModbusClient()
        c.host(cls.HOST)
        c.port(cls.PORT)
        c.open()
        regs = c.read_holding_registers(0, 32)
        print(regs)
        for e in regs:
            print(chr(e),end='')
        print()
        time.sleep(8)
        
        print("debit max")
        for i in range(4):
            c.write_single_register(32+i, 5)
        #rouge + 1/2 vert
        print("transfert R + % V")
        if c.read_coils(0, 1)[0] == False :
            c.write_single_coil(0, True)
        if c.read_coils(1, 1)[0] == False :
            c.write_single_coil(1, True)
        while True :
            if 25 <= c.read_input_registers(3, 1)[0] and c.read_holding_registers(32, 1)[0] == 5 :
                c.write_single_register(32,1)
            if 60 <= c.read_input_registers(4, 1)[0] and c.read_holding_registers(33, 1)[0] == 5 :
                c.write_single_register(33,1)
            if 32 <= c.read_input_registers(3, 1)[0] :
                if c.read_coils(0, 1)[0] == True :
                    c.write_single_coil(0, False)
            if 68 <= c.read_input_registers(4, 1)[0] :
                if c.read_coils(1, 1)[0] == True :
                    c.write_single_coil(1, False)
            if c.read_coils(0, 1)[0] == False and c.read_coils(1, 1)[0] == False :
                break
            time.sleep(0.1)
        if c.read_coils(3, 1)[0] == False :
            c.write_single_coil(3, True)
        while c.read_input_registers(3, 1)[0] != 0 or c.read_input_registers(4, 1)[0] != 0 :
            time.sleep(0.1)
        if c.read_coils(3, 1)[0] == True :
            c.write_single_coil(3, False)
            
        print("debit max")
        for i in range(4):
            c.write_single_register(32+i, 5)
        #bleu + 1/2 vert
        print("transfert B + % V")
        if c.read_coils(1, 1)[0] == False :
            c.write_single_coil(1, True)
        if c.read_coils(2, 1)[0] == False :
            c.write_single_coil(2, True)
        while True :
            if 50 <= c.read_input_registers(4, 1)[0] and c.read_holding_registers(33, 1)[0] == 5 :
                c.write_single_register(33,1)
            if 35 <= c.read_input_registers(5, 1)[0] and c.read_holding_registers(34, 1)[0] == 5 :
                c.write_single_register(34,1)
            if 58 <= c.read_input_registers(4, 1)[0] :
                if c.read_coils(1, 1)[0] == True :
                    c.write_single_coil(1, False)
            if 42 <= c.read_input_registers(5, 1)[0] :
                if c.read_coils(2, 1)[0] == True :
                    c.write_single_coil(2, False)
            if c.read_coils(1, 1)[0] == False and c.read_coils(2, 1)[0] == False :
                break
            time.sleep(0.1)
        if c.read_coils(3, 1)[0] == False :
            c.write_single_coil(3, True)
        while c.read_input_registers(4, 1)[0] != 0 or c.read_input_registers(5, 1)[0] != 0 :
            time.sleep(0.1)
        if c.read_coils(3, 1)[0] == True :
            c.write_single_coil(3, False)

        c.close()

    
if __name__ == "__main__":
    choice = Section.MISC
    
    if choice == Section.INTRO :
        #aLEnvers()
        #depassementDeTampon()
        header()
    elif choice == Section.MISC :
        #guessMe()
        ColorPlant.colorPlant()
    elif choice == Section.HARDWARE :
        #QuiEstCe.quiEstCeSimu()
        DaddyMorse.daddyMorse('fm')
    elif choice == Section.CRYPTO :
        Shuffle.shuffle()
        
    exit(0)
