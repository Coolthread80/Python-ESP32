<h1>Proyectos usando ESP32</h1>

<p>Por ahora solo tengo el carro que hice hace tiempo, pero solo conservo los archivos .py, porque entre que ya tiene un tiempo y que nos cambiamos de casa, no pude encontrarlo entre nuestras cosas.</p>

<p>El carro es controlado por un ESP32 y usa MicroPython. Tiene dos motores DC controlados por un puente H L298N, y un sensor ultrasónico HC-SR04 para evitar obstáculos. La comunicación con el carro se realiza a través de WiFi, usando sockets para enviar comandos desde una pagina web que se accede mediante el propio internet usando una ip que se asigna al ejecutar el script.</p>

<p>El código se encuentra en la carpeta de <a href="https://github.com/Coolthread80/Python-ESP32/tree/main/Webserver_car">aquí arriba.</a></p>

<img src="https://github.com/Coolthread80/Python-ESP32/blob/main/Webserver_car/evidence.gif" alt="">
<p>(Video de hace más de 3.5 años, cuando todavía era la versión antigua)</p>