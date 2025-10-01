"""
====================================================
        Ping Pong Tecnm - Juego Interactivo
====================================================

Integrantes:
- Juan Pablo Aranda Sánchez
- Becerra Delgado Marcos Mauricio
- Cristopher Rodríguez Martínez

Objetivo:
El objetivo del juego es simular una versión clásica del Pong
en una pantalla OLED controlada por un ESP32, donde dos jugadores
compiten para anotar puntos golpeando una pelota en movimiento.

Mecánica del juego:
- El Jugador 1 controla su barra con el sensor MPU6050. La barra
  se desplaza según la inclinación del dispositivo.
- El Jugador 2 controla su barra con un joystick analógico.
- Ambos jugadores tienen acceso a un "Power-Up" que expande el
  tamaño de su barra:
    • Jugador 1 lo activa al hacer un movimiento brusco (tilt alto).
    • Jugador 2 lo activa presionando el botón en el pin 18.
- El sistema mantiene la puntuación en pantalla.
- La pelota rebota en los bordes y en las barras, sumando puntos
  cuando un jugador no logra detenerla.

Requisitos cumplidos:
Control en tiempo real con MPU6050 (acelerómetro).
Control alternativo con joystick.
Detección de movimientos bruscos → activa Power-Up.
Botón físico como segundo método de Power-Up.
Rebote en bordes y colisión con paddles.
Sistema de puntos en pantalla.

Extra (Creativo):
Power-Ups dinámicos (barra más grande por tiempo limitado).
Interfaz OLED con indicadores de estado ("P1 POWER!", "P2 POWER!").
"""

from machine import Pin, I2C, ADC
import time
from ssd1306 import SSD1306_I2C

# --- Mini driver MPU6050 ---
class MPU6050Mini:
    """
    Clase simplificada para leer el acelerómetro del MPU6050.
    Se obtiene el ángulo de inclinación (tilt) a partir del eje Y.
    """
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        # Despertar el sensor (quitar modo sleep)
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')

    def read_raw(self):
        """
        Lee los datos crudos (acelerómetro) del MPU6050.
        Devuelve: (ax, ay, az)
        """
        data = self.i2c.readfrom_mem(self.addr, 0x3B, 6)

        def twos(b1, b2):
            v = b1 << 8 | b2
            if v & 0x8000:
                v = -((v ^ 0xFFFF) + 1)
            return v

        ax = twos(data[0], data[1])
        ay = twos(data[2], data[3])
        az = twos(data[4], data[5])
        return ax, ay, az

    def get_tilt(self):
        """
        Calcula la inclinación en el eje Y, normalizado.
        """
        ax, ay, az = self.read_raw()
        return ay / 16384  # Normalización típica


# --- Configuración hardware ---
i2c = I2C(0, scl=Pin(22), sda=Pin(21))      # Comunicación I2C
oled = SSD1306_I2C(128, 64, i2c)            # Pantalla OLED
mpu = MPU6050Mini(i2c)                      # Sensor MPU6050

# Joystick analógico (Jugador 2)
joystick = ADC(Pin(2))
joystick.atten(ADC.ATTN_11DB)
joystick.width(ADC.WIDTH_12BIT)

# Botón físico (Jugador 2 - Power-Up)
button_p2 = Pin(18, Pin.IN, Pin.PULL_UP)    # Activo en LOW


# --- Constantes del juego ---
WIDTH = 128
HEIGHT = 64


class Pong:
    """
    Clase principal que implementa la lógica del juego Pong.
    Incluye manejo de pelota, barras, puntuaciones y power-ups.
    """
    def __init__(self, oled):
        self.oled = oled

        # Estado inicial de la pelota
        self.ball_x = WIDTH // 2
        self.ball_y = HEIGHT // 2
        self.vx = 2
        self.vy = 1

        # Barras (paddles)
        self.paddle_w = 2
        self.paddle1_h = 12
        self.paddle2_h = 12
        self.p1_y = HEIGHT // 2 - self.paddle1_h // 2
        self.p2_y = HEIGHT // 2 - self.paddle2_h // 2

        # Marcador
        self.score1 = 0
        self.score2 = 0

        # Power-Ups
        self.paddle1_powered = False
        self.p1_power_start = 0
        self.paddle2_powered = False
        self.p2_power_start = 0
        self.powerup_duration = 3000  # milisegundos
        self.powerup_size = 24        # tamaño de paddle al activar

    def update_paddles(self):
        """
        Actualiza las posiciones de las barras (jugadores).
        - Jugador 1 con inclinación MPU6050.
        - Jugador 2 con joystick analógico.
        - Ambos tienen acceso a Power-Ups.
        """
        # --- Jugador 1 (MPU6050) ---
        tilt = mpu.get_tilt()
        self.p1_y += int(tilt * 4)

        # Power-Up con movimiento brusco
        if abs(tilt) > 0.8 and not self.paddle1_powered:
            self.paddle1_h = self.powerup_size
            self.paddle1_powered = True
            self.p1_power_start = time.ticks_ms()

        # Desactivar power-up tras duración
        if self.paddle1_powered and time.ticks_diff(time.ticks_ms(), self.p1_power_start) > self.powerup_duration:
            self.paddle1_h = 12
            self.paddle1_powered = False

        # --- Jugador 2 (Joystick analógico) ---
        val = joystick.read()
        mapped = int((val / 4095) * (HEIGHT - self.paddle2_h))
        self.p2_y = mapped

        # Power-Up con botón físico
        if button_p2.value() == 0 and not self.paddle2_powered:
            self.paddle2_h = self.powerup_size
            self.paddle2_powered = True
            self.p2_power_start = time.ticks_ms()

        if self.paddle2_powered and time.ticks_diff(time.ticks_ms(), self.p2_power_start) > self.powerup_duration:
            self.paddle2_h = 12
            self.paddle2_powered = False

        # Límites de pantalla
        if self.p1_y < 0: self.p1_y = 0
        if self.p1_y > HEIGHT - self.paddle1_h: self.p1_y = HEIGHT - self.paddle1_h
        if self.p2_y < 0: self.p2_y = 0
        if self.p2_y > HEIGHT - self.paddle2_h: self.p2_y = HEIGHT - self.paddle2_h

    def update_ball(self):
        """
        Lógica de movimiento de la pelota y detección de colisiones.
        """
        self.ball_x += self.vx
        self.ball_y += self.vy

        # Rebote contra bordes superior/inferior
        if self.ball_y <= 0 or self.ball_y >= HEIGHT - 1:
            self.vy = -self.vy

        # Colisión con paddle izquierdo (Jugador 1)
        if self.ball_x <= 3:
            if self.p1_y <= self.ball_y <= self.p1_y + self.paddle1_h:
                self.vx = -self.vx
            else:
                self.score2 += 1
                self.reset_ball()

        # Colisión con paddle derecho (Jugador 2)
        if self.ball_x >= WIDTH - 3:
            if self.p2_y <= self.ball_y <= self.p2_y + self.paddle2_h:
                self.vx = -self.vx
            else:
                self.score1 += 1
                self.reset_ball()

    def reset_ball(self):
        """
        Reinicia la pelota al centro tras un punto.
        """
        self.ball_x = WIDTH // 2
        self.ball_y = HEIGHT // 2
        self.vx = -self.vx
        self.vy = 1 if self.vy > 0 else -1

    def draw(self):
        """
        Dibuja todos los elementos en pantalla:
        - Paddles
        - Pelota
        - Marcador
        - Indicadores de Power-Up
        """
        o = self.oled
        o.fill(0)
        # Paddles
        o.fill_rect(0, self.p1_y, self.paddle_w, self.paddle1_h, 1)
        o.fill_rect(WIDTH - self.paddle_w, self.p2_y, self.paddle_w, self.paddle2_h, 1)
        # Pelota
        o.pixel(self.ball_x, self.ball_y, 1)
        # Marcador
        o.text(str(self.score1), 30, 0)
        o.text(str(self.score2), 90, 0)
        # Power-Up activo
        if self.paddle1_powered:
            o.text("P1 POWER!", 5, 56)
        if self.paddle2_powered:
            o.text("P2 POWER!", 70, 56)
        o.show()

    def loop(self):
        """
        Bucle principal del juego.
        """
        while True:
            self.update_paddles()
            self.update_ball()
            self.draw()
            time.sleep_ms(40)


# --- Pantalla de inicio ---
oled.fill(0)
oled.text("PONG 2P", 30, 20)
oled.text("MPU vs Joystick", 0, 40)
oled.show()
time.sleep(2)

# Iniciar juego
pong = Pong(oled)
pong.loop()