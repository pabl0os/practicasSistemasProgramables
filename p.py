import machine
import ssd1306
from time import sleep
import utime
from machine import Pin, time_pulse_us
from hcsr04 import HCSR04



# ESP32
# ECHO — 5.6 kΩ —●— 10 kΩ — GND
sensor = HCSR04(trigger_pin=12, echo_pin=13, echo_timeout_us=10000)

# ESP8266
# sensor = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=10000)

def mi_interrupcion(pin):
    print('Movimiento Detectado')
    sleep(5)
    
#pir 
pir_pin = machine.Pin(33, machine.Pin.IN)
pir_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=mi_interrupcion)



while True:
    try:
        #leemos distancia
        distance = sensor.distance_cm()
        if distance < 2:
            print('Distance:', distance, 'cm')
            sleep(.5)
            
        else:
            print('-1')
    except OSError as ex:
        print('-1', ex)
