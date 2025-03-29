from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from index import app

# Carregando os dados da planilha
file_path = 'dataset/Planilha de cargos - CMVC.xlsx'
df_estagiarios = pd.read_excel(file_path, sheet_name='Estagiários')

# Função para gerar os gráficos
def create_estagiarios_figure(cargo_selecionado=None, nivel_selecionado=None):
    df_grouped = df_estagiarios.groupby(['Cargo', 'Nível'])[
        ['Quantidade', 'Bolsa Estagio', 'Bolsa Estagio Total', 'Auxilio Transporte', 'Auxilio Transporte Total']
    ].sum().reset_index()

    if cargo_selecionado:
        df_grouped = df_grouped[df_grouped['Cargo'] == cargo_selecionado]
    if nivel_selecionado:
        df_grouped = df_grouped[df_grouped['Nível'] == nivel_selecionado]

    # Gráfico 1: Quantidade
    fig1 = px.bar(
        df_grouped,
        x='Cargo',
        y='Quantidade',
        color='Nível',
        title='Quantidade de Estagiários por Cargo e Nível',
        labels={'Quantidade': 'Quantidade'},
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Set2,
    )

    # Gráfico 2: Bolsa Estágio e Bolsa Estágio Total
    df_bolsa = pd.melt(
        df_grouped,
        id_vars=['Cargo', 'Nível'],
        value_vars=['Bolsa Estagio', 'Bolsa Estagio Total'],
        var_name='Tipo de Bolsa',
        value_name='Valor'
    )
    fig2 = px.bar(
        df_bolsa,
        x='Cargo',
        y='Valor',
        color='Tipo de Bolsa',
        title='Valores de Bolsa Estágio por Cargo',
        barmode='group',
        labels={'Valor': 'Valor (R$)', 'Tipo de Bolsa': 'Tipo'},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )

    # Gráfico 3: Auxílio Transporte e Auxílio Transporte Total
    df_auxilio = pd.melt(
        df_grouped,
        id_vars=['Cargo', 'Nível'],
        value_vars=['Auxilio Transporte', 'Auxilio Transporte Total'],
        var_name='Tipo de Auxílio',
        value_name='Valor'
    )
    fig3 = px.bar(
        df_auxilio,
        x='Cargo',
        y='Valor',
        color='Tipo de Auxílio',
        title='Valores de Auxílio Transporte por Cargo',
        barmode='group',
        labels={'Valor': 'Valor (R$)', 'Tipo de Auxílio': 'Tipo'},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )

    return fig1, fig2, fig3


# Layout com gráficos em cards separados
estagiarios_layout = dbc.Row([
    dbc.Col([  
        html.H1("Estagiários - Quantidade, Bolsa e Auxílio", 
                style={'font-size': '24px', 'text-align': 'center', 'margin-bottom': '20px'}),

        # Dropdowns
        dbc.Row([  
            dbc.Col([  
                dcc.Dropdown(
                    id='dropdown-cargo-estagiarios',
                    options=[{'label': c, 'value': c} for c in df_estagiarios['Cargo'].unique()],
                    placeholder="Selecione um Cargo",
                    style={'margin-bottom': '10px'}
                )
            ], width=6),
            dbc.Col([  
                dcc.Dropdown(
                    id='dropdown-nivel-estagiarios',
                    options=[{'label': n, 'value': n} for n in df_estagiarios['Nível'].unique()],
                    placeholder="Selecione um Nível",
                    style={'margin-bottom': '10px'}
                )
            ], width=6),
        ]),

        # Gráficos em cards separados com o estilo igual ao de efetivos.py
        dbc.Row([  
            dbc.Col(dbc.Card(dbc.CardBody([ 
                dcc.Graph(id='fig1_estagiarios', style={'height': '400px', 'width': '100%', 'padding': '0'})
            ])), width=6),

            dbc.Col(dbc.Card(dbc.CardBody([ 
                dcc.Graph(id='fig2_estagiarios', style={'height': '400px', 'width': '100%', 'padding': '0'})
            ])), width=6),

            dbc.Col(dbc.Card(dbc.CardBody([ 
                dcc.Graph(id='fig3_estagiarios', style={'height': '400px', 'width': '100%', 'padding': '0'})
            ])), width=6),
        ])
    ])
])

