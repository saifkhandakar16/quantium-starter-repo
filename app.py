import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

df = pd.read_csv('data/output.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Pink Morsel Sales Visualiser', style={
        'textAlign': 'center',
        'color': '#ff69b4',
        'fontFamily': 'Arial, sans-serif',
        'padding': '20px',
        'backgroundColor': '#1a1a2e',
        'margin': '0'
    }),
    html.Div([
        html.Label('Filter by Region:', style={
            'color': 'white',
            'fontFamily': 'Arial, sans-serif',
            'fontSize': '16px',
            'marginBottom': '10px'
        }),
        dcc.RadioItems(
            id='region-filter',
            options=[
                {'label': 'All', 'value': 'all'},
                {'label': 'North', 'value': 'north'},
                {'label': 'South', 'value': 'south'},
                {'label': 'East', 'value': 'east'},
                {'label': 'West', 'value': 'west'}
            ],
            value='all',
            inline=True,
            style={'color': 'white', 'fontFamily': 'Arial, sans-serif'},
            inputStyle={'marginRight': '5px', 'marginLeft': '15px'}
        )
    ], style={
        'backgroundColor': '#16213e',
        'padding': '20px',
        'margin': '10px 20px'
    }),
    dcc.Graph(id='sales-chart'),
], style={'backgroundColor': '#1a1a2e', 'minHeight': '100vh', 'margin': '0'})

@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(region):
    if region == 'all':
        filtered = df.groupby('date')['sales'].sum().reset_index()
    else:
        filtered = df[df['region'] == region].groupby('date')['sales'].sum().reset_index()

    fig = px.line(
        filtered,
        x='date',
        y='sales',
        title=f'Pink Morsel Sales Over Time ({region.capitalize()})',
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
        text='Price Increase Jan 15 2021',
        showarrow=False,
        font=dict(color='red')
    )

    fig.update_layout(
        plot_bgcolor='#16213e',
        paper_bgcolor='#16213e',
        font=dict(color='white'),
        xaxis=dict(gridcolor='#444'),
        yaxis=dict(gridcolor='#444')
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
