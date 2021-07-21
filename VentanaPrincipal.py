import tkinter as tk
import serial
import time
import threading
from tkinter import ttk
from tkinter import messagebox as mb
import cv2
from object_detector import *
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
import pedido
import tkinter.font as font

class FormularioFarmacia:
    def __init__(self, master):
        self.pedido1 = pedido.Pedido()
        self.master=master
        self.master.title("FARMACIA AUTOMATIZADA")
        imagen2=Image.open("MenuPrincipal_I.jpg")
        self.img = ImageTk.PhotoImage(imagen2)  # PIL solution
        self.background_label = tk.Label(self.master, image=self.img)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.pack()
        self.t1 = threading.Thread(target=self.ventanamed)
        self.t2 = threading.Thread(target=self.ventanaprocess)
        self.t3 = threading.Thread(target=self.ventanarepon)
        self.t1.daemon = True
        self.t2.daemon = True
        self.t3.daemon = True
        self.fuente1 = font.Font(family='Gadugi', size=9, weight='bold')
        self.fuente2 = font.Font(family='Gadugi', size=9, )
        self.saludo = tk.Label(self.master, text="¡BIENVENIDO! \n Seleccione *PEDIDO* \npara solicitar \nun medicamento", bg='light blue', height=4, width=20)
        self.saludo['font'] = self.fuente1
        self.saludo.place(x=10, y= 130)
        self.button1state = tk.Button(self.master, text="PEDIDO", command=self.AbrirVentanaCliente, height=2, width=15, bg='light cyan', fg='black')
        self.button1state['font'] =self.fuente1
        self.button1state.place(x=235, y= 90)
        #self.button2state = tk.Button(self.master, text="REPOSICIÓN", command=self.AbrirVentanaReposicion, height=2, width=15, bg='light cyan', fg='black' )
        #self.button2state['font'] =self.fuente1
        #self.button2state.place(x=235, y= 200)
        self.button3state = tk.Button(self.master, text="SALIR", command=self.master.quit, height=2, width=15,  bg='light cyan', fg='black')
        self.button3state['font'] =self.fuente1
        self.button3state.place(x=120, y= 296)
        self.ser = serial.Serial('COM3', 115200, timeout=.1)
        self.LecturaSerial()
    def AbrirVentanaCliente(self):
        try:
            self.t1.start()
        except:
            self.ventanamed()

    def AbrirVentanaReposicion(self):
        try:
            self.t3.start()
        except:
            self.ventanarepon()

    def LecturaSerial(self):
        self.lectura= self.ser.readline().decode('utf-8').strip()
        if (self.lectura == "R1"):
            self.saludo['text']= "FUERA DE SERVICIO\nNUESTRO ROBOT'i\n ESTÁ REPONIENDO \nSTOCK"
            self.AbrirVentanaReposicion()
            #self.master.after(10, self.LecturaSerial)
        elif (self.lectura == "P"):
            self.saludo['text']= "PUERTA DEL\n REPONEDOR ABIERTA"
        elif(self.lectura=="RF"):
            self.saludo['text']= "¡BIENVENIDO! \n Seleccione *PEDIDO* \npara solicitar \nun medicamento"
        self.master.after(100, self.LecturaSerial)

    def EscrituraSerial(self, x):
        self.ser.write(bytes(x, 'UTF-8'))

    def ventanamed(self):
        self.master.withdraw()
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title("SOLICITUD DE MEDICAMENTO")
        self.newWindow.geometry("700x500")
        width, height = 200, 150
        self.saludos2 = tk.Label(self.newWindow, text="CAMARA INICIALIZÁNDOSE, \nPODRÍA DEMORAR 15 SEGUNDOS.\n AGRADECEMOS SU PACIENCIA")
        self.saludos2.pack()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        imagen2=Image.open("background3.jpg")
        self.imgvm = ImageTk.PhotoImage(imagen2)  # PIL solution
        self.background_labelvm = tk.Label(self.newWindow, image=self.imgvm)
        self.background_labelvm.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_labelvm.pack()
        self.lmain = tk.Label(self.newWindow, text="CAMARA INICIALIZÁNDOSE, \nPODRÍA DEMORAR 15 SEGUNDOS.\n AGRADECEMOS SU PACIENCIA")
        self.lmain.place(x=330, y=10)
        self.saludos2['text']=""
        self.show_frame()
        self.tkLabel2 = tk.Label(self.newWindow, text="Acerque el código QR \nde su receta a la \ncámara. Por favor", bg='light blue')
        self.tkLabel2['font'] =self.fuente1
        self.tkLabel2.place(x=180, y=100)
        self.labelid = tk.Label(self.newWindow, text="ID: ", bg='light blue')
        self.labelid['font'] =self.fuente2
        self.labelid.place(x=350, y=140+70)
        self.idcarga = tk.StringVar()
        self.entryid = ttk.Entry(self.newWindow, textvariable=self.idcarga, state="readonly")
        self.entryid.place(x=350,y=170+70)
        self.labelnombre = tk.Label(self.newWindow, text="Nombre: ", bg='light blue')
        self.labelnombre.place(x=500, y=140+70)
        self.labelnombre['font'] =self.fuente2
        self.nombrecarga = tk.StringVar()
        self.entrynombre = ttk.Entry(self.newWindow, textvariable=self.nombrecarga, state="readonly")
        self.entrynombre.place(x=500,y=170+70)
        self.labeldescri = tk.Label(self.newWindow, text="Descripción: ", bg='light blue')
        self.labeldescri.place(x=350,y=200+70)
        self.labeldescri['font'] =self.fuente2
        self.descricarga = tk.StringVar()
        self.entrydescri = ttk.Entry(self.newWindow, textvariable=self.descricarga, state="readonly", width=45)
        self.entrydescri.place(x=350,y=230+70)
        self.labelprecio = tk.Label(self.newWindow, text="Precio unitario: ", bg='light blue')
        self.labelprecio.place(x=350,y=260+70)
        self.labelprecio['font'] =self.fuente2
        self.preciocarga = tk.StringVar()
        self.entryprecio = ttk.Entry(self.newWindow, textvariable=self.preciocarga, state="readonly")
        self.entryprecio.place(x=350,y=290+70)
        self.stockcarga = tk.StringVar()
        self.labelstock = tk.Label(self.newWindow, text="Stock: ", bg='light blue')
        self.labelstock['font'] =self.fuente2
        self.labelstock.place(x=500,y=260+70)
        self.entrystock = ttk.Entry(self.newWindow, textvariable=self.stockcarga, state="readonly")
        self.entrystock.place(x=500,y=290+70)
        self.labelcantidad = tk.Label(self.newWindow, text="Cantidad solicitada: ", bg='white')
        self.labelcantidad['font'] =self.fuente2
        self.labelcantidad.place(x=350,y=320+70)
        self.cantidadcarga = tk.StringVar()
        self.entrycantidad = ttk.Entry(self.newWindow, textvariable=self.cantidadcarga, state="readonly")
        self.entrycantidad.place(x=350,y=350+70)
        self.labelmonto = tk.Label(self.newWindow, text="Monto total a pagar: ", bg='white')
        self.labelmonto['font'] =self.fuente2
        self.labelmonto.place(x=500,y=320+70)
        self.montocarga = tk.StringVar()
        self.entrymonto = ttk.Entry(self.newWindow, textvariable=self.montocarga, state="readonly")
        self.entrymonto.place(x=500,y=350+70)
        self.BotonAceptar = tk.Button(self.newWindow, text="CONFIRMAR", command=self.solicitar, height=2, width=15, )
        self.BotonAceptar['font'] =self.fuente1
        self.BotonAceptar.place(x=50, y=400)
        self.BotonQuit= tk.Button(self.newWindow, text="VOLVER", command=self.quitventanamed, height=2, width=15, )
        self.BotonQuit['font'] =self.fuente1
        self.BotonQuit.place(x=200,y=400)
        self.EscrituraSerial('C')

    def quitventanamed(self):
        self.newWindow.destroy()
        self.t1 = None
        self.t1 = threading.Thread(target=self.ventanamed)
        self.cap.release()
        self.newWindow.destroy()
        self.master.deiconify()

    def show_frame(self):
        _, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        #cv2image = cv2.cvtColor(frame,0)
        barcode = decode(cv2image)
        for obj in barcode:
            points = obj.polygon
            (x,y,w,h) = obj.rect
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            #cv2image=cv2.polylines(frame, [pts], True, (0, 255, 0), 3)

            barcodeData = obj.data.decode("utf-8")
            id = str(barcodeData).split(':')[0]
            medic = str(barcodeData).split(':')[1]
            cant = str(barcodeData).split(':')[2]
            #cant = str(barcodeData).split(':')[1]
            string = "Nombre " + medic + " | Cantidad " + cant
            #self.nombrecarga.set(str(respuesta[0][0]))
            #self.descricarga.set(str(respuesta[0][1]))
            self.cantidadcarga.set(cant)
            self.idcarga.set(id)
            self.escanear()
            #respuesta = self.pedido1.consulta(self.idcarga.get())
            cv2image=cv2.putText(cv2image, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,0,0), 1)
        #print("ID: "+id +" | Cantidad: "+cant)

        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.lmain.after(10, self.show_frame)

    def escanear(self):
        self.nombrecarga.set("")
        self.descricarga.set("")
        self.preciocarga.set("")
        self.stockcarga.set("")
        self.montocarga.set("")
        respuesta = self.pedido1.consulta(self.idcarga.get())
        print(respuesta)
        if len(respuesta) > 0:
            self.tkLabel2['text']="Los datos\n correspondientes\n al código QR son:"
            self.nombrecarga.set(str(respuesta[0][0]))
            self.descricarga.set(str(respuesta[0][1]))
            self.preciocarga.set(str(respuesta[0][2]))
            self.stockcarga.set(str(respuesta[0][3]))
            pago=int(respuesta[0][2])*int(self.cantidadcarga.get())
            self.montocarga.set(str(pago))
            if (int(respuesta[0][3])<int(self.cantidadcarga.get())):
                mb.showinfo("Informacion", "No se hay suficientes medicamentos requeridos")
                self.idcarga.set("")
                self.cantidadcarga.set("")
                self.nombrecarga.set("")
                self.descricarga.set("")
                self.preciocarga.set("")
                self.stockcarga.set("")
                self.montocarga.set("")
                self.tkLabel2['text'] = "Acerque el código QR \nde su receta a la \ncámara. Por favor"
        else:
            mb.showinfo("Informacion", "No se han encontrados los datos")
            self.idcarga.set("")
            self.cantidadcarga.set("")

    def solicitar(self):
        print("Estamos enviando C de Py 2 Ard")
        self.EscrituraSerial('C')
        self.BotonAceptar['state'] = tk.DISABLED
        self.BotonQuit['state'] = tk.DISABLED
        self.newWindow.update()
        datos = (self.cantidadcarga.get(), self.idcarga.get())
        respuesta = self.pedido1.consulta(datos[1])  # Verifica si existe el medicamento
        if int(respuesta[0][3])> 0: #Existe el producto
            if int(respuesta[0][3]) < int(datos[0]):
                mb.showinfo("Información", "No existe cantidad de medicamentos solicitados")
                self.cantidadcarga.set("")
            else:
                stockviejo= self.pedido1.consultastock(datos[1])
                stocknuevo= int(stockviejo[0][0])-int(datos[0])
                datos2= (str(stocknuevo), str(datos[1]))
                #print(datos2)
                self.pedido1.updatestock(datos2)
                #mb.showinfo("Información", "Su pedido se esta procesando, aguarde")
                self.tarea=0
                self.codigo=str(datos[0])+"M"+str(datos[1])
                #print(str(stocknuevo)+str(datos[1]))
                print(self.codigo)
                self.EscrituraSerial(self.codigo)
                try:
                    self.t2.start()
                    self.EscrituraSerial(self.codigo)
                except:
                    self.ventanaprocess()
                #self.t2.join()
                #self.t2 = None
                #self.t2 = threading.Thread(target=self.ventanaprocess)

    def ventanaprocess(self):
        print("Se esta intentando crear la ventana process")
        self.VentanaProceso = tk.Toplevel(self.master)
        self.estado = tk.StringVar()
        self.estado.set("PROCESANDO")
        self.tkLabel = ttk.Label(self.VentanaProceso, textvariable=self.estado)
        if (self.tarea==0):
            self.VentanaProceso.title("ESTADO DEL PEDIDO")
            self.estado.set("AGUARDE, YA ESTA PREPARÁNDOSE SU PEDIDO")
        elif (self.tarea==1):
            self.VentanaProceso.title("PROGRESO EN LA REPOSICION")
            self.estado.set("ROBOT EN MOVIMIENTO")
        self.tkLabel.pack()
        self.progressbar_r = ttk.Progressbar(self.VentanaProceso, length=400, value=0)
        self.progressbar_r.pack()
        self.progresobarra()
        #self.running= True
        #self.VentanaProceso.protocol("WM_DELETE_WINDOW", self.cerrando)

    def progresobarra(self):
        #self.EscrituraSerial('R')
        print("Se ingreso a la funcion de la barra")
        progress_l= ""
        progress_l= self.lectura
        print(progress_l)
        if (progress_l.isnumeric()):
            if (progress_l == '100'):
                self.progressbar_r["value"] = 99.9
                self.progressbar_r.pack()
                if (self.tarea==0):
                    self.estado.set("TERMINADO. RETIRE SU PEDIDO")
                    self.VentanaProceso.after(3000, self.cerrando)
                elif(self.tarea==1):
                    self.estado.set("NUEVA REPOSICIÓN GUARDADA")
                    self.newWindow2.after(3000, self.quitventanarep)   
            else:
                self.progressbar_r["value"] = progress_l
                self.progressbar_r.pack()
                self.VentanaProceso.after(100, self.progresobarra)
        else:
            self.VentanaProceso.after(100, self.progresobarra)        

    def ventanarepon(self):
        self.master.withdraw()
        self.newWindow2 = tk.Toplevel(self.master)
        self.newWindow2.title("VENTANA DE REPOSICIÓN")
        self.newWindow2.geometry("600x600")
        self.lmain2 = tk.Label(self.newWindow2, text="CÁMARA INICIALIZÁNDOSE, PODRÍA DEMORAR 15 SEGUNDOS. AGRADECEMOS SU PACIENCIA")
        self.lmain2.pack()
        self.idcargar = tk.StringVar()
        self.parameters = cv2.aruco.DetectorParameters_create()
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
        #Se carga el detector de objetos
        self.detector = HomogeneousBgDetector()
        try:
            self.cam = cv2.VideoCapture('http://192.168.43.1:8080/video')
        except:
            pass
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 20)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 15)
        self.CamReposicion()
        self.tkLabel2 = ttk.Label(self.newWindow2, text="Los datos correspondientes al código QR son:")
        self.tkLabel2.pack()
        self.labelid = ttk.Label(self.newWindow2, text="ID: ")
        self.labelid.pack()
        self.entryid = ttk.Entry(self.newWindow2, textvariable=self.idcargar, state="readonly")
        self.entryid.pack()
        self.labelnombre = ttk.Label(self.newWindow2, text="Nombre")
        self.labelnombre.pack()
        self.nombrecargar = tk.StringVar()
        self.entrynombre = ttk.Entry(self.newWindow2, textvariable=self.nombrecargar, state="readonly")
        self.entrynombre.pack()       
        self.stockcargar = tk.StringVar()
        self.labelstock = ttk.Label(self.newWindow2, text="Stock Disponible")
        self.labelstock.pack()
        self.entrystock= ttk.Entry(self.newWindow2, textvariable=self.stockcargar, state="readonly")
        self.entrystock.pack()
        self.BotonQuitr= tk.Button(self.newWindow2, text="Volver", command=self.quitventanarep, height=4, width=20, )
        self.BotonQuitr.pack(side='top', ipadx=10, padx=10, pady=15)
        try:
            self.t4 = threading.Thread(target=self.cargar)
            self.t4.daemon = True
        except:
            pass

    def quitventanarep(self):
         self.cam.release()
         self.VentanaProceso.destroy()
         self.newWindow2.destroy()
         self.t3 = None
         self.t3 = threading.Thread(target=self.ventanarepon)
         self.master.deiconify()
    
    def CamReposicion(self):
        _, frame = self.cam.read()
        corners, _, _ = cv2.aruco.detectMarkers(frame, self.aruco_dict, parameters= self.parameters)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        #cv2image = cv2.cvtColor(frame,0)
        barcode = decode(cv2image)
        #Para estimar el tamanho en cm
        if corners:
            #print(corners)
            #Se dibuja un poligono alrededor del marcador
            int_corners = np.int0(corners)
            #cv2.polylines(frame, int_corners, True, (0,255,0), 5)
            cv2.polylines(frame, int_corners, True, (0,255,0), 3)

            #Perimetro del marcador
            aruco_perimeter = cv2.arcLength(corners[0], True)
            #print(aruco_perimeter)

            #Ratio entre cm y pixeles
            #pixel_cm_ratio = aruco_perimeter / 20
            pixel_cm_ratio = aruco_perimeter / 12
            #print(pixel_cm_ratio)

            contours = self.detector.detect_objects(frame)

            for cnt in contours:
                #Dibuja un poligono
                #cv2.polylines(img, [cnt], True, (255,0,0), 2)

                #Dibuja un rectangulo
                rect = cv2.minAreaRect(cnt)
                (x, y), (w, h), angle = rect

                #Se transforma el tamanho de pixels a cm con el ratio
                ancho = w / pixel_cm_ratio
                largo = h / pixel_cm_ratio

                #Dibuja un punto en el centro del objeto
                #cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
                cv2.circle(frame, (int(x), int(y)), 3, (0, 0, 255), -1)
                #Crea un contorno para la figura con sus caracteristicas
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                #Dibuja el rectangulo alrededor del objeto
                cv2image=cv2.polylines(frame, [box], True, (255,0,0), 2)
                cv2image=cv2.putText(frame, "Ancho {} cm".format(round(ancho, 1)), (int(x-100), int(y-30)), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 200, 0), 2)
                cv2image=cv2.putText(frame, "Largo {} cm".format(round(largo, 1)), (int(x-100), int(y+70)), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 200, 0), 2)

        for obj in barcode:
            points = obj.polygon
            (x,y,w,h) = obj.rect
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            #cv2.polylines(frame, [pts], True, (0, 255, 0), 3)

            barcodeData = obj.data.decode("utf-8")
            id = str(barcodeData).split(':')[0]
            medic = str(barcodeData).split(':')[1]
            #cant = str(barcodeData).split(':')[2]
        #    cant = str(barcodeData).split(':')[1]
            self.idcargar.set(id)
        #    if self.t4.running     
            try:
                self.t4.start()#Actualizacion BD
                #self.t4.join()
            except:
                pass
        img = Image.fromarray(cv2image)
        img = img.resize((300, 300), Image.ANTIALIAS) 
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain2.imgtk = imgtk
        self.lmain2.configure(image=imgtk)
        self.lmain2.after(10, self.CamReposicion)

    def cargar(self):
        print("Estamos enviando R de Py 2 Ard")
        self.EscrituraSerial('R')
        respuesta = self.pedido1.consulta(self.idcargar.get())
        if (len(respuesta)>0):  # Verifica si existe el medicamento
            self.nombrecargar.set(str(respuesta[0][0]))
            self.stockcargar.set(str(respuesta[0][3]))
            self.BotonQuitr['state'] = tk.DISABLED
            self.newWindow2.update()
            datos = self.idcargar.get()
            stockviejo = str(respuesta[0][3])
            self.codigo=stockviejo+"M"+str(datos)
            print(self.codigo)
            self.tarea=1
            self.EscrituraSerial(self.codigo)
            print("waiting...")
            self.ventanaprocess()
            self.newWindow2.wait_window(self.VentanaProceso)
            print("Acabo espera")
            stocknuevo= int(stockviejo)+1
            datos2= (str(stocknuevo), str(datos))
            self.pedido1.updatestock(datos2)
            #self.BotonQuitr['state'] = tk.NORMAL
            self.idcargar.set("")
            self.nombrecargar.set("")
            self.stockcargar.set("")
        else:
            mb.showinfo("Información", "No se encuentra registrado el producto")
        self.t4 = None
        self.t4 = threading.Thread(target=self.cargar)
            
    def cerrando(self):      
        self.BotonQuit['state'] = tk.NORMAL
        self.idcarga.set("")
        self.nombrecarga.set("")
        self.stockcarga.set("")
        self.montocarga.set("")
        #if (self.tarea==0):
        self.BotonAceptar['state'] = tk.NORMAL
        self.tkLabel2['text']="Acerque el código QR \nde su receta a la \ncámara. Por favor"
        self.VentanaProceso.destroy()
        self.cantidadcarga.set("") 
        self.descricarga.set("")
        self.preciocarga.set("")
    
root = tk.Tk()
applicacion = FormularioFarmacia(root)
print("Inicializando sistema")
time.sleep(2)
print("Sistema inicializado")
root.mainloop()