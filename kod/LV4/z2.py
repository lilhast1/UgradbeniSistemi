import time
from machine import ADC, Pin, SPI, Timer
from ili934xnew import ILI9341, color565
from micropython import const
import os
import glcdfont
import tt14
import tt24
import tt32

time.sleep(0.1) # Wait for USB to become ready

sin45 = 2**-0.5

SCR_WIDTH = const(320)
SCR_HEIGHT = const(240)
SCR_ROT = const(2)
CENTER_Y = int(SCR_WIDTH/2)
CENTER_X = int(SCR_HEIGHT/2)

TFT_CLK_PIN = const(18)
TFT_MOSI_PIN = const(19)
TFT_MISO_PIN = const(16)
TFT_CS_PIN = const(17)
TFT_RST_PIN = const(20)
TFT_DC_PIN = const(15)

fonts = [glcdfont,tt14,tt24,tt32]


spi = SPI(
    0,
    baudrate=62500000,
    miso=Pin(TFT_MISO_PIN),
    mosi=Pin(TFT_MOSI_PIN),
    sck=Pin(TFT_CLK_PIN))

display = ILI9341(
                spi,
                cs=Pin(TFT_CS_PIN),
                dc=Pin(TFT_DC_PIN),
                rst=Pin(TFT_RST_PIN),
                w=SCR_WIDTH,
                h=SCR_HEIGHT,
                r=SCR_ROT)
display.erase()

TIME = 0
TEMP = 20
BLACK = color565(0,0,0)
RED = color565(255,0,0)
WHITE = color565(255,255,255)

def write(pins, value):
  for pin in pins:
    pin(value % 2)
    value //= 2

def plot_low(x0, y0, x1, y1, col):
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if (dy < 0):
        yi = -1
        dy = -dy
    D = (2 * dy) - dx
    y = y0
    for x in range(x0, x1 + 1):
        display.pixel(y, x, col)
        if (D > 0):
            y += yi
            D += 2 * (dy - dx)
        else:
            D += 2* dy

def plot_high(x0, y0, x1, y1, col):
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if (dx < 0):
        xi = -1
        dx = -dx
    D = (2 * dx) - dy
    x = x0
    for y in range(y0, y1 + 1):
        display.pixel(y, x, col)
        if (D > 0):
            x += xi
            D += 2 * (dx - dy)
        else:
            D += 2 * dx

def draw_line(x0, y0, x1, y1, col):
    if (abs(y1 - y0) < abs(x1 - x0)):
        if (x0 > x1):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        plot_low(x0, y0, x1, y1, col)
    else:
        if (y0 > y1):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        plot_high(x0, y0, x1, y1, col)

class Point:
    def __init__(self, _x, _y):
        self.x = round(_x)
        self.y = round(_y)


def draw_circle(xpos0, ypos0, rad, col=color565(255, 255, 255)):
    x = rad - 1
    y = 0
    dx = 1
    dy = 1
    err = dx - (rad << 1)
    while x >= y:
        # Prikaz pojedinačnih piksela
        display.pixel(xpos0 + x, ypos0 + y, col)
        display.pixel(xpos0 + y, ypos0 + x, col)
        display.pixel(xpos0 - y, ypos0 + x, col)
        display.pixel(xpos0 - x, ypos0 + y, col)
        display.pixel(xpos0 - x, ypos0 - y, col)
        display.pixel(xpos0 - y, ypos0 - x, col)
        display.pixel(xpos0 + y, ypos0 - x, col)
        display.pixel(xpos0 + x, ypos0 - y, col)
        if err <= 0:
            y += 1
            err += dy
            dy += 2
        if err > 0:
            x -= 1
            dx += 2
            err += dx - (rad << 1)


# iscrtava ispunjeni krug
def draw_point(x, y, r, col=color565(255, 255, 255)):
    p = round(r * sin45)
    
    display.fill_rectangle(x - p, y - p, 2 * p + 1, 2 * p + 1, col)
    i = x - p 
    j = x + p
    itr = 1
    u = y - p - itr
    r2 = r * r
    while (i < j):
        d2 = (u - y) * (u - y)
        # i++ dok (u,i) nije u krugu
        while(d2 + (i - x) * (i - x) > r2 and i != j):
            i += 1
        # j-- dok (u, j) nije u krugu
        while(d2 + (j - x) * (j - x) > r2 and j >= i):
            j -= 1
        if (j < i):
            break
        # od (u, i) do (u, j) ispuni tu cizu cijelu
        k = i
        while (k <= j):
            display.pixel(u, k, col)
            display.pixel(y + p + itr, k, col)
            k += 1
        # iskoristi simetriju gornji donji polukrug
        itr += 1
        u -= 1
    i = y - p
    j = y + p
    itr = 1
    u = x - p - itr
    while (i < j):
        d2 = (u - x) * (u - x)
        # i++ dok (i,u) nije u krugu
        while(d2 + (i - y) * (i - y) > r2 and i != j):
            i += 1
        # j-- dok (j, u) nije u krugu
        while(d2 + (j - y) * (j - y) > r2 and j >= i):
            j -= 1
        if (j < i):
            break
        # od (i, u) do (j, u) ispuni tu cizu cijelu
        k = i
        while (k <= j):
            display.pixel(k, u, col)
            display.pixel(k, x + p + itr, col)
            k += 1
        # iskoristi simetriju gornji donji polukrug
        itr += 1
        u -= 1


temp = ADC(Pin(28)) # 0-65535 <- 0-3.3 ; 0-1 -> 0-100 ; 1V = 19859 ; 0-19859 -> 0-100

def temp_map(u):
    return 100 / 65535 * u # myb problem


def transform(time, temp):
    return 300 - 10 * time, -10.5 * temp + 430 # dio oko wokwia

def job(t):
    global TIME, TEMP
    oldTEMP = TEMP
    TEMP = temp_map(temp.read_u16())
    TIME += 1
    display.set_pos(30, 0)
    display.print('Napon: ' + str(round(temp.read_u16() / 19859 * 100)) + ' mV\n')
    display.print('Temp: ' + str(round(TEMP, 1)) + ' C\n')
    display.print('Vrijeme: ' + str(TIME) + ' s\n')
    
    print("HALF DONE")

    ot, oT = transform(TIME - 1, oldTEMP)
    nt, nT = transform(TIME, TEMP)
    draw_line(round(ot), round(oT), round(nt), round(nT), RED)

    print("old temp: " + str(round(oldTEMP)))
    display.fill_rectangle(round(oT)-1, round(ot)+1, 3, 3, color565(0, 0, 255))
    display.fill_rectangle(round(nT)-1, round(nt)+1, 3, 3, RED)
    #draw_point(round(ot), round(oT), 4, BLACK)
    #draw_point(round(nt), round(nT), 4, RED)




def main():
    #display.set_font(tt32)
    display.rotation = 3 #TODO fix transformacije
    display.init() # kljucna linija!!!!! takodjer mi je ujebala cijeli koord sistem...
    #display.rotation = 3
   
    display.fill_rectangle(0, 0, SCR_HEIGHT, SCR_WIDTH, color565(255, 255, 255))
    #display.pixel(SCR_WIDTH // 2, SCR_HEIGHT // 2, color565(255, 255, 255))
   #draw_circle(SCR_WIDTH // 2, SCR_HEIGHT // 2, 6)
    print("START")
    draw_point(180, 180, 20, color565(0,0,0))
    print("DONE")
    display.set_color(color565(0, 0, 0), color565(255, 255, 255))
    display.set_pos(0, SCR_WIDTH - 30)
    display.print('Napon: ')

    draw_line(SCR_WIDTH - 10, 0,SCR_WIDTH - 10, SCR_HEIGHT - 10, BLACK)
    draw_line(10, SCR_HEIGHT - 10,SCR_WIDTH - 10, SCR_HEIGHT - 10, BLACK)
    timmy = Timer(period=1000, mode=Timer.PERIODIC, callback=job)
    
    while (True):
        print(temp_map(temp.read_u16()))
        #job(0)
        #time.sleep(0.7)
    return 0

if __name__=='__main__':
    main()
