/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"

#define WAIT_TIME_MS 500 


//DigitalOut led1(LED1);
BusOut ledovi(p6, p7, p8, p9, p10, p11, p12, p13);
DigitalIn btn(p5);

int main()
{
    char brojac = 0;
    while(true) {
        ledovi.write(brojac);
        brojac += btn.read() ? -1 : 1;
        wait_us(1e6);
    }
}
