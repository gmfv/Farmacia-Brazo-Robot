import tkinter as tk
import serial
import time
import threading
from tkinter import ttk
from tkinter import messagebox as mb

import pedido

class FormularioFarmacia:
    def __init__(self, master):
        self.pedido1 = pedido.Pedido()
        #self.ser = serial.Serial('COM3', 115200, timeout=.1)
        self.master=master
        self.master.title("FARMACIA AUTOMATIZADA")
        self.button1state = tk.Button(self.master, text="CLIENTE", command=self.ventanamed, height=4,
                                       width=20, )
        self.button1state.pack(side='top', ipadx=50, padx=10, pady=15)
        # self.button2 = tk.IntVar()
        self.button2state = tk.Button(self.master, text="REPOSICIÓN", command=self.ventanarepon, height=4,
                                       width=20, )
        self.button2state.pack(side='top', ipadx=50, padx=20, pady=15)
        self.button3state = tk.Button(self.master, text="SALIR", command=self.master.quit, height=4,
                                      width=20, )
        self.button3state.pack(side='top', ipadx=50, padx=20, pady=15)
        self.t2 = threading.Thread(target=self.ventanaprocess)
        self.t2.daemon = True
        self.ser = serial.Serial('COM3', 115200, timeout=.1)
        self.ser.write(bytes('I', 'UTF-8'))
        #master.mainloop()

    def ventanamed(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title("SOLICITUD DE MEDICAMENTO")
        self.newWindow.geometry("600x600")
        self.Boton2 = tk.Button(self.newWindow, text="Escanear", command=self.escanear, height=4, width=20, )
        self.Boton2.pack(side='top', ipadx=10, padx=10, pady=15)
        self.tkLabel2 = ttk.Label(self.newWindow, text="Los datos correspondientes al código QR son:")
        self.tkLabel2.pack()
        self.labelid = ttk.Label(self.newWindow, text="ID: ")
        self.labelid.pack()
        self.idcarga = tk.StringVar()
        self.entryid = ttk.Entry(self.newWindow, textvariable=self.idcarga)
        self.entryid.pack()
        self.labelnombre = ttk.Label(self.newWindow, text="Nombre")
        self.labelnombre.pack()
        self.nombrecarga = tk.StringVar()
        self.entrynombre = ttk.Entry(self.newWindow, textvariable=self.nombrecarga, state="readonly")
        self.entrynombre.pack()
        self.labeldescri = ttk.Label(self.newWindow, text="Descripcion")
        self.labeldescri.pack()
        self.descricarga = tk.StringVar()
        self.entrydescri = ttk.Entry(self.newWindow, textvariable=self.descricarga, state="readonly")
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
        self.entrycantidad = ttk.Entry(self.newWindow, textvariable=self.cantidadcarga)
        self.entrycantidad.pack()
        self.BotonAceptar = tk.Button(self.newWindow, text="Confirmar", command=self.solicitar, height=4, width=20, )
        self.BotonAceptar.pack(side='top', ipadx=10, padx=10, pady=15)
        self.BotonQuit= tk.Button(self.newWindow, text="Volver", command=self.newWindow.destroy, height=4, width=20, )
        self.BotonQuit.pack(side='top', ipadx=10, padx=10, pady=15)
        #self.newWindow.update()

    def escanear(self):
        self.entrynombre.configure(state='normal')
        self.entrydescri.configure(state='normal')
        self.entryprecio.configure(state='normal')
        self.entrystock.configure(state='normal')
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
            self.entrynombre.configure(state='readonly')
            self.entrydescri.configure(state='readonly')
            self.entryprecio.configure(state='readonly')
            self.entrystock.configure(state='readonly')
        else:
            mb.showinfo("Informacion", "No se han encontrados los datos")

    def solicitar(self):
        self.entryid.configure(state='readonly')
        self.entrycantidad.configure(state='readonly')
        self.Boton2['state'] = tk.DISABLED
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
                self.ventanaprocess(self.tarea)
    
    def ventanarepon(self):
        self.newWindow2 = tk.Toplevel(self.master)
        self.newWindow2.title("VENTANA DE REPOSICIÓN")
        self.newWindow2.geometry("600x600")
        self.Boton2 = tk.Button(self.newWindow2, text="Escanear", command=self.escanear_re, height=4, width=20, )
        self.Boton2.pack(side='top', ipadx=10, padx=10, pady=15)
        self.tkLabel2 = ttk.Label(self.newWindow2, text="Los datos correspondientes al código QR son:")
        self.tkLabel2.pack()
        self.labelid = ttk.Label(self.newWindow2, text="ID: ")
        self.labelid.pack()
        self.idcarga = tk.StringVar()
        self.entryid = ttk.Entry(self.newWindow2, textvariable=self.idcarga)
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
        self.labelcantidad = ttk.Label(self.newWindow2, text="Cantidad a reponer: ")
        self.labelcantidad.pack()
        self.cantidadcarga = tk.StringVar()
        self.entrycantidad = ttk.Entry(self.newWindow2, textvariable=self.cantidadcarga)
        self.entrycantidad.pack()
        self.BotonAceptar = tk.Button(self.newWindow2, text="Cargar", command=self.cargar, height=4, width=20, )
        self.BotonAceptar.pack(side='top', padx=10, pady=15)
        self.BotonQuit= tk.Button(self.newWindow2, text="Volver", command=self.newWindow2.destroy, height=4, width=20, )
        self.BotonQuit.pack(side='top', ipadx=10, padx=10, pady=15)
    
    def escanear_re(self):
        self.entrynombre.configure(state='normal')
        self.entrystock.configure(state='normal')
        self.nombrecarga.set("")
        self.stockcarga.set("")
        respuesta = self.pedido1.consulta(self.idcarga.get())
        print(respuesta)
        if len(respuesta) > 0:
            self.nombrecarga.set(str(respuesta[0][0]))
            self.stockcarga.set(str(respuesta[0][3]))
            self.entrynombre.configure(state='readonly')
            self.entrystock.configure(state='readonly')
        else:
            mb.showinfo("Información", "No se han encontrados los datos")

    def cargar(self):
        self.Boton2['state'] = tk.DISABLED
        self.BotonAceptar['state'] = tk.DISABLED
        self.BotonQuit['state'] = tk.DISABLED
        self.newWindow2.update()
        datos = (self.cantidadcarga.get(), self.idcarga.get())
        stockviejo = self.pedido1.consultastock(datos[1]) # Verifica si existe el medicamento
        if int(stockviejo[0][0])> 0: #Existe el producto
            stocknuevo= int(stockviejo[0][0])+int(datos[0])
            datos2= (str(stocknuevo), str(datos[1]))
            #print(datos2)
            self.pedido1.updatestock(datos2)
            #mb.showinfo("PRECAUCIÓN", "Proceso en ejecución")  
            print("Inicia espera")
            self.tarea=1
            self.ventanaprocess(self.tarea)
        else:
            mb.showinfo("Información", "No se encuentra registrado el producto")

    def ventanaprocess(self, repon):
        self.t2.start()
        self.t2.join()
        self.VentanaProceso = tk.Toplevel(self.master)
        self.VentanaProceso.title("ESTADO DEL PEDIDO")
        self.estado = tk.StringVar()
        self.estado.set("PROCESANDO")
        self.tkLabel = ttk.Label(self.VentanaProceso, textvariable=self.estado)
        self.estado.set("AGUARDE, YA ESTA PREPARÁNDOSE SU PEDIDO")
        self.tkLabel.pack()
        self.progressbar_r = ttk.Progressbar(self.VentanaProceso, length=400, value=0)
        self.progressbar_r.pack()
        if (repon==1):
            self.ser.write(bytes('R', 'UTF-8'))
        elif (repon==0):
            self.ser.write(bytes('C', 'UTF-8'))
        self.progresobarra()
        #self.running= True
        #self.VentanaProceso.protocol("WM_DELETE_WINDOW", self.cerrando)

    def progresobarra(self):
        print("Se ingreso a la funcion de la barra")
        progress_l= ""
        progress_l= self.ser.readline().strip()
        print(progress_l)
        if (progress_l == b'A'):
             self.progressbar_r["value"] = 20
             self.progressbar_r.pack()
             self.VentanaProceso.after(1000, self.progresobarra)
        elif (progress_l == b'B'):
             self.progressbar_r["value"] = 40
             self.VentanaProceso.after(1000, self.progresobarra)
             self.progressbar_r.pack()
        elif (progress_l == b'C'):
             self.progressbar_r["value"] = 60
             self.VentanaProceso.after(1000, self.progresobarra)
             self.progressbar_r.pack()
        elif (progress_l == b'D'):
             self.progressbar_r["value"] = 80
             self.VentanaProceso.after(1000, self.progresobarra)
             self.progressbar_r.pack()
        elif (progress_l == b'E'):
             self.progressbar_r["value"] = 99.9
             self.progressbar_r.pack()
             self.ser.write(bytes('I', 'UTF-8'))
             self.estado.set("TERMINADO")
             self.VentanaProceso.after(1000, self.cerrando)
        else:
            self.VentanaProceso.after(1000, self.progresobarra)

    def cerrando(self):
        self.VentanaProceso.destroy()
        self.t2 = None
        self.t2 = threading.Thread(target=self.ventanaprocess)
        self.Boton2['state'] = tk.NORMAL
        self.BotonAceptar['state'] = tk.NORMAL
        self.BotonQuit['state'] = tk.NORMAL
        self.entryid.configure(state='normal')
        self.entrycantidad.configure(state='normal')
        self.idcarga.set("")
        self.nombrecarga.set("")
        self.stockcarga.set("")
        self.cantidadcarga.set("") 
        if (self.tarea==0):
            self.descricarga.set("")
            self.preciocarga.set("")

    
root = tk.Tk()
applicacion = FormularioFarmacia(root)
print("Inicializando sistema")
time.sleep(2)
print("Sistema inicializado")
root.mainloop()