# Rodríguez Martínez Cristopher Giovanni
# Juan Pablo Aranda Sánchez
# Marcos Mauricio Becerra Delgado
# objetivo: Mostrar un logo escalado en un display OLED 128x64 usando I2C con MicroPython
import machine
import ssd1306
from time import sleep

# Inicializa la interfaz I2C
i2c = machine.SoftI2C(
    scl=machine.Pin(15),
    sda=machine.Pin(4)
)

# basicamente utilizamos esto para prender o apagar el oled si lo apagamos hacemos un reseteo
pin = machine.Pin(16, machine.Pin.OUT)
pin.value(0)  # Pone GPIO16 en bajo para resetear el OLED
pin.value(1)  # Mientras el OLED esté en uso, GPIO16 debe estar en 1

# Dimensiones del OLED
oled_ancho = 128
oled_alto = 64

# Inicializa la pantalla OLED
oled = ssd1306.SSD1306_I2C(oled_ancho, oled_alto, i2c)

# Matriz de puntos para el ícono
ICONO = [
    [0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 0, 0, 1, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1],
    [0, 0, 1, 1, 0, 1, 1, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0],
]

# aquí lo que hacemos es que cuando detecta un 1 dibuja de tal forma que si es 2 por ejemplo se dibuja un cuadrado de 2x2 y si es 3 un cuadrado de 3x3 etc
def dibujar_icono(oled, matriz, x0=0, y0=0, escala=1):
    # Dibuja una matriz de icono en la pantalla OLED con un factor de escala.

    # oled   -> objeto SSD1306
    # matriz -> lista de listas con 0 y 1
    # x0, y0 -> posición inicial en pantalla
    # escala -> tamaño de escalado (1 = normal, 2 = doble, etc.)
    
    for y, fila in enumerate(matriz):
        for x, c in enumerate(fila):
            if c:  # Solo dibuja si es un "1"
                for dy in range(escala):
                    for dx in range(escala):
                        oled.pixel(x0 + x*escala + dx, y0 + y*escala + dy, 1)

    oled.show()
    
    
# llamamos a la función para dibujar el ícono en la pantalla OLED
dibujar_icono(oled, ICONO,  escala=2)
