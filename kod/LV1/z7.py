import time
import machine
from machine import Pin

time.sleep(0.2)

R = Pin(14, Pin.OUT)
G = Pin(12, Pin.OUT)
B = Pin(13, Pin.OUT)

t = 1
step = 1

while (True):
  for i in (0, 1):
    for j in (0, 1):
      for k in (0, 1):
        R.value(i)
        G.value(j)
        B.value(k)
        time.sleep(t / 10.)
        t += step
        if (t == 11):
          step = -1
          t = 10
        if (t == 0):
          step = 1
          t = 1

