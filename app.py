import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

df = pd.read_csv('data/output.csv')

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

df_grouped = df.groupby('date')['sales'].sum().reset_index()

fig = px.line(
    df_grouped,
    x='date',
    y='sales',
    title='Pink Morsel Sales Over Time',
    labels={'date': 'Date', 'sales': 'Sales ($)'}
)

fig.add_shape(
    type='line',
    x0='2021-01-15', x1='2021-01-15',
    y0=0, y1=1,
    xref='x', yref='paper',
    line=dict(color='red', dash='dash')
)

fig.add_annotation(
    x='2021-01-15', y=1,
    xref='x', yref='paper',
    text='Price Increase',
    showarrow=False
)

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Pink Morsel Sales Visualiser'),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True)
