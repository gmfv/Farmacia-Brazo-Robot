import tkinter as tk
import serial
import time
import threading
from tkinter import ttk
from tkinter import messagebox as mb
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
import pedido

class FormularioFarmacia:
    def __init__(self, master):
        self.pedido1 = pedido.Pedido()
        self.master=master
        self.master.title("FARMACIA AUTOMATIZADA")
        self.t1 = threading.Thread(target=self.ventanamed)
        self.t2 = threading.Thread(target=self.ventanaprocess)
        self.t3 = threading.Thread(target=self.ventanarepon)
        self.t1.daemon = True
        self.t2.daemon = True
        self.t3.daemon = True
        self.button1state = tk.Button(self.master, text="CLIENTE", command=self.AbrirVentanaCliente, height=4,
                                       width=20, )
        self.button1state.pack(side='top', ipadx=50, padx=10, pady=15)
        self.button2state = tk.Button(self.master, text="REPOSICIÓN", command=self.AbrirVentanaReposicion, height=4,
                                       width=20, )
        
        self.button2state.pack(side='top', ipadx=50, padx=20, pady=15)
        self.button3state = tk.Button(self.master, text="SALIR", command=self.master.quit, height=4,
                                      width=20, )
        self.button3state.pack(side='top', ipadx=50, padx=20, pady=15)
        self.ser = serial.Serial('COM3', 115200, timeout=.1)
        self.LecturaSerial()
        #self.t4 = threading.Thread(target=self.LecturaSerial)
        #self.t4.start()
        #self.ser.write(bytes('I', 'UTF-8'))
        #master.mainloop()
    #def botonReposicion(self):
    #    if (self.lectura == 'R'):
    #        try:
    #            self.t3.start()
    #        except:
    #            pass
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
        self.master.after(100, self.LecturaSerial)

    def EscrituraSerial(self, x):
        self.ser.write(bytes(x, 'UTF-8'))

    def ventanamed(self):
        self.master.withdraw()
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title("SOLICITUD DE MEDICAMENTO")
        self.newWindow.geometry("600x700")
        width, height = 200, 150
        self.lmain = tk.Label(self.newWindow, text="CAMARA INICIALIZANDOSE, PODRIA DEMORAR 15 SEGUNDOS. AGRADECEMOS SU PACIENCIA")
        self.lmain.pack()
        self.framevid = tk.LabelFrame(self.newWindow)
        self.framevid.pack()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.show_frame()
        self.tkLabel2 = ttk.Label(self.newWindow, text="Los datos correspondientes al código QR son:")
        self.tkLabel2.pack()
        self.labelid = ttk.Label(self.newWindow, text="ID: ")
        self.labelid.pack()
        self.idcarga = tk.StringVar()
        self.entryid = ttk.Entry(self.newWindow, textvariable=self.idcarga, state="readonly")
        self.entryid.pack()
        self.labelnombre = ttk.Label(self.newWindow, text="Nombre")
        self.labelnombre.pack()
        self.nombrecarga = tk.StringVar()
        self.entrynombre = ttk.Entry(self.newWindow, textvariable=self.nombrecarga, state="readonly")
        self.entrynombre.pack()
        self.labeldescri = ttk.Label(self.newWindow, text="Descripcion")
        self.labeldescri.pack()
        self.descricarga = tk.StringVar()
        self.entrydescri = ttk.Entry(self.newWindow, textvariable=self.descricarga, state="readonly", width=40)
        self.entrydescri.pack()
        self.labelprecio = ttk.Label(self.newWindow, text="Precio")
        self.labelprecio.pack()
        self.preciocarga = tk.StringVar()
        self.entryprecio = ttk.Entry(self.newWindow, textvariable=self.preciocarga, state="readonly")
        self.entryprecio.pack()
        self.stockcarga = tk.StringVar()
        self.labelstock = ttk.Label(self.newWindow, text="Stock")
        self.labelstock.pack()
        self.entrystock = ttk.Entry(self.newWindow, textvariable=self.stockcarga, state="readonly")
        self.entrystock.pack()
        self.labelcantidad = ttk.Label(self.newWindow, text="Cantidad: ")
        self.labelcantidad.pack()
        self.cantidadcarga = tk.StringVar()
        self.entrycantidad = ttk.Entry(self.newWindow, textvariable=self.cantidadcarga, state="readonly")
        self.entrycantidad.pack()
        self.BotonAceptar = tk.Button(self.newWindow, text="Confirmar", command=self.solicitar, height=4, width=20, )
        self.BotonAceptar.pack(side='top', ipadx=10, padx=10, pady=15)
        self.BotonQuit= tk.Button(self.newWindow, text="Volver", command=self.quitventanamed, height=4, width=20, )
        self.BotonQuit.pack(side='top', ipadx=10, padx=10, pady=15)
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
            cv2.polylines(frame, [pts], True, (0, 255, 0), 3)

            barcodeData = obj.data.decode("utf-8")
            id = str(barcodeData).split(':')[0]
            cant = str(barcodeData).split(':')[1]
            #string = "ID " + id + " | Cantidad " + cant
            #self.nombrecarga.set(str(respuesta[0][0]))
            #self.descricarga.set(str(respuesta[0][1]))
            self.cantidadcarga.set(cant)
            self.idcarga.set(id)
            self.escanear()
            #respuesta = self.pedido1.consulta(self.idcarga.get())
            #cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
            print("ID: "+id +" | Cantidad: "+cant)

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
        respuesta = self.pedido1.consulta(self.idcarga.get())
        print(respuesta)
        if len(respuesta) > 0:
            self.nombrecarga.set(str(respuesta[0][0]))
            self.descricarga.set(str(respuesta[0][1]))
            self.preciocarga.set(str(respuesta[0][2]))
            self.stockcarga.set(str(respuesta[0][3]))
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
        print("Se ingreso a la funcion de la barra")
        progress_l= ""
        progress_l= self.lectura
        print(progress_l)
        if (progress_l.isnumeric()):
            if (progress_l == '100'):
                self.progressbar_r["value"] = 99.9
                self.progressbar_r.pack()
                #self.ser.write(bytes('I', 'UTF-8'))
                self.estado.set("TERMINADO")
                if (self.tarea==0):
                    self.VentanaProceso.after(2000, self.cerrando)
                elif(self.tarea==1):
                    self.VentanaProceso.after(2000, self.VentanaProceso.destroy())       
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
        self.lmain2 = tk.Label(self.newWindow2, text="CAMARA INICIALIZANDOSE, PODRIA DEMORAR 15 SEGUNDOS. AGRADECEMOS SU PACIENCIA")
        self.lmain2.pack()
        self.framevid = tk.LabelFrame(self.newWindow2)
        self.framevid.pack()
        try:
            self.cam = cv2.VideoCapture('http://192.168.100.136:8080/video')
        except:
            pass
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 20)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 15)
        self.CamReposicion()
        self.tkLabel2 = ttk.Label(self.newWindow2, text="Los datos correspondientes al código QR son:")
        self.tkLabel2.pack()
        self.labelid = ttk.Label(self.newWindow2, text="ID: ")
        self.labelid.pack()
        self.idcarga = tk.StringVar()
        self.entryid = ttk.Entry(self.newWindow2, textvariable=self.idcarga, state="readonly")
        self.entryid.pack()
        self.labelnombre = ttk.Label(self.newWindow2, text="Nombre")
        self.labelnombre.pack()
        self.nombrecarga = tk.StringVar()
        self.entrynombre = ttk.Entry(self.newWindow2, textvariable=self.nombrecarga, state="readonly")
        self.entrynombre.pack()       
        self.stockcarga = tk.StringVar()
        self.labelstock = ttk.Label(self.newWindow2, text="Stock Diponible")
        self.labelstock.pack()
        self.entrystock= ttk.Entry(self.newWindow2, textvariable=self.stockcarga, state="readonly")
        self.entrystock.pack()
        self.BotonQuit= tk.Button(self.newWindow2, text="Volver", command=self.quitventanarep, height=4, width=20, )
        self.BotonQuit.pack(side='top', ipadx=10, padx=10, pady=15)
        self.t4 = threading.Thread(target=self.cargar)
        self.t4.daemon = True

    def quitventanarep(self):
         self.cam.release()
         self.newWindow2.destroy()
         self.t3 = None
         self.t3 = threading.Thread(target=self.ventanarepon)
         self.master.deiconify()
    
    def CamReposicion(self):
        _, frame = self.cam.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        #cv2image = cv2.cvtColor(frame,0)
        barcode = decode(cv2image)
        for obj in barcode:
            points = obj.polygon
            (x,y,w,h) = obj.rect
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (0, 255, 0), 3)

            barcodeData = obj.data.decode("utf-8")
            id = str(barcodeData).split(':')[0]
            cant = str(barcodeData).split(':')[1]
            #string = "ID " + id + " | Cantidad " + cant
            self.idcarga.set(id)
            try:
                self.t4.start()#Actualizacion BD
            except:
                pass
                #self.tarea=1
                #self.ventanaprocess()

        img = Image.fromarray(cv2image)
        img = img.resize((300, 300), Image.ANTIALIAS) 
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain2.imgtk = imgtk
        self.lmain2.configure(image=imgtk)
        self.lmain2.after(10, self.CamReposicion)

    def cargar(self):
        self.EscrituraSerial('R')
        self.var = tk.IntVar()
        respuesta = self.pedido1.consulta(self.idcarga.get())
        if (len(respuesta)>0):  # Verifica si existe el medicamento
            self.nombrecarga.set(str(respuesta[0][0]))
            self.stockcarga.set(str(respuesta[0][3]))
            self.BotonQuit['state'] = tk.DISABLED
            self.newWindow2.update()
            datos = self.idcarga.get()
            stockviejo = str(respuesta[0][3])
            stocknuevo= int(stockviejo)+1
            datos2= (str(stocknuevo), str(datos))
            self.pedido1.updatestock(datos2)
            self.codigo=stockviejo+"M"+str(datos2[1])
            print(self.codigo)
            self.tarea=1
            self.EscrituraSerial(self.codigo)
            print("waiting...")
            self.ventanaprocess()
            self.newWindow2.wait_window(self.VentanaProceso)
            print("Acabo espera")
            self.BotonQuit['state'] = tk.NORMAL
            self.idcarga.set("")
            self.nombrecarga.set("")
            self.stockcarga.set("")
        else:
            mb.showinfo("Información", "No se encuentra registrado el producto")
        self.t4 = None
        self.t4 = threading.Thread(target=self.cargar)
            
    def cerrando(self):      
        self.BotonQuit['state'] = tk.NORMAL
        self.idcarga.set("")
        self.nombrecarga.set("")
        self.stockcarga.set("")
        #if (self.tarea==0):
        self.BotonAceptar['state'] = tk.NORMAL
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