# Estructura base del proyecto: ingresos-egresos-dashboard

# 1. app.py
from dash import Dash, Input, Output, State, html, dcc, ctx
import dash_bootstrap_components as dbc
from components.layout import create_layout
from db import get_session, engine
from models import Movimiento, Base
from logic import agregar_movimiento, obtener_movimientos
from components.charts import render_grafico
import os

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)
app.title = "Dashboard de Ingresos y Egresos"

# Crear las tablas si no existen (solo la primera vez)
if not os.path.exists(".db_initialized"):
    Base.metadata.create_all(engine)
    with open(".db_initialized", "w") as f:
        f.write("initialized")

# ---------- Función de tabla paginada ----------
def render_tabla(page_size=10):
    movimientos = obtener_movimientos(usuario_id=1)
    if not movimientos:
        return html.Div("No hay movimientos registrados aún. Agrega tus ingresos y egresos para ver el análisis.", className="text-warning")

    import pandas as pd
    from dash import dash_table


    data = [{
        "ID": m.id,
        "Tipo": m.tipo,
        "Categoría": m.categoria,
        "Monto": f"${m.monto:,.2f}",
        "Descripción": m.descripcion,
        "Plazo": m.plazo,
        "Método": m.metodo,
        "Fecha": str(m.fecha)
    } for m in movimientos]

    df = pd.DataFrame(data)

    return html.Div([
        html.Label("Elementos por página:"),
        dcc.Dropdown(
            id="page-size-dropdown",
            options=[
                {"label": str(i), "value": i} for i in [5, 10, 100, 1000]
            ],
            value=page_size,
            clearable=False,
            style={"width": "100px"}
        ),
        dash_table.DataTable(
            id="tabla-dinamica",
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict("records"),
            page_size=page_size,
            page_current=0,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left"},
            style_header={"backgroundColor": "#343a40", "color": "white"},
            style_data={"backgroundColor": "#212529", "color": "white"},
        )
    ])

# Layout con tabla y gráfica ya precargadas
app.layout = create_layout(
    tabla_inicial=lambda: render_tabla(),
    grafico_inicial=lambda: render_grafico()
)

@app.callback(
    Output("result", "children"),
    Output("tabla-movimientos", "children"),
    Output("grafico-movimientos", "figure"),
    Input("guardar", "n_clicks"),
    State("tipo", "value"),
    State("categoria", "value"),
    State("monto", "value"),
    State("descripcion", "value"),
    State("plazo", "value"),
    State("metodo", "value"),
    prevent_initial_call=True
)
def guardar_datos(n_clicks, tipo, categoria, monto, descripcion, plazo, metodo):
    if not all([tipo, categoria, monto, descripcion, plazo, metodo]):
        return "Completa todos los campos", render_tabla(), render_grafico()

    data = {
        "tipo": tipo,
        "categoria": categoria,
        "monto": monto,
        "descripcion": descripcion,
        "plazo": plazo,
        "metodo": metodo,
        "usuario_id": 1
    }

    try:
        agregar_movimiento(data)
        return "✅ Éxito", render_tabla(), render_grafico()
    except Exception as e:
        print("Error al guardar:", e)
        return "❌ Error", render_tabla(), render_grafico()

# Callback para cambiar el tamaño de página
@app.callback(
    Output("tabla-dinamica", "page_size"),
    Input("page-size-dropdown", "value")
)
def actualizar_page_size(value):
    return value

if __name__ == "__main__":
    app.run(debug=True)
