import mysql.connector

class Pedido:

    def abrir(self):
        conexion=mysql.connector.connect(host="127.0.0.1",
                                              user="root", 
                                              password="",
                                              database="bd_farmacia",
                                              auth_plugin='mysql_native_password')
        return conexion

    def carga(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="UPDATE medicamentos set stock = stock+%s where id = %s"
        cursor.execute(sql, datos)
        cone.commit()
        cone.close()

    def consulta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select nombre, descripcion, precio, stock from medicamentos where id = %s" % datos
        cursor.execute(sql)
        registro=cursor.fetchall()
        cone.close()
        return registro
    
    def consultastock(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql1="select stock from medicamentos where id = %s" % datos
        cursor.execute(sql1)
        registro=cursor.fetchall()
        cone.close()
        return registro

    def updatestock(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        #print(datos)
        sql2="UPDATE medicamentos set stock = %s where id = %s" % datos
        cursor.execute(sql2)
        cone.commit()
        #print(sql2)
        cone.close()
