import time
import machine
from machine import Pin
time.sleep(0.1) # Wait for USB to become ready wokwi stvar komotno ignorisati


#ovo se treba u REPLU izvrsiti dakle linebyline

t1 = Pin(0, Pin.IN)
t1.value()
stanje = t1.value()
print(stanje)

time.sleep(4)

stanje = t1.value()
print(stanje)