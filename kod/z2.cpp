/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"
#include "lpc1114etf.h"




#define WAIT_TIME_MS 500 

DigitalOut ACT(LED_ACT); 


//DigitalOut led1(LED1);
BusOut ledovi(LED0, LED1, LED2, LED3, LED4, LED5, LED6, LED7);
DigitalIn btn(Taster_1);

int main()
{
    ACT = 0;                        // ACT mora biti lo
    char brojac = 0;
    while(true) {
        ledovi.write(brojac);
        brojac += btn.read() ? -1 : 1;
        wait_us(1e6);
    }
}
