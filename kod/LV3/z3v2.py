import time
from machine import Pin
time.sleep(1.5) # Wait for USB to become ready

"""
Matriˇcnu tastaturu povezati na sistem picoETF, kako je prikazano na slici 5, a 7-segmentni
displej prema slici iz zadatka 2 (slika 4).
Napisati program koji omogu´cuje korisniku provjeru ispravnosti unesenog PIN-a od ˇcetiri
cifre. PIN se prilikom unosa prikazuje na 7-segmentnom displeju. Kada se PIN unese, nakon
pritiska na taster ”#”, se provjeri ispravnost unosa i ukoliko je PIN ispravan, na sve ˇcetiri
cifre 7-segmentnog displeja se pale i gase decimalne taˇcke u trajanju od 5s. Ukoliko je unos
neispravan, na sve ˇcetiri cifre 7-segmentnog displeja se pale i gase znakovi ”-”. Nakon toga se
omogu´cava ponovni unos PIN-a.
Ukoliko je unos PIN-a neispravan tri puta za redom, ponovni unos se blokira u trajanju od
10 sekundi, ˇsto se indicira ispisivanjem cifre od 9 do 0 svake sekunde. Nakon toga se omogu´cava
ponovni unos PIN-a.

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
user_input = 0
FLAG = False

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
    global user_input, gen, row, col, matrix, FLAG
    keyboard_off()
    for i in range(0, 4):
        keyboard_off()
        row[i](True) #citaj i-ti red
        for j in range (0, 4):
            if (col[j].value() == 1 and matrix[i][j] == 0):
                matrix[i][j] = 1
                if (j < 3 and i < 3):
                    user_input *= 10 
                    user_input += 3 * i + 1 + j
                    return
                elif (j == 2 and i == 3):
                    FLAG = True
                    return
            matrix[i][j] = col[j].value()
            #time.sleep(0.001)
        row[i](False)


def seg_disp(T):
    for i in [0, 1, 2, 3]:
        reset_digits()
        digits[3-i](True)
        zero()
        if (T >= 10**i):
            display(ith_digit(T, i))
        zero()
        reset_digits()

def flicker(i, t):
    for i in [0, 1, 2, 3]:
        digits[i](True)
    zero()
    T = 0
    while (T < 5):
        segments[i](False)
        time.sleep(t)
        segments[i](True)
        time.sleep(t)
        T += 2 * t
    zero()
    reset_digits()


def input_timeout():
    for i in range (9, 1, -1):
        seg_disp(i)
        time.sleep(1)

def main():
    global FLAG, user_input
    miss = 0
    PIN = 1234
    while(True):
        seg_disp(PIN) # prikazi PIN na ekran
        read() # ocitaj tastaturu
        for i in [0, 1, 2, 3]:
            reset_digits()
            digits[3-i](True)
            zero()
            if (T >= 10**i):
                display(ith_digit(T, i))
            zero()
            reset_digits()
        if (FLAG):
            miss += 1
            if (miss % 3 != 0):
                if (PIN == user_input):
                    flicker(7, 0.5)
                else:
                    flicker(6, 0.5)
            else:
                input_timeout()
        FLAG = False

if __name__ == '__main__':
    main()

print("Hello, Pi Pico!")

