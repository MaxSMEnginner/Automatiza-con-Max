"""
Imaginemos que estamos trabajando con datos de ventas, donde cada registro tiene información sobre el producto,
la cantidad vendida, y el precio. Usamos clases para estructurar los datos y realizar cálculos como el total de
ventas.
"""

class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

class Venta:
    def __init__(self, producto, cantidad ):
        self.producto = producto
        self.cantidad = cantidad

    def total_venta(self):
        return self.producto.precio * self.cantidad

p1=Producto('Mangos',15)
p2=Producto('Peras',150)

v1=Venta(p1,2)
v2=Venta(p2,3)

# print(f'Producto: {p1.nombre} total: {v1.total_venta()}')
# print(f'Producto: {p2.nombre} total: {v2.total_venta()}')


"""
Aquí utilizamos herencia y polimorfismo para extender una clase base Estadisticas a clases más específicas, 
como Promedio, Mediana y Moda.
"""
import numpy as np
from scipy import stats


class Estadistica:
    def __init__(self, data):
        self.data = data

    def calcular(self):
        pass
class Promedio(Estadistica):
    def calcular(self):
        return np.mean(self.data)

class Mediana(Estadistica):
    def calcular(self):
        return np.median(self.data)

class Moda(Estadistica):
    def calcular(self):
        return stats.mode(self.data)[0]
datos = [1, 2, 2, 3, 4, 5, 5, 5, 6]
mean=Promedio(datos)
median=Mediana(datos)
mode=Moda(datos)
#
# print(f'Promedio: {mean.calcular()}\nMediana: {median.calcular()}\nMode: {mode.calcular()}')
"""
A veces, en lugar de usar herencia, es mejor usar la composición para estructurar el código. Imagina que estás 
analizando datos de ventas y productos, y que cada venta tiene un Producto asociado.
"""
class Producto2:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

class Venta2:
    def __init__(self, producto, cantidad ):
        self.producto = producto
        self.cantidad = cantidad

    def total_venta(self):
        return self.producto.precio * self.cantidad


class Analisis:
    def __init__(self):
        self.ventas=[]

    def agregar_venta(self, venta):
        self.ventas.append(venta)

    def total_ventas(self):
        return sum(venta.total_venta() for venta in self.ventas)

    def promedio_venta(self):
        return self.total_ventas()/len(self.ventas) if self.ventas else 0

p3=Producto2('Laptop',1500)
p4=Producto2('Computadora',2000)
v3=Venta2(p3,4)
v4=Venta2(p4,3)

a=Analisis()
a.agregar_venta(v3)
a.agregar_venta(v4)


# print(f'Total de ventas fue: {a.total_ventas():,.2f}$\nVentas Promedio: {a.promedio_venta():,.2f}$')

"""
Puedes usar decoradores para extender la funcionalidad de funciones de análisis de datos de manera limpia.
"""
import time

def medir_tiempo(func):
    def medicion(*args, **kwargs):
        inicio=time.time()
        result=func(*args, **kwargs)
        fin=time.time()
        print(f'La funcion a tardado {fin - inicio} segundos.')
        return result
    return medicion


datos = [1, 2, 2, 3, 4, 5, 5, 5, 6]
@medir_tiempo
def calcular_promedio(data):
    return np.mean(data)

print(f'Promedio de data: {calcular_promedio(datos)}')