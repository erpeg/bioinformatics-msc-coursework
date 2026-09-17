import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

fig = go.Figure()

df = pd.read_csv('data/datasets/COVID_19/nacional_covid19.csv')

df.columns = ['Time', 'Total confirmed cases', 'Cases confirmed by PCR', 'Cases confirmed by Antibody test',
              'Recovered', 'Deceased', 'Cases that required admission to the ICU', 'Cases that required hospitalization']
df = df.drop([91], axis=0)

things_to_plot = ['Cases confirmed by PCR', 'Cases confirmed by Antibody test']

for element in things_to_plot:
    fig.add_trace(go.Scatter(x=df['Time'], y=df[element], fill='tozeroy', name=element))

fig.update_layout(spikedistance=1000, hoverdistance=100)
fig.update_yaxes(showspikes=True, spikecolor="black", spikesnap="cursor", spikemode="across")

fig.update_layout(title='Share of testing methods in Spain',
                  xaxis_title='Time',
                  yaxis_title='Number of confirmed cases',
                  title_x=0.5,
                  xaxis=dict(
                      rangeselector=dict(buttons=list([
                          dict(count=7,
                               label="1w",
                               step="day",
                               stepmode="backward"),
                          dict(count=14,
                               label="2w",
                               step="day",
                               stepmode="backward"),
                          dict(count=1,
                               label="1m",
                               step="month",
                               stepmode="backward"),
                          dict(count=2,
                               label="2m",
                               step="month",
                               stepmode="backward"),
                          dict(count=3,
                               label="3m",
                               step="month",
                               stepmode="backward"),
                          dict(count=6,
                               label="6m",
                               step="month",
                               stepmode="backward"),
                          dict(step="all")
                      ])),
                      rangeslider=dict(visible=True),
                      type="date"),
                  hovermode='y unified')

fig.write_html('covid19_tests.html')
