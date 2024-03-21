/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"

#define WAIT_TIME_MS 500 


DigitalOut red(LED_RED), blue(LED_BLUE), green(LED_GREEN);


int main()
{
    int c = 10, dir = 1;
    const double Tr = 1, Tb = 0.5, Tg = 0.3;
    while(true) {
        red.write(1);
        wait_us(c * Tr * 1e5);
        red.write(0);
        wait_us((20 - c) * Tr * 1e5);
        
        green.write(1);
        wait_us(c * Tg * 1e5);
        green.write(0);
        wait_us((20 - c) * Tg * 1e5);

        blue.write(1);
        wait_us(c * Tb * 1e5);
        blue.write(0);
        wait_us((20 - c) * Tb * 1e5);

        if (c == 19)
            dir = -1;
        if (c == 1)
            dir = 1;
        c += dir;
    }
}
