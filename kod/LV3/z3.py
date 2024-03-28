import time
from machine import Pin
time.sleep(1.5) # Wait for USB to become ready

"""
Matriˇcnu tastaturu povezati na sistem picoETF, kako je prikazano na slici 5, a 7-segmentni
displej prema slici iz zadatka 2 (slika 4).
Potrebno je realizirati ”generator ˇcetvrtki”2 na pinu GP16. Generiranje signala se pokre´ce i
zaustavlja pritiskom na taster A. Pritiskom na taster 0-9 se postavlja period signala u rasponu
od 1 do 10ms. Pritisak na taster C pove´cava, a pritisak na taster D umanjuje period signala
za 1ms.
Na 7-segmentnom displeju treba biti prikazan trenutno postavljeni period signala

"""

digits = [Pin(4, Pin.OUT), Pin(5, Pin.OUT), Pin(6, Pin.OUT), Pin(7, Pin.OUT)]

segments = [Pin(8, Pin.OUT), Pin(9, Pin.OUT), Pin(10, Pin.OUT), Pin(11, Pin.OUT),
             Pin(12, Pin.OUT), Pin(13, Pin.OUT), Pin(14, Pin.OUT), Pin(15, Pin.OUT)]

row = [Pin(21, Pin.OUT), Pin(22, Pin.OUT), Pin(26, Pin.OUT), Pin(27, Pin.OUT)]

col = [Pin(0, Pin.IN), Pin(1, Pin.IN), Pin(2, Pin.IN), Pin(3, Pin.IN)]



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
T = 4
k = 0
out = Pin(16, Pin.OUT)
gen = True

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
    


def square(t):
    out(True)
    time.sleep(t)
    out(False)
    time.sleep(0.01 - t)



def keyboard_off():
    for i in [0, 1, 2, 3]:
        row[i](False)



matrix = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

def read():
    global T, gen, row, col, matrix
    keyboard_off()
    for i in range(0, 4):
        keyboard_off()
        row[i](True) #citaj i-ti red
        for j in range (0, 4):
            if (col[j].value() == 1 and matrix[i][j] == 0):
                matrix[i][j] = 1
                if (j < 3 and i < 3):
                    T = 3 * i + j + 1
                    print("ovde")
                    
                    return
                elif (j == 3 and i == 0):
                    gen = not gen
                    return

                elif (j == 3 and i == 2):
                    T += 1 
                    print("ovd")
                    return
                elif (j == 3 and i == 3):
                    T -= 1 
                    print("ocd")
                    return
            matrix[i][j] = col[j].value()
            #time.sleep(0.001)
        row[i](False)


def main():
    global T, gen, k
    while(True):
        # ocitaj tastaturu
        read()
        print(T)
        # prikazi T na ekran
        for i in [0, 1, 2, 3]:
            reset_digits()
            digits[3-i](True)
            zero()
            if (T >= 10**i):
                display(ith_digit(T, i))
            zero()
            reset_digits()
        k += 1
        # generiraj kvadrat
        if (gen):
            square(T / 1000)

if __name__ == '__main__':
    main()

print("Hello, Pi Pico!")

