import time
import machine
from machine import Pin

time.sleep(0.2)

R = Pin(14, Pin.OUT)
G = Pin(12, Pin.OUT)
B = Pin(13, Pin.OUT)

for i in (0, 1):
  for j in (0, 1):
    for k in (0, 1):
      R.value(i)
      G.value(j)
      B.value(k)
      print(f'{i},{j},{k}')
      time.sleep(2.)

#boje vidjene:
# crna
# plava
# zelena
# cyan
# crvena
# ljubicasta
# zuta
# bijela
