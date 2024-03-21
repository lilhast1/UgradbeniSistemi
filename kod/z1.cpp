#include "mbed.h"
#include "lpc1114etf.h"

BusOut ledovi(LED0, LED1, LED2, LED3);

DigitalOut ACT(LED_ACT);

int main() {
    ACT = 0;
    int val = 1;
    const int zero = 0;
    while(1) {
        ledovi.write(val);
        val = val < 8 ? val * 2 : 1;
        wait_us(1e6);
        ledovi.write(zero);
        wait_us(1e6);
    }
    return 0;
}