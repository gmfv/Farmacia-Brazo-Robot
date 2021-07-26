# FarmaciaBrazoRobotGUI
Interfaz gráfica para solicitudes de medicamentos vía código QR para farmacia, con un brazo robot de 6GDL. Visión artificial implementada para la reposición

## Materiales 🚀

* Piezas de impresión 3D de todas las partes del brazo robótico.
* 3 Servos MG996R y 3 servos SG90.
* 1 Arduino UNO y su cable USB.
* 1 botón.
* Cables jumpers.
* Adaptador DC de 6V para alimentación de todos los servos.
* Estante de 4x4

## Requisitos del Proyecto
* El plano de reposición no es el mismo al plano de almacenaje, por lo que el robot deberá trabajar para transportar los medicamentos de la línea de la cinta transportadora al rack de medicamentos.

* El plano del usuario no es el mismo al plano del rack de medicamentos ni al plano de reposición.

* La cámara debe permitir identificar el medicamento (código QR) y estimar el largo y ancho en centímetros (mostrar en pantalla proceso de reposición).

* Los medicamentos y las recetas estarán codificadas utilizando codificación QR. Para la solicitud del cliente con formato _ID:Nombre:Cantidad_, para reposición con el formato _ID:Nombre_

* Para la lectura del código QR del cliente, se utiliza la cámara del ordenador, para la lectura del código QR del medicamento para reposición se utiliza la cámara del móvil.

* La interfaz con el usuario deberá mostrar al usuario la receta leída, incluyendo cantidad y la disponibilidad, y consultar su confirmación sobre el pedido (por teclado). Además, debe avisar al usuario con mensajes de espera y cuando puede abrir la caja para retirar su producto. Si no hay disponible el producto también debe notificar al usuario.

* Mejoras en interfaz con el reponedor (puerta de desplazamiento, LEDs para avisar sobre estado del proceso, etc.). Al apretar el botón de reposición se muestra en pantalla que la puerta física de reposición se encuentra abierta, dos LEDS se encienden. Una vez que se vuelve a presionar, esta puerta física se cierra y se abre la ventana de reposición en pantalla, donde se ve la cámara del móvil, la decodificación del código QR y las dimensiones del medicamento.

### Pre-requisitos 📋

Verificar que se encuentra instalada la librería Servo.h para el arduino.
 
Instalación del programa [IP Webcam](https://www.programaspato.com/es/2012/04/ipwebcam-aplicacion-para-utilizar-webcam-de-movil-android-con-pc-via-wifi/) en el teléfono móvil, o aplicación similar, para la lectura del QR en la reposición. Variar la resolución de la cámara de ser necesario.

Creación de la base de datos, con el código BD.sql y agregar los medicamentos disponibles con BD_agregar.

### Modificaciones a realizar 🔧

Con el código calibración motores se deben definir las posiciones de los servos para cada posición del estante.

Se deben hacer los cambios necesarios en el código pedido.py para lograr una conexión correcta con la Base de Datos. (Cambiar user, password, nombre de la BD, de ser necesarios)


## Construido con 🛠️

* [Tkinter](https://docs.python.org/3/library/tkinter.html/) -Desarrollo de la interfaz gráfica
* [MySQL-Connector](https://dev.mysql.com/doc/connector-python/en/) - Conexión con la base de datos


## Autor ✒️

* **Giohanna Martinez** - [gmfv](https://github.com/gmfv) 😊
