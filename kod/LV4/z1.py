import time
from machine import ADC
from machine import Pin
time.sleep(0.1) # Wait for USB to become ready

def write(pins, value):
  for pin in pins:
    pin(value % 2)
    value //= 2
  
def conv_help(x):
  return 1.9 / 65535 * x + 0.1

def main():
  inp = ADC(28)
  ledovi = [Pin(4, Pin.OUT), Pin(5, Pin.OUT), Pin(6, Pin.OUT),
          Pin(7, Pin.OUT), Pin(8, Pin.OUT), Pin(9, Pin.OUT),
          Pin(10, Pin.OUT), Pin(11, Pin.OUT)]
  
  while (True):
    t = conv_help(inp.read_u16())
    value = 0x1
    while (value < 0xFF):
      write(ledovi, value)
      value *= 2 
      t = conv_help(inp.read_u16())
      time.sleep(t)
    value = 0xFF
    t = conv_help(inp.read_u16())
    time.sleep(t)
    write(ledovi, value)
    while (value > 0):
      write(ledovi, value)
      value //= 2
      t = conv_help(inp.read_u16())
      time.sleep(t)
    write(ledovi, 0)
    time.sleep(t)

if __name__=='__main__':
  main()
