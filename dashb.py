import dash
from dash import dcc, html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Загрузка данных
df = pd.read_csv('Resources/finance.csv')

# Создание Dash-приложения
app = dash.Dash(__name__)
 
# Определение макета приложения
app.layout = html.Div([
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            editable=True,
            style_table={'overflowX': 'scroll'},
            style_cell={
                'whiteSpace': 'pre-line',  
                'height': 'auto', 
            },
        ),
        
        dcc.Dropdown(
            id='column-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns[1:]],
            value=df.columns[1],
            multi=True
        ),
    ], style={'width': '90%', 'margin': 'auto'}), 

    html.Div([
        dcc.Graph(id='histogram')
    ], style={'width': '50%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Graph(id='pie-chart')
    ], style={'width': '50%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='scatter-plot')
    ], style={'width': '50%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Graph(id='line-chart')
    ], style={'width': '50%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Graph(id='heatmap')
    ], style={'width': '100%'}),
])

# Callback функция для обновления графиков и гистограмм на основе выбранных столбцов данных в таблице
@app.callback(
    [Output('histogram', 'figure'),
     Output('pie-chart', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('line-chart', 'figure'),
     Output('heatmap', 'figure')],
    [Input('table', 'data'),
     Input('table', 'columns'),
     Input('column-dropdown', 'value')]
)
def update_charts(rows, columns, selected_columns):
    dff = pd.DataFrame(rows, columns=[c['name'] for c in columns])

    fig_bar = px.bar(dff, x='Проект', y=selected_columns, barmode='group')

    if len(selected_columns) > 0:
        fig_pie = px.pie(dff, values=selected_columns[0], names='Проект')
    else:
        fig_pie = px.pie(dff, values='Бюджет проекта', names='Проект')

    fig_scatter = px.scatter(dff, x='Бюджет проекта', y='Ожидаемые расходы', color='Проект')

    fig_line = px.line(dff, x='Бюджет проекта', y='Планируемые доходы', color='Проект')

    numerical_columns = dff.select_dtypes(include=['number']).columns.tolist()
    
    matrix_data = dff[numerical_columns].values

    projects = dff['Проект'].tolist()
    indicators = numerical_columns

    fig_heatmap = go.Figure(data=go.Heatmap(
        z=matrix_data,
        x=indicators,  # Теперь индикаторы на оси X
        y=projects,  # Проекты на оси Y
        colorscale='Viridis'
    ))

    fig_heatmap.update_layout(
        title='Тепловая карта показателей проектов',
        xaxis_title='Показатели',
        yaxis_title='Проекты'
    )

    return fig_bar, fig_pie, fig_scatter, fig_line, fig_heatmap
if __name__ == '__main__':
    app.run_server(debug=True)