from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Carregando os dados da aba "Agentes Políticos"
file_path = 'dataset/Planilha de cargos - CMVC.xlsx'
df_agentes = pd.read_excel(file_path, sheet_name='Agentes Políticos')

# Função que gera os dois gráficos
def create_agentes_figure(cargo_selecionado=None, nivel_selecionado=None):
    df_grouped = df_agentes.groupby(['Cargo', 'Nível'])[['Quantidade', 'Subsídio', 'Subsídio Total']].sum().reset_index()

    if cargo_selecionado:
        df_grouped = df_grouped[df_grouped['Cargo'] == cargo_selecionado]
    if nivel_selecionado:
        df_grouped = df_grouped[df_grouped['Nível'] == nivel_selecionado]

    # Gráfico 1 – Quantidade
    fig1_agentes = px.bar(
        df_grouped,
        x='Cargo',
        y='Quantidade',
        color='Nível',
        title='Quantidade de Agentes Políticos por Cargo e Nível',
        labels={'Quantidade': 'Quantidade'},
        color_discrete_sequence=px.colors.qualitative.Set2,
        barmode='group',
        hover_data=['Nível']
    )

    # Gráfico 2 – Subsídio e Subsídio Total
    df_melted = pd.melt(df_grouped, id_vars=['Cargo', 'Nível'],
                        value_vars=['Subsídio', 'Subsídio Total'],
                        var_name='Tipo de Subsídio', value_name='Valor')

    fig2_agentes = px.bar(
        df_melted,
        x='Cargo',
        y='Valor',
        color='Tipo de Subsídio',
        title='Subsídio e Subsídio Total por Cargo e Nível',
        labels={'Valor': 'Valor (R$)', 'Tipo de Subsídio': 'Tipo'},
        color_discrete_sequence=px.colors.qualitative.Set2,
        barmode='group',
        hover_data=['Nível']
    )

    return fig1_agentes, fig2_agentes


# Layout dos Agentes Políticos com gráficos em cards separados
agentes_politicos_layout = dbc.Row([
    dbc.Col([ 
        html.H1("Agentes Políticos - Subsídios e Quantidade", 
                style={'font-size': '24px', 'text-align': 'center', 'margin-bottom': '20px'}),

        # Dropdowns
        dbc.Row([
            dbc.Col([ 
                dcc.Dropdown(
                    id='dropdown-cargo-agentes',
                    options=[{'label': c, 'value': c} for c in df_agentes['Cargo'].unique()],
                    placeholder="Selecione um Cargo",
                    style={'margin-bottom': '10px'}
                )
            ], width=6),
            dbc.Col([ 
                dcc.Dropdown(
                    id='dropdown-nivel-agentes',
                    options=[{'label': n, 'value': n} for n in df_agentes['Nível'].unique()],
                    placeholder="Selecione um Nível",
                    style={'margin-bottom': '10px'}
                )
            ], width=6),
        ]),

        # Gráficos em cards separados com o estilo igual ao de efetivos.py
        dbc.Row([
    dbc.Col(dbc.Card(dbc.CardBody([ 
        dcc.Graph(id='fig2_agentes', style={'height': '400px', 'width': '100%', 'padding': '0'}),
        html.Div(id='total-fig2-agentes', style={'marginTop': '10px', 'fontWeight': 'bold', 'width': '100%', 'display': 'flex','justifyContent': 'left', 'textAlign': 'left'})
    ])), xs=12, md=6),

    dbc.Col(dbc.Card(dbc.CardBody([ 
        dcc.Graph(id='fig1_agentes', style={'height': '400px', 'width': '100%', 'padding': '0'}),
        html.Div(id='total-fig1-agentes', style={'marginTop': '10px', 'fontWeight': 'bold', 'width': '100%', 'display': 'flex','justifyContent': 'left', 'textAlign': 'left'})
    ])), xs=12, md=6),
])

    ])
])


