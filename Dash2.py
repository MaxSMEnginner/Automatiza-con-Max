import os
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Cargar datos
df = pd.read_csv(os.path.join('..','DataFrames','Prueba','Product_v6.csv'))

# Crear la aplicación
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
app.title = "Product V6 Data"


# Función para calcular KPIs
def calcular_kpis(df):
    total_productos = df['category.code'].nunique()
    total_valor = df['value'].sum()
    promedio_valor = df['value'].mean()
    productos_activos = df[df['status'] == 'ACTIVE']['category.code'].nunique()
    productos_inactivos = df[df['status'] == 'INACTIVE']['category.code'].nunique()
    categoria_popular = df['category.code'].value_counts().idxmax()
    return total_productos, total_valor, promedio_valor, productos_activos, productos_inactivos, categoria_popular


# Layout del dashboard
app.layout = dbc.Container([
    # Título
    html.H1("Products Kpi's and Data", className="text-center my-4"),

    # KPIs
    dbc.Row([
        dbc.Col(dbc.Card([
            html.H5("Total de Productos", className="text-center"),
            html.H2(id="kpi-total-productos", className="text-center")
        ], body=True, color="primary", inverse=True), width=2),
        dbc.Col(dbc.Card([
            html.H5("Valor Total (USD)", className="text-center"),
            html.H2(id="kpi-total-valor", className="text-center")
        ], body=True, color="info", inverse=True), width=2),
        dbc.Col(dbc.Card([
            html.H5("Promedio de Valor", className="text-center"),
            html.H2(id="kpi-promedio-valor", className="text-center")
        ], body=True, color="success", inverse=True), width=2),
        dbc.Col(dbc.Card([
            html.H5("Productos Activos", className="text-center"),
            html.H2(id="kpi-productos-activos", className="text-center")
        ], body=True, color="warning", inverse=True), width=2),
        dbc.Col(dbc.Card([
            html.H5("Productos Inactivos", className="text-center"),
            html.H2(id="kpi-productos-inactivos", className="text-center")
        ], body=True, color="danger", inverse=True), width=2),
        dbc.Col(dbc.Card([
            html.H5("Categoría Más Popular", className="text-center"),
            html.H2(id="kpi-categoria-popular", className="text-center")
        ], body=True, color="dark", inverse=True), width=2),
    ], className="mb-4"),

    # Filtros y Gráficos
    dbc.Row([
        # Filtros
        dbc.Col([
            html.H5("Data Filtrate", className="mb-4"),
            dcc.Dropdown(
                id='product-type',
                options=[{'label': t, 'value': t} for t in df['productType'].unique()],
                placeholder="Selecciona un tipo de dato",
                className="mb-3"
            ),
            dcc.Checklist(
                id='status-checklist',
                options=[{'label': s, 'value': s} for s in df['status'].unique()],
                inline=True,
                className="mb-3"
            ),
            dcc.RangeSlider(
                id='value-slider',
                min=df['value'].min(),
                max=df['value'].max(),
                step=10,
                marks={i: f"${i}" for i in range(int(df['value'].min()), int(df['value'].max()), 1000)},
                value=[df['value'].min(), df['value'].max()],
                className="mt-3"
            )
        ], width=3),

        # Gráficos
        dbc.Col([
            dcc.Graph(id='bar-chart'),
            dcc.Graph(id='donut-chart')
        ], width=9)
    ])
], fluid=True)


# Callbacks
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('donut-chart', 'figure'),
     Output('kpi-total-productos', 'children'),
     Output('kpi-total-valor', 'children'),
     Output('kpi-promedio-valor', 'children'),
     Output('kpi-productos-activos', 'children'),
     Output('kpi-productos-inactivos', 'children'),
     Output('kpi-categoria-popular', 'children')],
    [Input('product-type', 'value'),
     Input('status-checklist', 'value'),
     Input('value-slider', 'value')]
)
def update_dashboard(product_type, status, value_range):
    filtered_df = df[
        (df['value'] >= value_range[0]) &
        (df['value'] <= value_range[1])
        ]
    if product_type:
        filtered_df = filtered_df[filtered_df['productType'] == product_type]
    if status:
        filtered_df = filtered_df[filtered_df['status'].isin(status)]

    # Gráfico de barras
    bar_fig = px.bar(filtered_df, x='category.code', y='value', color='status',
                     title="Distribución de Categorías por Valor",
                     labels={'value': 'Valor (USD)', 'category.code': 'Categoría'},
                     template="plotly_dark")

    # Gráfico de dona
    donut_fig = px.pie(filtered_df, names='status', values='value', hole=0.5,
                       title="Proporción de Productos por Estado",
                       color_discrete_sequence=px.colors.sequential.RdBu
                       )

    # KPIs
    total_productos, total_valor, promedio_valor, productos_activos, productos_inactivos, categoria_popular = calcular_kpis(
        filtered_df)

    return (bar_fig, donut_fig,
            total_productos, f"${total_valor:,.2f}",
            f"${promedio_valor:,.2f}", productos_activos,
            productos_inactivos, categoria_popular)


# Ejecutar el servidor
if __name__ == '__main__':
    app.run_server(debug=True)
