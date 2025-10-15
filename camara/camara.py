# Importar las bibliotecas necesarias
import camera # Para controlar la cámara
import network # Para conectarse a Wi-Fi
import socket # Para crear un servidor web
import time # Para manejar pausas
#----------------------------------------
# PASO 1: Conexión a la red Wi-Fi
#----------------------------------------
def conectar_wifi(ssid, password):
 """
 Función para conectarse a una red Wi-Fi.
 :param ssid: Nombre de la red Wi-Fi
 :param password: Contraseña de la red Wi-Fi
 :return: Dirección IP asignada al dispositivo
 """
 wlan = network.WLAN(network.STA_IF)
 # Configurar la interfaz de red
 wlan.active(True) # Activar la interfaz
 # Conectar a la red Wi-Fi
 wlan.connect(ssid, password)
 
 print('Conectando a la red Wi-Fi...')
 while not wlan.isconnected(): # Esperar hasta que se establezca la conexión
    time.sleep(1)
    print('.', end='') # Mostrar puntos para indicar que se está intentando conectar
 print('\n¡Conexión exitosa!')
 print('Dirección IP asignada:', wlan.ifconfig()[0]) # Mostrar la dirección IP
 return wlan.ifconfig()[0] # Retornar la dirección IP

#----------------------------------------
# PASO2: Inicializar la cámara
#----------------------------------------
def inicializar_camara():
 """
 Función para inicializar la cámara.
 """
 try:
    camera.init(0, format=camera.JPEG)#Inicializar la cámara en formato JPEG
    camera.framesize(camera.FRAME_240X240) # Establecer el tamaño de la imagen (240x240 píxeles)
    print('Cámara inicializada correctamente.')
 except Exception as e:
    print('Error al inicializar la cámara:', e)

 
#----------------------------------------
# PASO3: Tomar una foto
#----------------------------------------
def tomar_foto():
 """
 Función para capturar una foto con la
 cámara.
 :return: Los datos de la imagen capturada.
 """
 print('Tomando una foto...')
 try:
    foto = camera.capture() # Capturar la imagen
    print('Foto tomada exitosamente.')
    return foto
 except Exception as e:
    print('Error al tomar la foto:', e)
    return None


 
#----------------------------------------
# PASO4: Configurar el servidor web
#----------------------------------------
def iniciar_servidor(ip):
 """
 Función para iniciar un servidor web que permite ver la cámara.
 :param ip: Dirección IP del dispositivo
 """
 addr = (ip, 80) # Dirección IP y puerto del servidor (puerto 80 es estándar para HTTP)
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crear un socket TCP/IP
 s.bind(addr) # Enlazar el socket a la dirección IP y puerto
 s.listen(1) # Escuchar conexiones entrantes (1 cliente a la vez)
 print('Servidor web iniciado en http://%s:80' % ip)
 while True:
    conn, addr = s.accept() # Aceptar una conexión entrante
    print('Conexión desde:', addr)
    request = conn.recv(1024) # Recibir la solicitud del cliente
    print('Solicitud recibida:', request)
 
 # Verificar si el cliente solicitó una foto
    if b'GET /foto' in request:
        foto = tomar_foto() # Tomar una foto
        if foto:
           # Enviar la foto como respuesta HTTP
           conn.send(b'HTTP/1.1 200 OK\r\n') # Código de estado HTTP 200 (OK)
           conn.send(b'Content-Type: image/jpeg\r\n\r\n') # Tipo de contenido: imagen JPEG
           conn.send(foto) # Enviar los datos de la imagen
        else:
           # Si no se pudotomar lafoto, enviar un mensaje de error
           conn.send(b'HTTP/1.1 500 Internal Server Error\r\n')
           conn.send(b'Content-Type: text/html\r\n\r\n')
           conn.send(b'<html><body><h1>Error al tomar la foto</h1></body></html>')
    else:
       # Si el cliente accede a la página principal, mostrar instrucciones
       conn.send(b'HTTP/1.1 200 OK\r\n')
       conn.send(b'Content-Type: text/html\r\n\r\n')
       conn.send(b'<html><body>')
       conn.send(b'<h1>Servidor ESP32-CAM</h1>')
       conn.send(b'<p>Ir a <a href="/foto">/foto</a> para ver la foto.</p>')
       conn.send(b'</body></html>')
       


#----------------------------------------
# PROGRAMAPRINCIPAL
#----------------------------------------
if __name__ == '__main__':
 # Configurar la red Wi-Fi
 ssid = 'INFINITUM659E' # Cambia esto por el nombre de tu red Wi-Fi
 password = '6DayQ2DDGs' # Cambia esto por la contraseña de tu red Wi-Fi
 # PASO1: Conectar a la red Wi-Fi
 ip = conectar_wifi(ssid, password)
 # PASO2: Inicializar la cámara
 inicializar_camara()
 # PASO3: Iniciar el servidor web
 iniciar_servidor(ip)