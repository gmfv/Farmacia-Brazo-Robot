# Farmacia con brazo robot y solicitudes en código QR
Interfaz gráfica para solicitudes de medicamentos vía código QR para farmacia + control del movimiento de un brazo robot de 6GDL + visión artificial implementada para la reposición.

## Objetivos
### Objetivo General
* Diseñar e implementar un sistema robótico para la automatización de la reposición, manejo de stock y retiro de productos.
### Objetivos específico
* Diseñar e implementar un sistema de base de datos para aumentar la
eficiencia en el manejo de stock.
* Generación de una interfaz gráfica que comunique un programa ejecutándose
en el ordenador con el arduino.
* Controlar servomotores con el arduino para general el movimiento del robot.

## GUI
A continuación se muestran la ventana principal y la ventana de solicitud de medicamento. Al ejecutarse la operación de reposición la ventana principal queda bloqueada.

### Ventana Principal
<img src="https://github.com/gmfv/Farmacia-Brazo-Robot/blob/main/VentanaPrincipal.jpg" width="300" height="250">

### Ventana de solicitud de medicamento
<img src="https://github.com/gmfv/Farmacia-Brazo-Robot/blob/main/VentanaSolicitud.jpg" width="350" height="250">

## Materiales
### Generales
* Placa Arduino UNO + cable USB
* Teléfono celular con la aplicación IP Webcam
* Ordenador
* Estante de 4x4 espacios de 10 cm x 10 cm

### Brazo de 6GDL
* 3 Servos MG996R
* 3 servos SG90
* 1 servo REV 40 1097 para el slider.
* Piezas de impresión 3D de las guías del slider.

<img src="https://github.com/gmfv/Farmacia-Brazo-Robot/blob/main/impresiones3D.jpg" width="300" height="300">

* Estructura de base acrílica para el slider.
* Perfiles de aluminio para que la guías del slider quepan con precisión.
* Correa dentada de 6 mm.
* 2 engranajes con topes para el slider, a uno y otro lado del mismo.

<img src="https://github.com/gmfv/Farmacia-Brazo-Robot/blob/main/RielesyPoseas.jpg" width="300" height="300">

* 1 botón.
* Cables jumpers.
* Adaptador DC de 6V para alimentación de todos los servos.

<img src="https://github.com/gmfv/Farmacia-Brazo-Robot/blob/main/BrazoCompleto.jpg" width="300" height="300">

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
* [OpenCV](https://pypi.org/project/opencv-python/) - Reconocimiento de imágenes QR

----------------------------------------------------------

**Giohanna Martinez** - [gmfv](https://github.com/gmfv) 😊

#### El proyecto se ha desarrollado como proyecto final de Robótica 1 en la carrera de Ingeniería Mecatrónica de la FIUNA
