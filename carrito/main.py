"""
Carrito controlado por control remoto IR (protocolo NEC) usando L298N
Motores al 100% (ENA/ENB fijos a 5 V). 

Hardware esperado:
- ESP32 con MicroPython.
- Módulo L298N (ENA/ENB siempre activos) y dos motores DC.
- Receptor IR en GPIO 15 (ajustable).
"""

import time
from machine import Pin
from ir_rx import NEC_16

# ==============================
#  CONFIGURACIÓN DE PINES MOTOR
# ==============================
# Ajusta los números de pin según tu cableado.
IN1 = Pin(27, Pin.OUT)   # Motor izquierdo - Dirección
IN2 = Pin(26, Pin.OUT)   # Motor izquierdo - Dirección
IN3 = Pin(33, Pin.OUT)   # Motor derecho  - Dirección
IN4 = Pin(32, Pin.OUT)   # Motor derecho  - Dirección

# ==============================
#  FUNCIONES DE MOVIMIENTO
# ==============================
def adelante():
    """Hace avanzar el carrito (ambos motores hacia adelante)."""
    IN1.value(1); IN2.value(0)
    IN3.value(1); IN4.value(0)

def atras():
    """Hace retroceder el carrito (ambos motores hacia atrás)."""
    IN1.value(0); IN2.value(1)
    IN3.value(0); IN4.value(1)

def izquierda():
    """Gira en el lugar a la izquierda (izq atrás, der adelante)."""
    IN1.value(0); IN2.value(1)
    IN3.value(1); IN4.value(0)

def derecha():
    """Gira en el lugar a la derecha (izq adelante, der atrás)."""
    IN1.value(1); IN2.value(0)
    IN3.value(0); IN4.value(1)

def detener():
    """Detiene ambos motores (rueda libre)."""
    IN1.value(0); IN2.value(0)
    IN3.value(0); IN4.value(0)

# ======================================
#  TABLA DE CÓDIGOS IR -> NOMBRE BOTÓN
# ======================================
# Mapa entre el código recibido (entero) y una etiqueta legible.
# Nota: La etiqueta "RGHT" es intencional (coincide con tu tabla).
buttons = {
    0x45: "1",
    0x46: "2",
    0x47: "3",
    0x44: "4",
    0x40: "5",
    0x43: "6",
    0x07: "7",
    0x15: "8",
    0x09: "9",
    0x19: "0",
    0x16: "*",
    0x18: "UP",
    0x52: "DOWN",
    0x0D: "#",
    0x1C: "OK",
    0x08: "LEFT",
    0x5A: "RGHT"
}

def ejecutarOpcion(data, addr, ctrl):
    """
    Callback principal del receptor IR.
    Traduce el 'data' recibido a un botón usando 'buttons'
    y ejecuta la acción correspondiente.
    """

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
            # Aquí caen dígitos y símbolos "*", "#", etc.
            # Puedes asignarles acciones si lo deseas.
            print("Botón no asignado a movimiento:", boton)
    else:
        # Código no reconocido en la tabla
        print("Código IR desconocido:", hex(data))


# ==========================
#  INICIALIZACIÓN DEL IR
# ==========================
# Receptor IR protocolo NEC (16 bits) en GPIO 15.
# Si tu receptor está en otro pin, cámbialo aquí.
ir_sensor = NEC_16(Pin(15, Pin.IN), callback=ejecutarOpcion)

# ==========================
#  LOOP PRINCIPAL
# ==========================
# No es necesario hacer nada dentro del bucle: el control es por interrupciones
# (el callback 'ejecutarOpcion' se ejecuta cada vez que llega un código IR).
while True:
    time.sleep(1)  # Pequeño delay para mantener vivo el script
