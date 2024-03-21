/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"
#include "lpc1114etf.h"
#define WAIT_TIME_MS 500 

DigitalOut ACT(LED_ACT);
BusOut ledovi(LED0, LED1, LED2, LED3, LED4, LED5, LED6, LED7);

int main()
{
    ACT = 0;
    short val = 1;
    double c = 2.;
    while(true) {
        ledovi.write(val > 0xFF ? 0xFF : val);
        val *= c;
        if (val == 1)
            c = 2;
        if (val == 0x100)
            c = 0.5;
        wait_us(1e5);
    }
}
