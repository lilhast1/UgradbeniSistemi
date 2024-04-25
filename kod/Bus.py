from machine import Pin

'Kopija ponasanja BusOut i BusIn iz mbed.os-a'

class BusOut():
	def __init__(self, *args):
		self.arr = []
		for num in args:
			self.arr.append(Pin(num, Pin.OUT))

	def write(self, n):
		for pin in self.arr:
			pin.value(n % 2)
			n //= 2

	def read(self):
		n = 0
		k = 1
		for pin in arr:
			n += k * pin.value()
			k *= 2
		return n 

class BusIn():
	def __init__(self, *args):
		self.arr = []
		for num in args:
			self.arr.append(Pin(num, Pin.IN))
	
	def read(self):
		n = 0
		k = 1
		for pin in self.arr:
			n += k * pin.value()
			k *= 2
		return n 

