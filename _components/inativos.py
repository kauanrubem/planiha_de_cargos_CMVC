from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Carregar os dados da planilha
file_path = 'dataset/Planilha de cargos - CMVC.xlsx'
df_inativos = pd.read_excel(file_path, sheet_name='Inativos')

# Função para gerar os gráficos
def create_inativos_figure(cargo_selecionado=None, nivel_selecionado=None):
    df_grouped = df_inativos.groupby(['Cargo', 'Nível'])[['Quantidade',
        'Aposentadoria/Pensão por morte',
        'Aposentadoria/Pensão por morte Total']].sum().reset_index()

    if cargo_selecionado:
        df_grouped = df_grouped[df_grouped['Cargo'] == cargo_selecionado]
    if nivel_selecionado:
        df_grouped = df_grouped[df_grouped['Nível'] == nivel_selecionado]

    # Gráfico 1: Quantidade
    fig1_inativos = px.bar(
        df_grouped,
        x='Cargo',
        y='Quantidade',
        color='Nível',
        title="Quantidade de Inativos por Cargo e Nível",
        labels={'Quantidade': 'Quantidade de Inativos'},
        color_discrete_sequence=px.colors.qualitative.Set2,
        barmode='group',
        hover_data=['Nível']
    )

    # Gráfico 2: Aposentadoria/Pensão
    df_melted = pd.melt(
        df_grouped,
        id_vars=['Cargo', 'Nível'],
        value_vars=['Aposentadoria/Pensão por morte'],
        var_name='Tipo de Benefício',
        value_name='Valor'
    )

    fig2_inativos = px.bar(
        df_melted,
        x='Cargo',
        y='Valor',
        color='Tipo de Benefício',
        title="Valores de Aposentadoria/Pensão por Cargo e Nível",
        labels={'Valor': 'Valor (R$)', 'Tipo de Benefício': 'Benefício'},
        color_discrete_sequence=px.colors.qualitative.Set2,
        barmode='group',
        hover_data=['Nível']
    )

    return fig1_inativos, fig2_inativos

# Layout com gráficos em cards separados
inativos_layout = dbc.Row([
    dbc.Col([
        html.H1("Inativos - Quantidade e Benefícios", id="grafico-titulo", 
                style={'font-size': '24px', 'text-align': 'center', 'margin-bottom': '20px'}),

        dbc.Row([
            dbc.Col([ 
                dcc.Dropdown(
                    id='dropdown-cargo-inativos',
                    options=[{'label': c, 'value': c} for c in df_inativos['Cargo'].unique()],
                    placeholder="Selecione um Cargo",
                    style={'margin-bottom': '10px'}
                )
            ], width=6),

            dbc.Col([ 
                dcc.Dropdown(
                    id='dropdown-nivel-inativos',
                    options=[{'label': n, 'value': n} for n in df_inativos['Nível'].unique()],
                    placeholder="Selecione um Nível",
                    style={'margin-bottom': '10px'}
                )
            ], width=6),
        ]),

        dbc.Row([  
    dbc.Col(dbc.Card(dbc.CardBody([ 
        dcc.Graph(id='fig2_inativos', style={'height': '400px', 'width': '100%', 'padding': '0'}),
        html.Div(id='total-fig2-inativos', style={'marginTop': '10px', 'fontWeight': 'bold', 'width': '100%', 'display': 'flex','justifyContent': 'left', 'textAlign': 'left'})
    ])), xs=12, md=6),

    dbc.Col(dbc.Card(dbc.CardBody([ 
        dcc.Graph(id='fig1_inativos', style={'height': '400px', 'width': '100%', 'padding': '0'}),
        html.Div(id='total-fig1-inativos', style={'marginTop': '10px', 'fontWeight': 'bold', 'width': '100%', 'display': 'flex','justifyContent': 'left', 'textAlign': 'left'})
    ])), xs=12, md=6),
])

    ])
])

