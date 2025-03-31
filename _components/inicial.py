from dash import dcc, html
import dash_bootstrap_components as dbc

# Layout do aplicativo inicial
inicial_layout = dbc.Row([
    dbc.Col([ 
        dbc.Card([ 
            html.Img(src="assets/camara_municipal_VCA.jpg", style={"width": "100%"}),
            html.Hr(),
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
            html.Hr(),
            # Card com totalizador em linha única
            dbc.Card(
                dbc.CardBody(
                    html.Div([
                        html.Span("Totalizador: ",
                                  style={"fontWeight": "bold", "fontSize": "14px"}),
                        html.Span("R$ 1.940.102,09",
                                  style={"fontWeight": "bold", "fontSize": "15px", "color": "#2c3e50", "whiteSpace": "nowrap"})
                    ],
                    style={"textAlign": "center"})
                ),
                style={"marginBottom": "10px"}
            ),
        ], className="fixed-radio-items"),
    ], width=2),
])
