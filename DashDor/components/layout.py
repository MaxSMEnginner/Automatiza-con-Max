from dash import html, dcc
import dash_bootstrap_components as dbc


def create_layout(tabla_inicial, grafico_inicial, kpis_inicial):
    return dbc.Container([
        html.H1("I/O Administrador", className="my-4 text-center"),

        # KPIs
        html.Div(id="kpi-container", children=kpis_inicial()),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Nuevo Movimiento"),
                    dbc.CardBody([
                        dbc.RadioItems(
                            id="tipo",
                            options=[{"label": "Ingreso", "value": "ingreso"}, {"label": "Egreso", "value": "egreso"}],
                            value="ingreso",
                            inline=True
                        ),
                        dbc.Input(id="categoria", placeholder="Categoría", className="my-2"),
                        dbc.Input(id="monto", placeholder="Monto", type="number", className="my-2"),
                        dbc.Input(id="descripcion", placeholder="Descripción", className="my-2"),
                        dbc.RadioItems(
                            id="plazo",
                            options=[{"label": "Semanal", "value": "Semanal"}, {"label": "Quincenal", "value": "Quincenal"}, {"label": "Mensual", "value": "Mensual"}],
                            value="Semanal",
                            inline=True
                        ),
                        dbc.Input(id="metodo", placeholder="Método (ej. Tarjeta Santander)", className="my-2"),
                        dbc.Button("Guardar", id="guardar", color="primary", className="mt-2"),
                        html.H6(children="", id="result", className="my-2")
                    ])
                ])
            ], width=6),

            dbc.Col([
                dcc.Graph(id="grafico-movimientos", figure=grafico_inicial())
            ], width=6)
        ]),

        dbc.Row([
            dbc.Col([
                html.Div(id="tabla-movimientos", className="mt-4", children=tabla_inicial())
            ], width=12)
        ])
    ], fluid=True)