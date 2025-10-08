import machine
import time
from ir_rx import NEC_16
from ssd1306 import SSD1306_I2C
from machine import Pin
import framebuf


# ==== CONFIGURACIÓN DE PINES ====
# Cambia los números según tu conexión
IN1 = Pin(27, Pin.OUT)   # Motor izquierdo
IN2 = Pin(26, Pin.OUT)
IN3 = Pin(33, Pin.OUT)   # Motor derecho
IN4 = Pin(32, Pin.OUT)

# ==== FUNCIONES DE MOVIMIENTO ====

def adelante():
    """Hace avanzar el carrito."""
    IN1.value(1)
    IN2.value(0)
    IN3.value(1)
    IN4.value(0)
    print("🚗 Avanzando")

def atras():
    """Hace retroceder el carrito."""
    IN1.value(0)
    IN2.value(1)
    IN3.value(0)
    IN4.value(1)
    print("🚗 Retrocediendo")

def izquierda():
    """Gira el carrito a la izquierda."""
    IN1.value(0)
    IN2.value(1)
    IN3.value(1)
    IN4.value(0)
    print("↩️ Girando a la izquierda")

def derecha():
    """Gira el carrito a la derecha."""
    IN1.value(1)
    IN2.value(0)
    IN3.value(0)
    IN4.value(1)
    print("↪️ Girando a la derecha")

def detener():
    """Detiene ambos motores."""
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)
    print("🛑 Carrito detenido")



# Diccionario de botones mapeados a códigos IR
# Deberán llenar la tabla
buttons = {
    0x45:"1",
    0x46:"2",
    0x47:"3",
    0x44:"4",
    0x40:"5",
    0x43:"6",
    0x7:"7",
    0x15:"8",
    0x9:"9",
    0x19:"0",
    0x16:"*",
    0x18:"UP",
    0x52:"DOWN",
    0xd:"#",
    0x1c:"OK",
    0x8:"LEFT",
    0x5a:"RGHT"
}
def ir(data, addr, ctrl):
    print("Dato recibido:", data, " Addr:", addr, " Ctrl:", ctrl)


escala = 0
def ejecutarOpcion(data, addr, ctrl):
    print("Dato recibido:", data, " Addr:", addr, " Ctrl:", ctrl)
    if data in buttons:
        boton = buttons[data]
        if boton == "UP":
            adelante()
        elif boton == "DOWN":
            atras()
        elif boton == "LEFT":
            izquierda()
        elif boton == "RGHT":
            derecha()
        elif boton == "OK":
            detener()
        else:
            print("Botón no asignado a movimiento:", boton)
    
    

def ir_callback(data, addr, ctrl):
    if data in buttons:
        mensaje = "Botón: " + buttons[data]
    else:
        mensaje = "Cod: " + hex(data)



#Deberá mostrar qué tecla se presionó
# Configuración del receptor IR en el GPIO 15
ir_sensor = NEC_16(Pin(15, Pin.IN), callback=ejecutarOpcion)
# Loop infinito para mantener la ejecución
while True:
    time.sleep(1)
