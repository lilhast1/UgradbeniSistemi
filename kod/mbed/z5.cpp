/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"

#define WAIT_TIME_MS 500 



DigitalIn btn1(BUTTON1);
DigitalOut led(LED1);


int main()
{
    int c = 10, dir = 1;
    const double T = 1;
    while(true) {
        led.write(1);
        wait(c * T / 10.);
        led.write(0);
        wait((20 - c) * T / 10.);
        if (c == 19)
            dir = -1;
        if (c == 1)
            dir = 1;
        c += dir;
    }
}
