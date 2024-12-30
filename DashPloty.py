import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = px.data.gapminder()

app = dash.Dash(__name__)
app.title = "Dashboard Interactivo"

app.layout = html.Div([
    html.H1("Dashboard Dinámico con Plotly Dash", style={"text-align": "center"}),

    html.Div([
        html.Label("Selecciona un continente:"),
        dcc.Dropdown(
            id="dropdown-continent",
            options=[{"label": cont, "value": cont} for cont in df['continent'].unique()],
            value="Asia",
            style={"width": "30%"}
        )
    ], style={"padding": "10px"}),

    html.Div([
        html.Label("Selecciona un año:"),
        dcc.Slider(
            id="year-slider",
            min=df['year'].min(),
            max=df['year'].max(),
            step=5,
            marks={str(year): str(year) for year in df['year'].unique()},
            value=df['year'].min()
        )
    ], style={"padding": "20px"}),

    dcc.Graph(id="bar-chart"),


])

@app.callback(
    Output("bar-chart", "figure"),
    [Input("dropdown-continent", "value"),
     Input("year-slider", "value")]
)
def update_chart(selected_continent, selected_year):
    filtered_df = df[(df['continent'] == selected_continent) & (df['year'] == selected_year)]
    fig = px.bar(filtered_df, x="country", y="pop", color="country",
                 title=f"Población en {selected_continent} en {selected_year}",
                 labels={"pop": "Población",
                         "country": "Paises"})
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
