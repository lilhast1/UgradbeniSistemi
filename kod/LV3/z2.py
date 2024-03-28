import time
from machine import Pin
time.sleep(1.5) # Wait for USB to become ready

"""
DIODE SVJETLE NA 7SEG KADA SE DOVEDE 0  
        -A-
    |F       B|
        -G-   
    |E       C|
        -D-       DP. 
         
KONTROLA CIFRE D1-D4 je aktivna u 0


picoETF
Na razvojni sistem picoETF spojiti ˇcetverocifreni 7-segmentni displej kako je prikazano na slici
4.
Napisati program koji implementira brojaˇc na tasterima 1 i 2. Pritiskom na taster 1 se prikaz
na 7-segmentnom displeju treba uve´cavati (npr. 0000, 0001, 0002, itd.), dok se pritiskom na
taster 2 prikaz smanjuje. Pritisak na taster 3 resetuje brojaˇc na 0000, a pritisak na taster 4
pokre´ce/zaustavlja automatsko brojanje (promjena brojaˇca svaku sekundu).

"""


taster1 = Pin(0, Pin.IN)
taster2 = Pin(1, Pin.IN)
taster3 = Pin(2, Pin.IN)
taster4 = Pin(3, Pin.IN)

digits = [Pin(4, Pin.OUT), Pin(5, Pin.OUT), Pin(6, Pin.OUT), Pin(7, Pin.OUT)]

segments = [Pin(8, Pin.OUT), Pin(9, Pin.OUT), Pin(10, Pin.OUT), Pin(11, Pin.OUT),
             Pin(12, Pin.OUT), Pin(13, Pin.OUT), Pin(14, Pin.OUT), Pin(15, Pin.OUT)]

num2seg = {0: [0,1,2,3,4,5], 
            1: [1,2],
            2: [0,1,3,4,6],
            3: [0,1,2,3,6],
            4: [1,2,5,6],
            5: [0,2,3,5,6],
            6: [0,2,3,4,5,6],
            7: [0,1,2],
            8: [0,1,2,3,4,5,6],
            9: [0,1,2,3,5,6]}

def display(d):
    for i in range(0,8): 
        segments[i](i not in num2seg[d])

def reset_digits():
    digits[0](False)
    digits[1](False)
    digits[2](False)
    digits[3](False)

def zero():
    for j in range(0, 8):
            segments[j](True)

def ith_digit(n, i):
    k = 0
    while(k < i):
        n //= 10
        k += 1
    return n % 10
    
brojac = 0
inc = 1
auto = True

tasteri = [0,0,0,0]

print(taster1.value())
zero()

k = 0

while(True):
    if (taster4.value() == 1 and taster4.value() != tasteri[3]):
        auto = not auto
    if (taster1.value() == 1 and taster1.value() != tasteri[0]):
        brojac += 1
    if (taster2.value() == 1 and taster2.value() != tasteri[1]):
        brojac -= 1
    if (taster3.value() == 1 and taster3.value() != tasteri[2]):
        brojac = 0
    for i in [0, 1, 2, 3]:
        reset_digits()             # izbjegavanje konflikata
        digits[3-i](True)   # biraj i-ti slot
        if (brojac > 10**i - 1):
            display(ith_digit(brojac, i))  # prikazi i-tu cifru
        reset_digits()             # izbjegavanje konflikata
        zero()
    time.sleep(0.05)
    k += 1
    if (auto and k % 20 == 0):
        brojac += 1
    tasteri[0] = taster1.value()
    tasteri[1] = taster2.value()
    tasteri[2] = taster3.value()
    tasteri[3] = taster4.value()



print("Hello, Pi Pico!")

