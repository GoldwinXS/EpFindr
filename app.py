import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.io as plt_io
from imdb import IMDb

""" STYLE """

card_style = {'width': '90%', 'padding': '5pt', 'margin': '10pt'}

background_color = "#202232"
text_color = '#DEE5E5'
panel_color = '#2D2D39'
accent_color = "#EA9010"

text_style = {"color": text_color, 'margin': '3pt', 'textAlign': 'center'}
div_style = {'background-color': panel_color, 'margin': '5pt', 'padding': '5pt'}

# create our custom_dark theme from the plotly_dark template
plt_io.templates["custom_dark"] = plt_io.templates["plotly_dark"]

# set the paper_bgcolor and the plot_bgcolor to a new color
plt_io.templates["custom_dark"]['layout']['paper_bgcolor'] = panel_color
plt_io.templates["custom_dark"]['layout']['plot_bgcolor'] = panel_color
plt_io.templates["custom_dark"]['layout']['font_color'] = text_color

# you may also want to change gridline colors if you are modifying background
plt_io.templates['custom_dark']['layout']['yaxis']['gridcolor'] = background_color
plt_io.templates['custom_dark']['layout']['xaxis']['gridcolor'] = background_color

app = dash.Dash(__name__, title='EpFindr', external_stylesheets=[dbc.themes.BOOTSTRAP])

""" ELEMENTS """

explanation = dcc.Markdown(
    '''
    # Welcome to Epfindr! 
    
    You can use this little app to find the best (or worst) of your favorite shows!
    
    # Usage
    1. Enter the name of a show into the box below. This will then search imdb and populate the dropdown to the
     right with options.
    2. Select an option from the dropdown
    3. Wait for your results!  
    
    ''')
title_input = dcc.Input(id='title-input')
selection_dropdown = dcc.Dropdown(id='selection-dropdown', style={'width': '50rem'})
result_graph = dcc.Loading(html.Div('Please search for a title to populate this graph', id='result-graph'))

""" LAYOUT """

app.layout = html.Center([
    dbc.Card(explanation, style=card_style, ),
    dbc.Card([dbc.CardHeader('Search Area'),
              dbc.CardBody([dbc.Row([title_input, selection_dropdown])])],
             style=card_style,
             className='align-self-center'),

    dbc.Card([dbc.CardHeader('Results'), result_graph],
             style=card_style,
             className='align-self-center'
             )
])

""" CALLBACKS """


@app.callback(Output('selection-dropdown', 'options'),
              Input('title-input', 'value'))
def update_options(title):
    """ Returns valid options for the dropdown menu from IMDb's search """
    if title is None:
        return []
    else:
        search_results = IMDb().search_movie(title)
        return [{'label': title.data['title'], 'value': title.movieID}
                for title in search_results]


def fetch_data(movieID: str) -> pd.DataFrame:
    """ Returns a dataframe with columns relevant for the app """
    ia = IMDb()
    result = ia.get_movie(movieID)
    ia.update(result, 'episodes')
    columns = ['season', 'episode', 'name', 'rating', ]
    data = {var: [] for var in columns}

    if 'episodes' not in result.keys():
        return 'Are you sure this is a show?'

    for k, v in result['episodes'].items():
        data['season'] += [eps['season'] for eps in v.values()]
        data['episode'] += [eps['episode'] for eps in v.values()]
        data['name'] += [eps['title'] for eps in v.values()]
        # some shows are there but are not yet rated
        data['rating'] += [eps['rating'] if 'rating' in eps.keys() else None for eps in v.values()]
    return pd.DataFrame(data)


@app.callback(
    Output('result-graph', 'children'),
    Input('selection-dropdown', 'value'), )
def update_graph(movieID):
    if not movieID:
        raise PreventUpdate
    else:
        df = fetch_data(movieID)
        return dcc.Graph(figure=px.line(df,
                                        x=df.index,
                                        y='rating',
                                        color='season',
                                        hover_data=['name', 'season', 'episode', 'rating'],
                                        template='custom_dark'))


# best way to style body tag
app.index_string = app.index_string.replace("<body>", f"<body style=\"background-color:{background_color}\";>")
server = app.server

if __name__ == '__main__':
    app.run_server(debug=False)
