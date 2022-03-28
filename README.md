# FarmaciaBrazoRobotGUI
Interfaz gráfica para solicitudes de medicamentos vía código QR para farmacia, con un brazo robot de 6GDL. Visión artificial implementada para la reposición.

## Materiales
* Placa Arduino
* Teléfono celular con la aplicación IP Webcam
* Brazo de 6GDL (Se ha utilizado impresión 3D)
* Ordenador


### Pre-requisitos 📋

* Verificar que se encuentra instalada la librería Servo.h para el arduino.
 
* Instalación del programa [IP Webcam](https://www.programaspato.com/es/2012/04/ipwebcam-aplicacion-para-utilizar-webcam-de-movil-android-con-pc-via-wifi/) en el teléfono móvil, o aplicación similar, para la lectura del QR en la reposición. Variar la resolución de la cámara de ser necesario.

* Creación de la base de datos, con el código BD.sql y agregar los medicamentos disponibles con BD_agregar.sql

* Generar códigos QR con el formato _ID:Nombre:Cantidad_ para simular las solicitudes de medicamento por parte del cliente. Para este punto se ha utilizado [una página online](https://www.codigos-qr.com/generador-de-codigos-qr/)

## Requisitos del Proyecto
* El plano de reposición no es el mismo al plano de almacenaje, por lo que el robot deberá trabajar para transportar los medicamentos de la línea de la cinta transportadora al rack de medicamentos.

* El plano del usuario no es el mismo al plano del rack de medicamentos ni al plano de reposición.

* La cámara debe permitir identificar el medicamento (código QR) y estimar el largo y ancho en centímetros (mostrar en pantalla proceso de reposición).

* Los medicamentos y las recetas estarán codificadas utilizando codificación QR. Para la solicitud del cliente con formato _ID:Nombre:Cantidad_, para reposición con el formato _ID:Nombre_

* Para la lectura del código QR del cliente, se utilizará la cámara del ordenador, para la lectura del código QR del medicamento para reposición se utilizará la cámara del móvil.

* La interfaz con el usuario deberá mostrar al usuario la receta leída, incluyendo cantidad y la disponibilidad, y consultar su confirmación sobre el pedido (por teclado). Además, debe avisar al usuario con mensajes de espera y cuando puede abrir la caja para retirar su producto. Si no hay disponible el producto también debe notificar al usuario.

* Mejoras en interfaz con el reponedor (puerta de desplazamiento, LEDs para avisar sobre estado del proceso, etc.). Al presionarse el botón de reposición se debe mostrar un aviso en pantalla de que la puerta física de reposición se encuentra abierta, dos LEDS se encienden. Una vez que se vuelve a presionar, esta puerta física se cierra y se abre la ventana de reposición en pantalla, donde se ve la cámara del móvil, la decodificación del código QR y las dimensiones del medicamento.

### Modificaciones a realizar 🔧

Con el código calibración motores se deben definir las posiciones de los servos para cada posición del estante.

Se deben hacer los cambios necesarios en el código pedido.py para lograr una conexión correcta con la Base de Datos. (Cambiar user, password, nombre de la BD, de ser necesarios)


## Construido con 🛠️

* [Tkinter](https://docs.python.org/3/library/tkinter.html/) -Desarrollo de la interfaz gráfica
* [MySQL-Connector](https://dev.mysql.com/doc/connector-python/en/) - Conexión con la base de datos


----------------------------------------------------------

**Giohanna Martinez** - [gmfv](https://github.com/gmfv) 😊

#### El proyecto se ha desarrollado como proyecto final de Robótica 1 en la carrera de Ingeniería Mecatrónica de la FIUNA
