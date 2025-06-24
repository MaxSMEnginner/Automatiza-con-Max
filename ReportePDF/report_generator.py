import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

df= pd.read_csv(os.path.join('..','Analisis_PT.csv'))

#KPIS
total_ingreso=df['Ingreso'].sum()
total_cantidad=df['Cantidad'].sum()
margen_prom=df['Margen'].mean()

summary={
    'Total Ingreso:': f'$ {total_ingreso:,.2f}',
    'Total Cantidad:': f'{total_cantidad:,.2f} QTY',
    'Margen Promedio:': f'$ {margen_prom:,.2f}'
}


comentarios = {
    "Resumen de Actividad": (
        "Este resumen muestra tres métricas clave para evaluar el desempeño global de la empresa en los últimos meses:\n"
        "- El Total de Ingreso refleja la suma total de todas las ventas registradas.\n"
        "- El Total de Productos Vendidos representa la cantidad total de unidades que se han comercializado.\n"
        "- El Margen Promedio indica cuánto se gana, en promedio, por cada producto vendido, después de costos."
    ),
    "Top 5 Productos más Vendidos": (
        "En este gráfico se identifican los cinco productos con mayor volumen de ventas. "
        "Esta información es útil para entender cuáles son los productos más populares y enfocar estrategias de marketing, stock e inversión en ellos."
    ),
    "Ventas Mensuales": (
        "Aquí se visualiza cómo se ha comportado el ingreso mensual a lo largo del tiempo. "
        "Este análisis permite identificar picos de demanda, estacionalidades o tendencias positivas/negativas que pueden influir en la toma de decisiones."
    ),
    "Margen Promedio por Categoría": (
        "Este gráfico compara la rentabilidad media por categoría de producto. "
        "Nos ayuda a ver qué líneas de productos generan mayor beneficio y cuáles podrían necesitar revisión de costos, precios o estrategias comerciales."
    ),
    "Stock Promedio por Tienda": (
        "Aquí se muestra la cantidad promedio de inventario disponible por tienda. "
        "Es útil para detectar tiendas con sobrestock o quiebre de inventario, lo cual puede impactar tanto en costos como en ventas."
    )
}

def generar_grafico(datos,tipo,filename,**kwargs):
    plt.figure(figsize=(6,4))
    if tipo == 'bar':
        datos.plot(kind='bar',**kwargs)
    elif tipo == 'line':
        datos.plot(kind='line', **kwargs)
    elif tipo == 'barh':
        datos.plot(kind='barh', **kwargs)

    plt.title(kwargs.get("title",""))
    plt.tight_layout()
    plt.savefig(filename,dpi=300)
    plt.close()


top_productos=df.groupby("NombreProducto")['Cantidad'].sum().sort_values(ascending=False).head(5)
ventas_mensuales=df.groupby('Mes_Nombre')['Ingreso'].sum().sort_index()
margen_categoria=df.groupby('Categoría')['Margen'].mean().sort_index()
stock_tienda=df.groupby('NombreTienda')['StockActual'].mean().sort_values()

generar_grafico(top_productos,'bar', 'top_productos.png',color='orange', title='Top 5 Productos mas Vendidos')
generar_grafico(ventas_mensuales,'line', 'ventas_mensuales.png',color='navy', title='Ventas Mensuales')
generar_grafico(margen_categoria,'barh', 'margen_categoria.png',color='darkorange', title='Margen x Categoria')
generar_grafico(stock_tienda,'bar', 'stock_tienda.png',color='steelblue', title='Stock x Tienda')


class PDFConFondo(FPDF):
    def __init__(self, fondo):
        super().__init__()
        self.fondo = fondo

    def header(self):
        self.image(self.fondo, x = 0, y= 0, w=self.w, h=self.h)
        self.set_y(40)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial','I',8)
        self.cell(0,10,f"Pagina {self.page_no()}", align="C")

def agregar_seccion(pdf,titulo, imagen_path, comentario, w_rel=0.5):
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0,10,titulo, ln=True)
    pdf.image(imagen_path, x=pdf.l_margin, w=pdf.w * w_rel)
    pdf.ln(5)
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(0, 6, comentario)
    pdf.ln(5)

#Crear PDF

pdf = PDFConFondo(fondo='Fondo.png')
pdf.set_auto_page_break(auto=True, margin=40)
pdf.set_margins(40,40,40)


#Pagina 1 Titulo KPIS, y 1 grafico
pdf.add_page()
pdf.set_font('Arial', "B", 16)
pdf.cell(0, 10, 'Reporte de Estadisticas -- EmpresaFake', ln =True)
pdf.ln(5)

pdf.set_font("Arial", "B", 14)
pdf.cell(0,10, "Resumen de Actividad", ln=True)
pdf.set_font("Arial", "", 12)
for k,v in summary.items():
    pdf.cell(0,8,f'{k} {v}',ln=True)

pdf.ln(3)
pdf.set_font('Arial','I', 10)
pdf.multi_cell(0,6,comentarios['Resumen de Actividad'])
pdf.ln(8)
agregar_seccion(pdf, "Top 5 Productos mas Vendidos","top_productos.png", comentarios["Top 5 Productos más Vendidos"],)
agregar_seccion(pdf, "Ventas Mensuales","ventas_mensuales.png", comentarios["Ventas Mensuales"],)
agregar_seccion(pdf, "Margen Promedio por Categoría","margen_categoria.png", comentarios["Margen Promedio por Categoría"],)
agregar_seccion(pdf, "Stock Promedio por Tienda","stock_tienda.png", comentarios["Stock Promedio por Tienda"])

pdf.output('Reporte_Fake.pdf')



