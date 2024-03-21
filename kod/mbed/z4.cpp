/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"

#define WAIT_TIME_MS 500 


BusOut ledovi(p6, p7, p8, p9, p10, p11, p12, p13);
DigitalIn btn1(BUTTON1);
DigitalIn btn2(p5);


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
        wait(wait_s);
    }
}

int main()
{
    int c = 0;
    while(true) {
        ledovi.write(c = !c);
        if (btn1.read())
            trci(0.1);
        if (btn2.read())
            trci(0.5);
        wait(0.5);
    }
}
