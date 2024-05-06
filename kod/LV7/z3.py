import time, network
from machine import ADC, Pin, PWM, Timer
import dht
from umqtt.robust import MQTTClient
import ujson
from dht import DHT11
# teme:
# hasta/led1
# hasta/led2 
# hasta/led3 
# hasta/potenciometar 
# hasta/taster
# hasta/rgb

station = network.WLAN(network.STA_IF)
accpoint = network.WLAN(network.AP_IF)

led1 = Pin(4, Pin.OUT)
led2 = Pin(5, Pin.OUT)
led3 = PWM(Pin(6))
led3.freq(20)

R = Pin(14, Pin.OUT)
G = Pin(12, Pin.OUT)
B = Pin(13, Pin.OUT)

potenctiometar = ADC(Pin(26))
dht11 = DHT11(Pin(28))

btn = Pin(0, Pin.IN)

nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect('Lab220', 'lab220lozinka')

while not nic.isconnected():
	print('cekam...')
	time.sleep(0.5)

ip = nic.ifconfig()[0]

mqtt_conn = MQTTClient(client_id='picoETF', server='broker.hivemq.com',user='',password='',port=1883)

def duty(m):
	return int(float(m) * 65535)

def rgb(m):
	v = int(m)
	return v // 100, (v // 10) % 10, v % 10

def subskripcija(tema, msg):
	p = ujson.loads(msg)
	if tema == b'hasta/led1':
		m = p[""]
		led1.value(m % 2)
	elif tema == b'hasta/led2':
		led2.value(m % 2)
	elif tema == b'hasta/led3':
		c = duty(m)
		led3.duty_u16(c)
	elif tema == b'hasta/rgb':
		r, g, b = rgb(m)
		R.value(r)
		G.value(g)
		B.value(b)

P = potenctiometar.read_u16()

def publish_poten(p):
	global P
	if (P != potenctiometar.read_u16()):
		P = potenctiometar.read_u16()
		f = float(P / 65535)
		s = '{"Potenciometar": ' + str(f) + '}'
		b = s.encode('utf-8')
		mqtt_conn.publish(b'hasta/potenciometar', b)

def publish_button_on(p):
	mqtt_conn.publish(b'hasta/taster', b'{"Taster": 1}')

def publish_dht(p):
	d = {"Temperatura": dht11.temperature, "Vlaga": dht11.humidity}
	s = ujson.dumps(d)
	b = s.encode('utf-8')
	mqtt_conn.publish(b'hasta/DHTmjerenja', b)

mqtt_conn.set_callback(subskripcija)
mqtt_conn.connect()
mqtt_conn.subscribe([b"hasta/led1", b"hasta/led2"])

btn.irq(trigger=Pin.IRQ_RISING, handler=publish_button_on)
t = Timer(period=20, mode=Timer.PERIODIC, callback=publish_poten)
t2 = Timer(period=2000, mode=Timer.PERIODIC, callback=publish_dht)

while(True):
	mqtt_conn.wait_msg()