import pandas as pd
import panel as pn
import hvplot.pandas as hvplot
import os
from bokeh.models import NumeralTickFormatter

pn.extension()

df_kpis= pd.read_csv(os.path.join('DataDA','analisis_kpis_mensuales.csv'))

linea_kpis= df_kpis.hvplot.line(x='Mes',y=['IngresoTotal','MargenTotal'],title="KPI's Historicos - DA", ylabel='MXN', grid=True).opts(
    xrotation=45,
    yformatter=NumeralTickFormatter(format="0a")
)

    

tabla= pn.widgets.DataFrame(df_kpis,width=800,height=300)

pn.template.FastListTemplate(title="Analisis de Datos KPI'S-Fordh",
                             main=['# Analisis de Desempeño Mensual',
                                   linea_kpis,
                                   "## KPI's Detallados",
                                   tabla]
                             ).servable()


