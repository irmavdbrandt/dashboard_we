"""
Created on ...

@authors: Astrid van den Brandt & Irma van den Brandt
"""



import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from dash.dependencies import Input, Output

# Loading the data
purchase_history = pd.read_csv('/Users/IrmavandenBrandt/Downloads/dashboard_v2/Data/WE_sample_purchase_history.csv')
matrix = pd.read_csv('/Users/IrmavandenBrandt/Downloads/dashboard_v2/Data/WE_matrix_final_sample.csv')
product_data = pd.read_csv('/Users/IrmavandenBrandt/Downloads/dashboard_v2/Data/male_product_df.csv')
class_descriptions = pd.read_excel('/Users/IrmavandenBrandt/Downloads/dashboard_v2/Data/Class_descriptions.xlsx')


app = dash.Dash()

app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Recommender System Dashboard', className="app-header--title")
        ]
    ),
    dcc.Tabs(id="tabs", value='tab-men', children=[
        dcc.Tab(label='Men', value='tab-men'),
        dcc.Tab(label='Women', value='tab-women'),
        dcc.Tab(label='Boys', value='tab-boys'),
        dcc.Tab(label='Girls', value='tab-girls'),
        ],
        style={'fontFamily': 'Futura', 'fontSize': '12px', 'fontWeight': 'bold', 'textTransform': 'uppercase'}
    ),
    html.Div(id='tabs-content'),
    html.Div(
        className="row",
        children=[
            html.Div(
                # menu/settings
               className="menu",
                children=html.Div([
                    html.Div([html.Details([html.Summary('Instellingen', className="menu--title"),
                    html.Div('User Id', className="menu--subtitle"),
                    dcc.Dropdown(
                        id="user-id",
                        className='dropdown',
                        options=[
                            {'label': user, 'value': user} for user in matrix['user_id'].unique()
                        ],
                        value='',
                    ),
                    html.Div(id='purchase_history'),
                    html.Div('Product categorie aanbevelingen', className="menu--subtitle"),
                    dcc.Dropdown(
                        id="category",
                        className='dropdown',
                        options=[
                            {'label': class_description, 'value': class_description}
                            for class_description in class_descriptions['ClassDescription'].unique()
                        ],
                        value=class_descriptions['ClassDescription'][4],
                        multi=True
                    ),
                    html.Div('Gebruikers groep', className="menu--subtitle"),
                    dcc.RadioItems(
                        id="group",
                        options=[
                            {'label': 'Men', 'value':'Men'},
                            {'label': 'Women','value':'Women'},
                            {'label': 'Boys','value':'Boys'},
                            {'label': 'Girls','value':'Girls'}
                        ],
                        value=['Men'],

                        labelStyle={'display': 'table', 'margin-left': '5px'},
                    ),
                    html.Div('Sorteren op', className="menu--subtitle"),
                    dcc.Checklist(
                        id="best-worst",
                        options=[
                            {'label': 'Beste', 'value':'Beste'},
                            {'label': 'Slechtste','value':'Slechtste'},
                        ],
                        values=['Beste', 'Slechtste'],
                        labelStyle={'display': 'inline-block', 'margin-left': '5px'},
                    ),
                    html.Div('Aantal aanbevelingen', className="menu--subtitle"),
                    dcc.Slider(
                        id="slider",
                        min=1,
                        max=10,
                        marks={i: '{}'.format(i) for i in range(11)},
                        value=5,
                    ),
                ])])]),
                style={'width':'24%', 'display': 'inline-block', 'vertical-align': 'top'},
            ),
            html.Div(
                className="content",
                children=[
                    html.Div([
                        html.Div('Aankoop geschiedenis', className="content--title"),
                        html.Div(id='table-ph')
                        ],
                    ),
                    html.Div([
                        html.Div('Aanbevelingen', className="content--title"),
                        html.Div(id='table-rec')
                        ],
                    ),
                ],
                style={'width':'72%','display': 'inline-block', 'margin-right':'0px', 'float':'right'}
            ),
        ],
    ),
])

@app.callback(
    dash.dependencies.Output('table-ph', 'children'),
    [dash.dependencies.Input('user-id', 'value'),
    ])

# generates table with purchase history by chosen user_id
def generate_table_ph(value):
    return [html.Table(html.Tr([html.Td(html.Img(src=image, style={'height': '220px'})) for image in
                product_data[product_data['productid'].isin(purchase_history[purchase_history['user_id'] == value]['productid'])]['image_url']]),
                style={'display': 'block', 'overflow-x': 'auto','white-space': 'nowrap','align': 'center'})]


@app.callback(
    dash.dependencies.Output('table-rec', 'children'),
    [dash.dependencies.Input('user-id', 'value'),
     dash.dependencies.Input('best-worst', 'values'),
     dash.dependencies.Input('slider', 'value'),
    ])

# generates table with recommendations by chosen user_id
def generate_table_rec(user, sort, number):
    list_of_products = matrix[matrix['user_id'] == user].sort_values('score', ascending=False)
    if sort==['Beste']:
    # returns top 'number' best items

        return [
            html.Table(html.Tr([html.Td(html.Img(src=image, style={'height': '220px'})) for image in
                  product_data[product_data['productid'].isin(list_of_products['product_id'][:number])]['image_url']])
                       ,style={'display': 'block', 'overflow-x': 'auto','white-space': 'nowrap','align': 'center'})
               ]

    elif sort==['Slechtste']:
    # returns top 'number' worst items

        return [
            html.Table(html.Tr([html.Td(html.Img(src=image, style={'height': '220px'})) for image in
                  product_data[product_data['productid'].isin(list_of_products['product_id'][-number:])]['image_url']])
                       ,style={'display': 'block', 'overflow-x': 'auto','white-space': 'nowrap','align': 'center'})
               ]

    elif sort==['Slechtste','Beste'] or sort==['Beste','Slechtste']:
    # returns both top 'number' best and worst items

        return [
            html.Table(html.Tr([html.Td(html.Img(src=image, style={'height': '220px'})) for image in
                  product_data[product_data['productid'].isin(list_of_products['product_id'][:number])]['image_url']])
                       ,style={'display': 'block', 'overflow-x': 'auto','white-space': 'nowrap','align': 'center'}),

            html.Table(html.Tr([html.Td(html.Img(src=image, style={'height': '220px'})) for image in
                  product_data[product_data['productid'].isin(list_of_products['product_id'][-number:])]['image_url']])
                       ,style={'display': 'block', 'overflow-x': 'auto','white-space': 'nowrap','align': 'center'})

               ]






app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})



if __name__ == '__main__':
    app.run_server(debug=True)
