/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"

#define WAIT_TIME_MS 500 


BusOut ledovi(p6, p7, p8, p9, p10, p11, p12, p13);
DigitalIn btn(p5);

int main()
{
    short val = 1;
    double c = 2.;
    while(true) {
        ledovi.write(val > 0xFF ? 0xFF : val);
        val *= c;
        if (val == 1)
            c = 2;
        if (val == 0x100)
            c = 0.5;
        wait(0.100);
    }
}
