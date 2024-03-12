import time
import machine
from machine import Pin
time.sleep(1) # Wait for USB to become ready

led0 = Pin(4, Pin.OUT)

led0.value(1)

t1 = Pin(1, Pin.IN)

led0.value(t1.value())

# pitanje sta se desi ako iznad linije 12 stavim while(1)