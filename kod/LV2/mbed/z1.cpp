#include "mbed.h"

BusOut ledovi(LED1, LED2, LED3, LED4);

int main() {
    int val = 1;
    const int zero = 0;
    while(1) {
        ledovi.write(val);
        val = val < 8 ? val * 2 : 1;
        wait(1);
        ledovi.write(zero);
        wait(1);
    }
    return 0;
}