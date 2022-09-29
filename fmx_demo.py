import dash  # use Dash version 1.16.0 or higher for this app to work
from dash import dcc, html
from dash.dependencies import Output, Input
from dash_extensions import Lottie       # pip install dash-extensions
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px
import plotly.graph_objects as go              # pip install plotly
import pandas as pd                       # pip install pandas
from wordcloud import WordCloud          # pip install wordcloud

# Lottie by Emil - https://github.com/thedirtyfew/dash-extensions
url_coonections = "https://assets7.lottiefiles.com/packages/lf20_jzixommu.json"
url_engage = "https://assets1.lottiefiles.com/private_files/lf30_4bozb1lk.json"
url_prfl = "https://assets2.lottiefiles.com/private_files/lf30_xa2hm6z1.json"
url_reach = "https://assets5.lottiefiles.com/packages/lf20_vpxae5vy.json"
url_reactions = "https://assets2.lottiefiles.com/packages/lf20_nKwET0.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

df = pd.read_csv(r'ata_1.txt', encoding='latin1', sep='\t', lineterminator='\n')

# Función para resumir col FUENTES DE DATOS
def src(x):
    if x == 'Twitter':
        return x
    elif x == 'Facebook':
        return x
    elif x == 'Reddit':
        return x    
    else:
        return 'Blogs y notas'

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

# Applying the conditions
df['Date'] = pd.to_datetime(df['Date'])
df['Source'] = df['Source'].apply(src)


# Bootstrap themes by Ann: https://hellodash.pythonanywhere.com/theme_explorer
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardImg(src='/assets/atz_logo_small.png') # 150px by 45px
            ],
             style={"width": "300px", "height": "100px"},
             className='mb-2'),
            dbc.Card([
                dbc.CardBody([
                    html.H4("Escucha Digital", className="card-title"),
                    html.P(
                        "Se presenta un análisis sobre las focos de conversación en medios digitales "
                        "en medios digitales sobre el Presidente Pedro Rodríguez Villegas " 
                        "y el Gobierno Municipal de Atizapán de Zaragoza ",
                        className="card-text text-wrap",
                    ),                    
                    
                    dbc.CardLink("Gobierno Municipal de Atizapán de Zaragoza", target="_blank",
                                 href="https://www.facebook.com/GobAtizapan/"
                    )
                ])
            ], color="info", inverse=True),
        ], width=8),
        dbc.Col([
            dcc.Dropdown(id='dpdn2', value=['Facebook','Twitter'], multi=True,
                        options=[{'label': x, 'value': x} for x in df['Source'].unique()]),
            dcc.Markdown(children='', id='text-desc', style={'color':'purple'}),
            

        ], width={'size':4, 'offset':0, 'order':2}
        ,  className='text-center fs-4 row align-items-center' 
           #xs=12, sm=12, md=12, lg=5, xl=5
        ),
    ],className='mb-2 mt-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=url_coonections)),
                dbc.CardBody([
                    html.H6('Total de Menciones'),
                    html.H2(id='content-connections', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=url_engage)),
                dbc.CardBody([
                    html.H6('Engagement Obtenido'),
                    html.H2(id='content-companies', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=url_prfl)),
                dbc.CardBody([
                    html.H6('Perfiles Únicos'),
                    html.H2(id='content-msg-in', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=url_reach)),
                dbc.CardBody([
                    html.H6('Alcance total'),
                    html.H2(id='content-msg-out', children="000")
                ], style={'textAlign': 'center'})
            ]),
        ], width=3)
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='line-chart', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='pie-chart', figure={}),
                ])
            ]),
        ], width=5),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='bar-chart', figure={}),
                ])
            ]),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='wordcloud', figure={}),
                ])
            ]),
        ], width=6),
    ],className='mb-2'),
], fluid=True)


# Updating Description
@app.callback(
    Output('text-desc','children'),
    Input('dpdn2', component_property='value')
)
def update_markdown(src_chosen):
    df_m = df.copy()
    df_m = df_m[df_m['Source'].isin(src_chosen)]
    return "Se detectaron {} menciones en el ámbito digital general el {}. \n".format(df_m.shape[0], df_m['Date'].dt.strftime('%d-%m')[0])
    #return "Hay {} observaciones y {} columnas/variables/features en este DF. \n".format(df_m.shape[0],df_m.shape[1])


# Updating the 5 number cards
@app.callback(
    Output('content-connections','children'),
    Output('content-companies','children'),
    Output('content-msg-in','children'),
    Output('content-msg-out','children'),
    Input('dpdn2', component_property='value')
)
def update_graph(src_chosen):
    dff = df.copy()
    dff = dff[dff['Source'].isin(src_chosen)]
    total_mentions = dff.shape[0]
    total_engagament = dff['Engagement'].sum()
    unique_users = len(dff["User Profile Url"].unique())
    value = dff['Reach'].sum()    
    total_reach = f'{value:,}'  
    
    return total_mentions, total_engagament, unique_users, total_reach


# Line Chart ***********************************************************
@app.callback(
    Output('line-chart','figure'),
    Input('dpdn2', component_property='value')
)
def update_line(src_chosen):
    dff = df.copy() 
    dff = dff[dff['Source'].isin(src_chosen)]
    dff2 = dff.groupby([dff['Date'].dt.strftime('%H')]).Date.count()
    fig_line = px.line(dff2, y='Date', template='ggplot2',
                  title="Menciones por Hora")
    fig_line.update_traces(mode="lines+markers", fill='tozeroy',line={'color':'mediumpurple'})
    fig_line.update_layout(margin=dict(l=20, r=20, t=30, b=20))

    return fig_line


# Pie Chart ***********************************************************
@app.callback(
    Output('pie-chart','figure'),
    Input('dpdn2', component_property='value')
)
def update_pie(src_chosen):
    df_p = df.copy() 
    df_p = df_p[df_p['Source'].isin(src_chosen)]
    df_p = pd.DataFrame(df_p.Sentiment.value_counts())
    df_p.reset_index(inplace=True)
    #print(df_p)
    fig2 = px.pie(df_p, values='Sentiment', names='index', color='index',
                    template='ggplot2', title='Sentiment Detectado',
                    color_discrete_map={
                                    "Positive": "limegreen",
                                    "Negative": "orangered",
                                    "Neutral": "grey"})
    fig2.update_traces(textfont_size=20, hole=0.5,
                  marker=dict(line=dict(color='white', width=2)))

    return fig2


# Word Cloud ************************************************************
@app.callback(
    Output('wordcloud','figure'),
    Input('dpdn2', component_property='value')
)
def update_cloud(src_chosen):
    df_w = df.copy() 
    df_w = df_w[df_w['Source'].isin(src_chosen)]
    df_w.dropna(subset=['Key Phrases'],inplace=True)
    #df_w['Key Phrases'] = str(df_w['Key Phrases'])
    my_wordcloud = WordCloud(
        background_color='white',
        relative_scaling=0.5,
        repeat=True,
        height=275
    ).generate(' '.join(df_w['Key Phrases']))
    fig_wordcloud = px.imshow(my_wordcloud, template='ggplot2',
                              title="Términos Más Frecuentes")
    fig_wordcloud.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig_wordcloud.update_xaxes(visible=False)
    fig_wordcloud.update_yaxes(visible=False)

    return fig_wordcloud


# Bar chart ************************************************************
@app.callback(
    Output('bar-chart','figure'),
    Input('dpdn2', component_property='value')
)
def update_bar(src_chosen):
    df_b = df.copy() 
    df_b = df_b[df_b['Source'].isin(src_chosen)]
    df_b = df_b.groupby(df_b['Source']).URL.count().to_frame().reset_index()
    ordered_df = df_b.sort_values(by='URL', ascending=False)
    #fig_bar = px.bar(ordered_df, x='Source', y='URL')
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        y=ordered_df['URL'],
        x=ordered_df['Source'],
        text=ordered_df['URL'],
        textposition="inside",
        marker=dict(
            color='rgba(246, 78, 139, 0.6)',
            line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
        )
    ))
    fig_bar.update_layout(title='Plataformas', barmode="overlay", showlegend=False, template="presentation",margin=dict(l=10, r=10, t=40, b=20))
    fig_bar.update_yaxes(visible=False)
    return fig_bar


if __name__=='__main__':
    app.run_server(debug=False)
