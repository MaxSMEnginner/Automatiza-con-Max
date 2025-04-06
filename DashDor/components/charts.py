import plotly.express as px
import pandas as pd
from logic import obtener_movimientos

def grafico_placeholder():
    return {
        "data": [],
        "layout": {"title": "Gráfico vacío", "template": "plotly_dark"}
    }

def render_grafico():
    movimientos = obtener_movimientos(usuario_id=1)
    if not movimientos:
        return grafico_placeholder()

    data = [{
        "tipo": m.tipo,
        "monto": m.monto,
        "fecha": m.fecha,
        "categoria": m.categoria
    } for m in movimientos if m.monto is not None]

    df = pd.DataFrame(data)

    if df.empty:
        return {
            "data": [],
            "layout": {"title": "Sin datos para mostrar", "template": "plotly_dark"}
        }

    df_grouped = df.groupby(["tipo", "categoria"], as_index=False).sum(numeric_only=True)

    fig = px.bar(
        df_grouped,
        x="categoria",
        y="monto",
        color="tipo",
        title="Ingresos vs Egresos por Categoría",
        barmode="group",
        template="plotly_dark"
    )
    return fig