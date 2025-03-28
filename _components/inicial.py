from dash import dcc, html
import dash_bootstrap_components as dbc
from app import app

# Layout do aplicativo inicial
app.layout = dbc.Row([
    dbc.Col([ 
        dbc.Card([ 
            html.Img(src="assets/LOPES CONSULTORIA.png", style={"width": "100%"}),
            html.Hr(),
            dcc.RadioItems(  # RadioItems que será fixo
                options=[
                    {"label": "Efetivos", "value": "Efetivos"},
                    {"label": "Comissionados", "value": "Comissionados"},
                    {"label": "Inativos", "value": "Inativos"},
                    {"label": "Agentes Políticos", "value": "Agentes Políticos"},
                    {"label": "Estágiarios", "value": "Estágiarios"},
                ],
                value="Efetivos",  # Valor padrão
                id="main_variable",  # ID para a seleção
                inline=True
            ),
            # Dropdowns para Cargo e Nível
            dbc.Row([
                dbc.Col([  
                    dcc.Dropdown(
                        id='dropdown-cargo',
                        options=[{'label': c, 'value': c} for c in ['Cargo 1', 'Cargo 2', 'Cargo 3']],  # Ajuste conforme necessário
                        placeholder="Selecione um Cargo",
                    ),
                ], width=6),
                dbc.Col([  
                    dcc.Dropdown(
                        id='dropdown-nivel',
                        options=[{'label': n, 'value': n} for n in ['Nível 1', 'Nível 2', 'Nível 3']],  # Ajuste conforme necessário
                        placeholder="Selecione um Nível",
                    ),
                ], width=6),
            ]),
            # Campo de entrada para valor ou quantidade
            dbc.Row([
                dbc.Col([  
                    dcc.Input(
                        id='input-valor',
                        type='number',
                        placeholder="Digite o valor ou quantidade para alteração",
                        style={'margin-top': '10px'}
                    ),
                ], width=12),
            ])
        ], className="fixed-radio-items"),  # Aplica a classe fixa
    ], width=2),  # Define o tamanho da coluna como sm=2
])
