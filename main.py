from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__)

years = df['year'].unique()

app.layout = html.Div([
    html.H1(children='Countries', style={'textAlign': 'center'}),

    html.P(children='Страны'),

    dcc.Dropdown(options=[{'label': country, 'value': country} for country in df.country.unique()],
                 value=['Russia'], multi=True, id='dropdown-selection'),

    html.P(children='Ось Y линейного графика'),

    dcc.Dropdown(options=[{'label': measure, 'value': measure} for measure in ['pop', 'gdpPercap', 'lifeExp']],
                 value='pop', id='y-axis'),

    dcc.Graph(id='line-chart'),

    html.H2(children='Год'),

    dcc.Dropdown(options=[{'label': year, 'value': year} for year in years],
                 value=years[-1], id='year-dropdown'),

    html.P(children='Ось X'),

    dcc.Dropdown(options=[{'label': measure, 'value': measure} for measure in ['pop', 'gdpPercap', 'lifeExp']],
                 value='pop', id='bubble-x-axis'),

    html.P(children='Ось Y'),
    dcc.Dropdown(options=[{'label': measure, 'value': measure} for measure in ['pop', 'gdpPercap', 'lifeExp']],
                 value='pop', id='bubble-y-axis'),

    html.P(children='Размер'),
    dcc.Dropdown(options=[{'label': measure, 'value': measure} for measure in ['pop', 'gdpPercap', 'lifeExp']],
                 value='pop', id='bubble-size'),

    dcc.Graph(id='bubble-chart'),

    dcc.Graph(id='top-15-population-chart'),

    dcc.Graph(id='population-by-continent-chart')
])


@app.callback(
    Output('line-chart', 'figure'),
    Output('bubble-chart', 'figure'),
    Output('top-15-population-chart', 'figure'),
    Output('population-by-continent-chart', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('y-axis', 'value'),
    Input('bubble-x-axis', 'value'),
    Input('bubble-y-axis', 'value'),
    Input('bubble-size', 'value'),
    Input('year-dropdown', 'value')
)
def update_graph(selected_countries, y_axis, bubble_x_axis, bubble_y_axis, bubble_size, selected_year):
    dff = df[df.country.isin(selected_countries)]

    line_fig = px.line(dff, x='year', y=y_axis, color='country')

    bubble_fig = px.scatter(df[df['year'] == selected_year], x=bubble_x_axis, y=bubble_y_axis, size=bubble_size,
                            color='country', hover_name='country', log_x=True)

    top_15_pop = df[df['year'] == selected_year].nlargest(15, 'pop')
    top_15_pop_fig = px.bar(top_15_pop, x='country', y='pop', color='country',
                            title=f'Top 15 Countries by Population ({selected_year})')

    pop_by_continent_fig = px.pie(df[df['year'] == selected_year], values='pop', names='continent',
                                  title=f'Population Distribution by Continent ({selected_year})')

    return line_fig, bubble_fig, top_15_pop_fig, pop_by_continent_fig


if __name__ == '__main__':
    app.run_server(debug=True)
