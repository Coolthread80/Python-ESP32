from machine import Pin, PWM#Machine contiene todo lo que necesitamos para que funcione el esp32
from hcsr04 import HCSR04#Librería para el ultrasónico
import time#Para el tiempo dormido
import socket#Para crear el web server
import network#Para conectar el esp32 a internet
import gc#Para comprobar el estado de memoria del esp32
import select#Para hacer instrucciones de forma simultánea

def conectaralwaifai(SSID, PASSWORD):#Esto se encarga de hacer que el esp32 se conecte a internet
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        print('Conectando', SSID + "...")
        while not sta_if.isconnected():
            pass
    print('Network configuration (IP/netmask/gw/DNS):', sta_if.ifconfig())

def web_page():#El que crea una web page simple
    html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
    <body><h1>ESP Web Server</h1><a href=\"?led=on\"><button>ON</button></a>&nbsp;
    <a href=\"?led=off\"><button>OFF</button></a></body></html>"""
    return html

#Nombre de la red y contraseña
SSID = "itmerida"#Totalplay-2.4G-8600
PASSWORD = ""#H8JK9EdMPmahBUgZ

#Método que lo conecta a internet
conectaralwaifai(SSID, PASSWORD)

#El que se encarga de iniciar la web page
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

chi = False
nio = False

while True:
    try:
        sensor = HCSR04(trigger_pin=13, echo_pin=12, echo_timeout_us=10000)#El que lanza el ultrasónico en los pines 12 y 12+1
        
        led = Pin(2, Pin.OUT)#Ledsito
      
        IN1 = Pin(5,Pin.OUT)#Declaramos los pines para que manden información
        IN2 = Pin(4,Pin.OUT)
        IN3 = Pin(22,Pin.OUT)
        IN4 = Pin(23,Pin.OUT)
        
        frecuencia = 5000#Frecuencia a la que funciona el que se encarga de manejar las ruedas
        ENA = PWM(Pin(18), frecuencia)#Rueda izquierda (creo)
        ENB = PWM(Pin(19), frecuencia)#Rueda derecha (creo)
        
        if gc.mem_free() < 102000:#Si hay memoria libre entonces la agarra
            gc.collect()
            
        if chi:#Si chi es verdadero
            
            led.value(1)
            
            distancia = sensor.distance_cm()#Medimos la distancia
            print ('Distancia:', distancia, 'cm')
                      
            #La fuerza a la que se mueven las ruedas
            ENA.duty(1023)#1023
            ENB.duty(1023)#1023
            
            #Este habla por sí solo
            if distancia > 15 or distancia < 0:
                IN1.value(1)
                IN3.value(1)
                IN2.value(0)
                IN4.value(0)
                
            #Este también
            if distancia <= 15 and distancia >= 0:
                
                #Se detiene
                IN1.value(0)
                IN3.value(0)
                IN2.value(0)
                IN4.value(0)
                time.sleep(2)
                
                #Para atrás
                IN1.value(0)
                IN3.value(0)
                IN2.value(1)
                IN4.value(1)
                time.sleep(1)
                
                #Se detiene
                IN1.value(0)
                IN3.value(0)
                IN2.value(0)
                IN4.value(0)
                time.sleep(1)
                
                #Da la vuelta sobre sí mismo
                IN1.value(1)
                IN3.value(0)
                IN2.value(0)
                IN4.value(1)
                time.sleep(0.5)
                
                #Se detiene
                IN1.value(0)
                IN3.value(0)
                IN2.value(0)
                IN4.value(0)
                time.sleep(0.5)
                
        elif nio:#Si nio es verdadero
            
            led.value(0)
            
            print('Led apagao')
            time.sleep(0.2)
            
            #Se detiene
            IN1.value(0)
            IN3.value(0)
            IN2.value(0)
            IN4.value(0)
            
        lector, escritor, condi = select.select([s], [], [], 0.1)
        
        """Select se encarga de recibir información al mismo tiempo que está mandando, en este caso nos interesa que esta
        cosa espere a recibir la señal mientras el resto del código se sigue ejecutando, por ejemplo, solo tarda 0.1 de segundo en decir 'ya me cansé, que sigan su camino0 y sigue
        el resto del código, si en lugar de 0.1 tuvieramos None entonces el código esperaría indefinitamente hasta que recibamos un dato,
        y entonces el ultrasónico dejarpia de funcionar, que es lo mismo que pasaba antes y estuvimos un buen ratote"""
        
        for socket in lector:#Se encarga de leer los datos en s, que es el socket y si nota algún cambio entonces cambiarán los valores
            conn, addr = s.accept()#Se conecta y devuelve la dirección
            conn.settimeout(3.0)#3 segundos de que diga nel pastel
            print('Conexión recibida de %s' % str(addr))#Imprime la dirección de quien vino la conexión
            request = conn.recv(1024)#Se encarga de recibir datos
            conn.settimeout(None)#Con un tiempo nulo
            request = str(request)#Imprime el
            print('Contenido = %s' % request)#estado actual del web server
            led_on = request.find('/?led=on')#Se encarga de detectar si alguien entra a '?led=on'
            led_off = request.find('/?led=off')#Se encarga de detectar si alguien entra a '?led=off'
        
            if led_on == 6:#Si led_on entonces se harán las cosas de allá arriba
                chi = True
                nio = False
                      
            if led_off == 6:#Si led_off entonces se hará lo otro que está arriba
                chi = False
                nio = True
            
            #Y esto se encarga de terminar la página
            response = web_page()

            #Y esto de hacer que funcione correctamente
            conn.send(b'HTTP/1.1 200 OK\n')#Dice que sí recibió los datos correctamente
            conn.send(b'Content-Type: text/html\n')#Esto enviará los datos en html
            conn.send(b'Connection: close\n\n')#Esto cerrará la conexión
            conn.sendall(response.encode('utf-8'))#Esto hará que la página refleje el resultado
            conn.close()#Y esto terminará de mandar los datos cerrando la conexión con el web server
    
    except OSError as e:#chi
        conn.close()
        print('Connection closed')
