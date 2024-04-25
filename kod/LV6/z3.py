import time
from machine import Pin

time.sleep(0.1)

brojac = 0

ledice = [Pin(4, Pin.OUT), Pin(5, Pin.OUT), Pin(6, Pin.OUT), Pin(7, Pin.OUT),
		Pin(8, Pin.OUT), Pin(9, Pin.OUT), Pin(10, Pin.OUT), Pin(11, Pin.OUT)]

clock_wise = Pin(0, Pin.IN)
counter_clock = Pin(1, Pin.IN)
press = Pin(2, Pin.IN)

def write(arr, val):
	for pin in arr:
		pin.value(val % 2)
		val //= 2

def handle1(pin):
	global brojac
	if (counter_clock.value() == 1):
		brojac += 1

def handle2(pin):
	global brojac
	if (clock_wise.value() == 1):
		brojac -= 1

def reset(pin):
	global brojac
	brojac = 0

clock_wise.irq(handle1, Pin.IRQ_FALLING)
counter_clock.irq(handle2, Pin.IRQ_FALLING)
press.irq(reset, Pin.IRQ_FALLING)

def main():
	while (True):
		write(ledice, brojac)
		time.sleep(0.05)

if __name__=='__main__':
	main()