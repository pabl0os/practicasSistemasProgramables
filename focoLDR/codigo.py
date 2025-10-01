# Proyecto: Control de foco 110V con LDR y relé
# - Juan Pablo Aranda Sánchez
# - Becerra Delgado Marcos Mauricio
# - Cristopher Rodríguez Martínez
# Descripción:
# Este programa enciende un foco conectado a un relé cuando la luz ambiente
# disminuye por debajo de un umbral, y lo apaga cuando vuelve a subir.
# Hardware: ESP32/ESP8266 + LDR + Módulo Relé + Foco 110V

from machine import Pin, ADC
import time

# Configuración del LDR (entrada analógica)
ldr = ADC(Pin(36))   # Pin analógico 36 en ESP32
ldr.atten(ADC.ATTN_11DB)   # Rango 0-3.3V

# Configuración del relé (salida digital)
rele = Pin(26, Pin.OUT)

# Umbral ajustable (valor de 0 a 4095 en ESP32)
UMBRAL = 2000

while True:
    # Leer nivel de luz (cuanto más luz, mayor valor del ADC)
    valor_ldr = ldr.read()
    print("Valor LDR:", valor_ldr)

    # Comparar con el umbral
    if valor_ldr < UMBRAL:
        rele.value(1)  # Enciende el foco
        print("Foco ENCENDIDO (noche)")
    else:
        rele.value(0)  # Apaga el foco
        print("Foco APAGADO (día)")

    time.sleep(1)