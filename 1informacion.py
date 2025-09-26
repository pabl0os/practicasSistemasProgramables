# Rodríguez Martínez Cristopher Giovanni
# Juan Pablo Aranda Sánchez
# Marcos Mauricio Becerra Delgado
# objetivo: Mostrar texto en un display OLED 128x64 usando I2C con MicroPython
import machine
import ssd1306
from time import sleep

# Inicialización del bus I2C que es el protocolo de comunicación que vimos en clase
i2c = machine.SoftI2C(scl=machine.Pin(15), sda=machine.Pin(4))

# basicamente utilizamos esto para prender o apagar el oled si lo apagamos hacemos un reseteo
pin = machine.Pin(16, machine.Pin.OUT)
pin.value(0)  # Colocar en bajo para reset
pin.value(1)  # Mantener en alto mientras el OLED esté en uso

# Dimensiones del display OLED
oled_ancho = 128
oled_alto = 64

# Inicialización del OLED y le mandamos las dimensiones y el bus I2C
oled = ssd1306.SSD1306_I2C(oled_ancho, oled_alto, i2c)

# Limpiar pantalla
oled.fill(0)

# Mostrar texto
oled.text('Hola Mundo', 0, 0)
oled.text('Sistemas Programables', 0, 10)
oled.text('Septiembre 2022', 0, 20)

# Actualizar display
oled.show()