from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc

# Importando o app e o servidor do arquivo app.py
from app import app

# Importando os layouts dos componentes
from _components.efetivos import efetivos_layout
from _components.comissionados import comissionados_layout
from _components.inativos import inativos_layout
from _components.agentes_politicos import agentes_politicos_layout
from _components.estagiarios import estagiarios_layout
from _components.inicial import app as inicial_app

# Inicialização do app
# O 'app' foi importado de app.py
# O 'server' já está configurado em 'app.py', portanto, não é necessário redefini-lo aqui
app.config.suppress_callback_exceptions = True

# Layout principal do aplicativo
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(inicial_app.layout, width=2),
        dbc.Col(html.Div(id='dynamic-content'), width=10),
    ])
], fluid=True)

# Callback para alternar entre os layouts de acordo com o valor do RadioItems
@app.callback(
    Output('dynamic-content', 'children'),
    [Input('main_variable', 'value')]
)
def update_layout(selected_value):
    if selected_value == "Efetivos":
        return efetivos_layout
    elif selected_value == "Comissionados":
        return comissionados_layout
    elif selected_value == "Inativos":
        return inativos_layout
    elif selected_value == "Agentes Políticos":
        return agentes_politicos_layout
    elif selected_value == "Estágiarios":
        return estagiarios_layout

# Callback dos gráficos de efetivos
@app.callback(
    [Output("fig1_efetivos", "figure"),
     Output("fig2_efetivos", "figure"),
     Output("fig3_efetivos", "figure"),
     Output("fig4_efetivos", "figure"),
     Output("fig5_efetivos", "figure"),
     Output("fig6_efetivos", "figure")],
    [Input('dropdown-cargo', 'value'),
     Input('dropdown-nivel', 'value')]
)
def update_graph(cargo_selecionado, nivel_selecionado):
    from _components.efetivos import create_efetivos_figure
    fig1_efetivos, fig2_efetivos, fig3_efetivos, fig4_efetivos, fig5_efetivos, fig6_efetivos = create_efetivos_figure(cargo_selecionado, nivel_selecionado)
    return fig1_efetivos, fig2_efetivos, fig3_efetivos, fig4_efetivos, fig5_efetivos, fig6_efetivos

# Callback dos gráficos de comissionados
@app.callback(
    [Output("fig1_comissionados", "figure"),
     Output("fig2_comissionados", "figure"),
     Output("fig3_comissionados", "figure"),
     Output("fig4_comissionados", "figure")],
    [Input('dropdown-cargo', 'value'),
     Input('dropdown-nivel', 'value')]
)
def update_comissionados_graph(cargo_selecionado, nivel_selecionado):
    from _components.comissionados import create_comissionados_figure
    fig1_comissionados, fig2_comissionados, fig3_comissionados, fig4_comissionados = create_comissionados_figure(cargo_selecionado, nivel_selecionado)
    return fig1_comissionados, fig2_comissionados, fig3_comissionados, fig4_comissionados

# Callback dos gráficos de inativos
@app.callback(
    [Output("fig1_inativos", "figure"),
     Output("fig2_inativos", "figure")],
    [Input('dropdown-cargo-inativos', 'value'),
     Input('dropdown-nivel-inativos', 'value')]
)
def update_inativos_graph(cargo, nivel):
    from _components.inativos import create_inativos_figure
    fig1_inativos, fig2_inativos = create_inativos_figure(cargo, nivel)
    return fig1_inativos, fig2_inativos

# Callback dos gráficos de agentes políticos
@app.callback(
    [Output("fig1_agentes", "figure"),
     Output("fig2_agentes", "figure")],
    [Input('dropdown-cargo-agentes', 'value'),
     Input('dropdown-nivel-agentes', 'value')]
)
def update_agentes_graph(cargo, nivel):
    from _components.agentes_politicos import create_agentes_figure
    fig1_agentes, fig2_agentes = create_agentes_figure(cargo, nivel)
    return fig1_agentes, fig2_agentes

# Callback dos gráficos de estagiários
@app.callback(
    [Output("fig1_estagiarios", "figure"),
     Output("fig2_estagiarios", "figure"),
     Output("fig3_estagiarios", "figure")],
    [Input('dropdown-cargo-estagiarios', 'value'),
     Input('dropdown-nivel-estagiarios', 'value')]
)
def update_estagiarios_graph(cargo, nivel):
    from _components.estagiarios import create_estagiarios_figure
    fig1_estagiarios, fig2_estagiarios, fig3_estagiarios = create_estagiarios_figure(cargo, nivel)
    return fig1_estagiarios, fig2_estagiarios, fig3_estagiarios

# Rodar o servidor com o servidor do app importado de app.py
if __name__ == '__main__':
    app.run_server(debug=True)
