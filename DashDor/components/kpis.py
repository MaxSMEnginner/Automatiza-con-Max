# components/kpis.py
from dash import html
import dash_bootstrap_components as dbc
from logic import obtener_movimientos
import pandas as pd

def calcular_kpis():
    movimientos = obtener_movimientos(usuario_id=1)
    if not movimientos:
        return {}

    df = pd.DataFrame([{
        "tipo": m.tipo,
        "monto": m.monto,
        "fecha": m.fecha,
        "plazo": m.plazo
    } for m in movimientos if m.monto and m.fecha])


    ingresos = df[df['tipo'] == 'ingreso']
    egresos = df[df['tipo'] == 'egreso']

    ingreso_total = ingresos['monto'].sum()
    egreso_total = egresos['monto'].sum()
    balance = ingreso_total - egreso_total

    ingreso_semanal = ingresos[ingresos['plazo'] =='Semanal']['monto'].sum()
    ingreso_quincenal = ingresos[ingresos['plazo'] =='Quincenal']['monto'].sum()
    ingreso_mensual = ingresos[ingresos['plazo'] =='Mensual']['monto'].sum()

    # Análisis de deuda: ¿cuánto tiempo se tarda en cubrir los egresos al ritmo de ingreso mensual?
    if ingreso_mensual > 0:
        meses_para_liberarse = egreso_total / ingreso_mensual
        tiempo_libre_deuda = f"{meses_para_liberarse:.1f} meses para cubrir egresos"
    else:
        tiempo_libre_deuda = "Sin ingresos mensuales registrados"

    situacion = "✅ Ingresos superan egresos" if balance >= 0 else "⚠️ Egresos superan ingresos"

    return {
        "Ingreso Total": ingreso_total,
        "Ingreso Semanal": ingreso_semanal,
        "Ingreso Quincenal": ingreso_quincenal,
        "Ingreso Mensual": ingreso_mensual,
        "Egreso Total": egreso_total,
        "Balance": balance,
        "Situación Actual": situacion,
        "Tiempo para Cubrir Egresos": tiempo_libre_deuda
    }

def render_kpis():
    kpis = calcular_kpis()
    if not kpis:
        return html.Div("No hay datos suficientes para KPIs.", className="text-warning")

    cards = []
    for key, value in kpis.items():
        card = dbc.Col(
            dbc.Card([
                dbc.CardHeader(key, className="text-center", style={"fontSize": "0.85rem"}),
                dbc.CardBody(
                    html.H5(f"${value:,.2f}" if isinstance(value, (int, float)) else value,
                            className="text-center", style={"fontSize": "1rem"})
                )
            ], className="shadow-sm", color="dark", inverse=True),
            md=3, sm=6, xs=12
        )
        cards.append(card)

    return dbc.Row(cards, className="mb-4")