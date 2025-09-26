import machine
import ssd1306
from utime import sleep_ms
from time import sleep
import dht
import time
import utime
 
sensordht = dht.DHT11(machine.Pin(18))

  
def mostrarTemperatura():
    sensordht.measure()
    temp = sensordht.temperature()
    print("Temp:", temp)
    sleep_ms(500)

def mostrarHumedad():
    sensordht.measure()
    hum = sensordht.humidity()
    print("Humedad:", hum)
    sleep_ms(500)

def mostrar_menu():
    print("Menú de opciones:")
    print("1. Luminosidad")
    print("2. Temperatura")
    print("3. Humedad")
    print("4. Integrantes")

# Configurar pin 4 como entrada analógica (ADC)
ldr = machine.ADC(machine.Pin(4))
ldr.atten(machine.ADC.ATTN_11DB)   # Permite leer hasta 3.3V aprox.
ldr.width(machine.ADC.WIDTH_10BIT) # Resolución de 10 bits (0–1023)
def mostrarLuminosidad():
    valor = ldr.read()   # Lee el valor ADC (0–1023)
    print("Luz:", valor)
    sleep_ms(500)
    
def mostrarLOGONombres():
    print("Integrantes del grupo:")
    print(" - Juan David Castro")
    
    


while True:
    mostrar_menu()
    opcion = input("Selecciona una opción (1-4): ")
    inicio = utime.ticks_ms()
    while utime.ticks_diff(utime.ticks_ms(), inicio) < 5000:  # 5000 ms = 5 segundos
        if opcion == "1":
            print("1  Has seleccionado: Luminosidad")
            mostrarLuminosidad()
        elif opcion == "2":
            print("2  Has seleccionado: Temperatura")
            mostrarTemperatura()
        elif opcion == "3":
            print("3  Has seleccionado: Humedad")
            mostrarHumedad()
        elif opcion == "4":
            print("4  Has seleccionado: Integrantes")
            mostrarLOGONombres()
        else:
            print("Opción no válida. Intenta de nuevo.")
    print()  # Línea en blanco para separar