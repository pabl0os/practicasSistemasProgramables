from machine import Pin, ADC
import time

# Configuración de pines
# Ejes analógicos del joystick
adc_x = ADC(Pin(4))  # Eje X en pin 4
adc_y = ADC(Pin(2))  # Eje Y en pin 2

# Botón del joystick (entrada digital con pull-up)
boton = Pin(18, Pin.IN, Pin.PULL_UP)

# Configurar atenuación para lectura ADC (0-3.3V)
adc_x.atten(ADC.ATTN_11DB)
adc_y.atten(ADC.ATTN_11DB)

def leer_joystick():
    """
    Lee los valores del joystick y retorna un diccionario con los datos
    """
    # Leer valores analógicos (0-4095)
    valor_x = adc_x.read()
    valor_y = adc_y.read()
    
    # Convertir a porcentaje (0-100%)
    porcentaje_x = (valor_x / 4095) * 100
    porcentaje_y = (valor_y / 4095) * 100
    
    # Leer estado del botón (0 = presionado, 1 = no presionado debido al pull-up)
    estado_boton = not boton.value()  # Invertir para que True = presionado
    
    return {
        'x_raw': valor_x,
        'y_raw': valor_y,
        'x_percent': round(porcentaje_x, 2),
        'y_percent': round(porcentaje_y, 2),
        'boton_presionado': estado_boton
    }

def detectar_direccion(x_percent, y_percent, umbral=20):
    """
    Detecta la dirección del joystick basándose en los porcentajes
    umbral: porcentaje mínimo para considerar movimiento
    """
    direccion = "CENTRO"
    
    # Detectar movimiento en X
    if x_percent < (50 - umbral):
        direccion = "IZQUIERDA"
    elif x_percent > (50 + umbral):
        direccion = "DERECHA"
    
    # Detectar movimiento en Y
    if y_percent < (50 - umbral):
        if direccion == "CENTRO":
            direccion = "ABAJO"
        else:
            direccion += "-ABAJO"
    elif y_percent > (50 + umbral):
        if direccion == "CENTRO":
            direccion = "ARRIBA"
        else:
            direccion += "-ARRIBA"
    
    return direccion

def main():
    """
    Función principal que lee continuamente el joystick
    """
    print("=== LECTURA DE JOYSTICK ===")
    print("Eje X: Pin 4")
    print("Eje Y: Pin 2") 
    print("Botón: Pin 18")
    print("Presiona Ctrl+C para salir\n")
    
    try:
        while True:
            # Leer valores del joystick
            datos = leer_joystick()
            
            # Detectar dirección
            direccion = detectar_direccion(datos['x_percent'], datos['y_percent'])
            
            # Mostrar información
            print(f"X: {datos['x_raw']:4d} ({datos['x_percent']:6.2f}%) | "
                  f"Y: {datos['y_raw']:4d} ({datos['y_percent']:6.2f}%) | "
                  f"Botón: {'SI' if datos['boton_presionado'] else 'NO':2s} | "
                  f"Dirección: {direccion}")
            
            # Pequeña pausa para no saturar la consola
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\nLectura del joystick terminada.")

# Ejecutar el programa principal
if __name__ == "__main__":
    main()
