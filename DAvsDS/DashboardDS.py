import pandas as pd
import panel as pn
import hvplot.pandas
import os
pn.extension()

df_pred=pd.read_csv(os.path.join('DataDS','pred.csv'))

grafica_pred=df_pred.hvplot.bar(x='KPI', y='valor', color='KPI', title='Prediccion KPIS proximo mes', ylabel='MXN', height=400)

pn.template.FastListTemplate(title='Dashboard Prediccion KPIS', main=['# Prediccion KPIS proximo mes', grafica_pred]).servable()

