import time
import machine
from machine import Pin

time.sleep(0.2)

t1 = Pin(0, Pin.IN)
t2 = Pin(1, Pin.IN)
t3 = Pin(2, Pin.IN)
t4 = Pin(3, Pin.IN)

print("CHECKPOINT")

led = [Pin(4, Pin.OUT), Pin(5, Pin.OUT), Pin(6, Pin.OUT), Pin(7, Pin.OUT), Pin(8, Pin.OUT), Pin(9, Pin.OUT), Pin(10, Pin.OUT), Pin(11, Pin.OUT)]

print("CHECKPOINT")

brojac = 0

while (True):
  if (t3.value()):
    brojac = 0
  elif (t4.value()):
    brojac = 0xFF
  elif (t1.value()):
    brojac += 1
  elif (t2.value()):
    brojac -= 1
  brojac %= 0xFF + 1 # prekoracenje da izbjegnem
  s = bin(brojac)[2:] # bin(x)->'0b' + binarna reprezentacija x
  s = "0" * (8-len(s)) + s # padding na 8 bita
  for i in range(0, 8):
    led[i].value(int(s[i])) 
  time.sleep(0.1) # da bi mogao stici inc/dec