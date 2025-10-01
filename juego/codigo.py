"""
pong2players_oled.py
MicroPython (ESP32) - Juego tipo "Pong clásico" con 2 jugadores + PowerUps.

- Jugador 1: MPU6050, power-up con movimiento brusco.
- Jugador 2: Joystick + botón (pin 18), power-up al presionar el botón.
"""

from machine import Pin, I2C, ADC
import time
from ssd1306 import SSD1306_I2C

# --- Mini driver MPU6050 ---
class MPU6050Mini:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')

    def read_raw(self):
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
        ax, ay, az = self.read_raw()
        return ay / 16384  # Normalizado

# --- Configuración hardware ---
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(128, 64, i2c)
mpu = MPU6050Mini(i2c)

# Joystick
joystick = ADC(Pin(2))
joystick.atten(ADC.ATTN_11DB)
joystick.width(ADC.WIDTH_12BIT)

# Botón del jugador 2 (power-up)
button_p2 = Pin(18, Pin.IN, Pin.PULL_UP)  # activo en LOW

# --- Juego Pong ---
WIDTH = 128
HEIGHT = 64

class Pong:
    def __init__(self, oled):
        self.oled = oled
        self.ball_x = WIDTH // 2
        self.ball_y = HEIGHT // 2
        self.vx = 2
        self.vy = 1
        self.paddle_w = 2

        # Paddles individuales
        self.paddle1_h = 12
        self.paddle2_h = 12
        self.p1_y = HEIGHT // 2 - self.paddle1_h // 2
        self.p2_y = HEIGHT // 2 - self.paddle2_h // 2

        # Scores
        self.score1 = 0
        self.score2 = 0

        # PowerUps
        self.paddle1_powered = False
        self.p1_power_start = 0
        self.paddle2_powered = False
        self.p2_power_start = 0
        self.powerup_duration = 3000  # ms
        self.powerup_size = 24

    def update_paddles(self):
        # --- Jugador 1 (MPU) ---
        tilt = mpu.get_tilt()
        self.p1_y += int(tilt * 4)

        # Activar power-up con movimiento brusco
        if abs(tilt) > 0.8 and not self.paddle1_powered:
            self.paddle1_h = self.powerup_size
            self.paddle1_powered = True
            self.p1_power_start = time.ticks_ms()

        # Desactivar power-up
        if self.paddle1_powered and time.ticks_diff(time.ticks_ms(), self.p1_power_start) > self.powerup_duration:
            self.paddle1_h = 12
            self.paddle1_powered = False

        # --- Jugador 2 (Joystick) ---
        val = joystick.read()
        mapped = int((val / 4095) * (HEIGHT - self.paddle2_h))
        self.p2_y = mapped

        # Power-up jugador 2 con botón
        if button_p2.value() == 0 and not self.paddle2_powered:  # presionado
            self.paddle2_h = self.powerup_size
            self.paddle2_powered = True
            self.p2_power_start = time.ticks_ms()

        if self.paddle2_powered and time.ticks_diff(time.ticks_ms(), self.p2_power_start) > self.powerup_duration:
            self.paddle2_h = 12
            self.paddle2_powered = False

        # Limitar dentro de pantalla
        if self.p1_y < 0: self.p1_y = 0
        if self.p1_y > HEIGHT - self.paddle1_h: self.p1_y = HEIGHT - self.paddle1_h
        if self.p2_y < 0: self.p2_y = 0
        if self.p2_y > HEIGHT - self.paddle2_h: self.p2_y = HEIGHT - self.paddle2_h

    def update_ball(self):
        self.ball_x += self.vx
        self.ball_y += self.vy

        # Rebote arriba/abajo
        if self.ball_y <= 0 or self.ball_y >= HEIGHT - 1:
            self.vy = -self.vy

        # Paddle izquierda
        if self.ball_x <= 3:
            if self.p1_y <= self.ball_y <= self.p1_y + self.paddle1_h:
                self.vx = -self.vx
            else:
                self.score2 += 1
                self.reset_ball()

        # Paddle derecha
        if self.ball_x >= WIDTH - 3:
            if self.p2_y <= self.ball_y <= self.p2_y + self.paddle2_h:
                self.vx = -self.vx
            else:
                self.score1 += 1
                self.reset_ball()

    def reset_ball(self):
        self.ball_x = WIDTH // 2
        self.ball_y = HEIGHT // 2
        self.vx = -self.vx
        self.vy = 1 if self.vy > 0 else -1

    def draw(self):
        o = self.oled
        o.fill(0)
        # Dibujar paddles
        o.fill_rect(0, self.p1_y, self.paddle_w, self.paddle1_h, 1)
        o.fill_rect(WIDTH - self.paddle_w, self.p2_y, self.paddle_w, self.paddle2_h, 1)
        # Pelota
        o.pixel(self.ball_x, self.ball_y, 1)
        # Scores
        o.text(str(self.score1), 30, 0)
        o.text(str(self.score2), 90, 0)
        # Indicadores Power-up
        if self.paddle1_powered:
            o.text("P1 POWER!", 5, 56)
        if self.paddle2_powered:
            o.text("P2 POWER!", 70, 56)
        o.show()

    def loop(self):
        while True:
            self.update_paddles()
            self.update_ball()
            self.draw()
            time.sleep_ms(40)

# --- Inicio ---
oled.fill(0)
oled.text("PONG 2P", 30, 20)
oled.text("MPU vs Joystick", 0, 40)
oled.show()
time.sleep(2)

pong = Pong(oled)
pong.loop()