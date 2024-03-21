/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"
#include "lpc1114etf.h"

#define WAIT_TIME_MS 500 


DigitalOut ACT(LED_ACT);
DigitalIn btn1(Taster_1);
DigitalOut led(LED1);


int main()
{
    ACT = 0;
    int c = 10, dir = 1;
    const double T = 1;
    while(true) {
        led.write(1);
        wait_us(c * T * 1e5);
        led.write(0);
        wait_us((20 - c) * T * 1e5);
        if (c == 19)
            dir = -1;
        if (c == 1)
            dir = 1;
        c += dir;
    }
}
