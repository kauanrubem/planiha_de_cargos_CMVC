from dash import dcc, html
import dash_bootstrap_components as dbc

# Layout do aplicativo inicial
inicial_layout = dbc.Row([
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
        ], className="fixed-radio-items"),  # Aplica a classe fixa
    ], width=2),  # Define o tamanho da coluna como sm=2
])
