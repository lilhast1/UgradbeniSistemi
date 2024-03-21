/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"
#include "lpc1114etf.h"
#define WAIT_TIME_MS 500 

DigitalOut ACT(LED_ACT);
BusOut ledovi(LED0, LED1, LED2, LED3, LED4, LED5, LED6, LED7);
DigitalIn btn1(Taster_1);
DigitalIn btn2(Taster_2);


void trci(double wait_s)
{
    short val = 1;
    double c = 2.;
    
    while(1) {
        ledovi.write(val > 0xFF ? 0xFF : val);
        val *= c;
        if (val == 1)
            break;
        if (val == 0x100)
            c = 0.5;
        wait_us(wait_s);
    }
}

int main()
{
    int c = 0;
    while(true) {
        ledovi.write(c = !c);
        if (btn1.read())
            trci(1e5);
        if (btn2.read())
            trci(5e5);
        wait_us(5e5);
    }
}
