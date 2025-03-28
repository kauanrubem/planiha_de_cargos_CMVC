from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc

from _components.efetivos import create_efetivos_figure, efetivos_layout
from _components.comissionados import create_comissionados_figure, comissionados_layout
from _components.inativos import create_inativos_figure, inativos_layout
from _components.agentes_politicos import create_agentes_figure, agentes_politicos_layout
from _components.estagiarios import create_estagiarios_figure, estagiarios_layout  # ✅ NOVO
from _components.inicial import app as inicial_app

# Inicialização do app
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
app.config.suppress_callback_exceptions = True

# Layout principal com duas colunas: esquerda (card) e direita (conteúdo dinâmico)
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(inicial_app.layout, width=2),
        dbc.Col(html.Div(id='dynamic-content'), width=10),
    ])
], fluid=True)

# Callback para alternar entre os layouts por tipo selecionado
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
     Input('dropdown-nivel', 'value'),
     Input('input-valor', 'value')]  # Novo input para capturar o valor
)
def update_graph(cargo_selecionado, nivel_selecionado, valor_input):
    # Lógica para alteração do valor ou quantidade
    if valor_input:
        valor_input = float(valor_input)  # Garantir que o valor seja numérico

    # Criar os gráficos com a alteração dos valores, se necessário
    fig1_efetivos, fig2_efetivos, fig3_efetivos, fig4_efetivos, fig5_efetivos, fig6_efetivos = create_efetivos_figure(cargo_selecionado, nivel_selecionado)

    # Alterar os valores dos gráficos (exemplo: multiplicar a quantidade ou valor por um fator)
    if valor_input:
        fig1_efetivos.update_traces(y=[y * valor_input for y in fig1_efetivos.data[0].y])  # Exemplo de alteração da quantidade
        fig2_efetivos.update_traces(y=[y * valor_input for y in fig2_efetivos.data[0].y])  # Exemplo para o gráfico de salários
        fig3_efetivos.update_traces(y=[y * valor_input for y in fig3_efetivos.data[0].y])
        fig4_efetivos.update_traces(y=[y * valor_input for y in fig4_efetivos.data[0].y])
        fig5_efetivos.update_traces(y=[y * valor_input for y in fig5_efetivos.data[0].y])
        fig6_efetivos.update_traces(y=[y * valor_input for y in fig6_efetivos.data[0].y])

    return fig1_efetivos, fig2_efetivos, fig3_efetivos, fig4_efetivos, fig5_efetivos, fig6_efetivos

# Callback dos gráficos de comissionados
@app.callback(
    [Output("fig1_comissionados", "figure"),
     Output("fig2_comissionados", "figure"),
     Output("fig3_comissionados", "figure"),
     Output("fig4_comissionados", "figure")],
    [Input('dropdown-cargo', 'value'),
     Input('dropdown-nivel', 'value'),
     Input('input-valor', 'value')]  # Novo input para capturar o valor
)
def update_comissionados_graph(cargo_selecionado, nivel_selecionado, valor_input):
    # Lógica para alteração do valor ou quantidade
    if valor_input:
        valor_input = float(valor_input)  # Garantir que o valor seja numérico

    # Criar os gráficos com a alteração dos valores, se necessário
    fig1_comissionados, fig2_comissionados, fig3_comissionados, fig4_comissionados = create_comissionados_figure(cargo_selecionado, nivel_selecionado)

    # Alterar os valores dos gráficos (exemplo: multiplicar a quantidade ou valor por um fator)
    if valor_input:
        fig1_comissionados.update_traces(y=[y * valor_input for y in fig1_comissionados.data[0].y])  # Exemplo de alteração da quantidade
        fig2_comissionados.update_traces(y=[y * valor_input for y in fig2_comissionados.data[0].y])  # Exemplo para o gráfico de salários
        fig3_comissionados.update_traces(y=[y * valor_input for y in fig3_comissionados.data[0].y])
        fig4_comissionados.update_traces(y=[y * valor_input for y in fig4_comissionados.data[0].y])

    return fig1_comissionados, fig2_comissionados, fig3_comissionados, fig4_comissionados

# Callback dos gráficos de inativos
@app.callback(
    [Output("fig1_inativos", "figure"),
     Output("fig2_inativos", "figure")],
    [Input('dropdown-cargo-inativos', 'value'),
     Input('dropdown-nivel-inativos', 'value'),
     Input('input-valor', 'value')]  # Novo input para capturar o valor
)
def update_inativos_graph(cargo, nivel, valor_input):
    # Lógica para alteração do valor ou quantidade
    if valor_input:
        valor_input = float(valor_input)  # Garantir que o valor seja numérico

    # Criar os gráficos com a alteração dos valores, se necessário
    fig1_inativos, fig2_inativos = create_inativos_figure(cargo, nivel)

    # Alterar os valores dos gráficos (exemplo: multiplicar a quantidade ou valor por um fator)
    if valor_input:
        fig1_inativos.update_traces(y=[y * valor_input for y in fig1_inativos.data[0].y])  # Exemplo de alteração da quantidade
        fig2_inativos.update_traces(y=[y * valor_input for y in fig2_inativos.data[0].y])  # Exemplo para o gráfico de salários

    return fig1_inativos, fig2_inativos

# Callback dos gráficos de agentes políticos
@app.callback(
    [Output("fig1_agentes", "figure"),
     Output("fig2_agentes", "figure")],
    [Input('dropdown-cargo-agentes', 'value'),
     Input('dropdown-nivel-agentes', 'value'),
     Input('input-valor', 'value')]  # Novo input para capturar o valor
)
def update_agentes_graph(cargo, nivel, valor_input):
    # Lógica para alteração do valor ou quantidade
    if valor_input:
        valor_input = float(valor_input)  # Garantir que o valor seja numérico

    # Criar os gráficos com a alteração dos valores, se necessário
    fig1_agentes, fig2_agentes = create_agentes_figure(cargo, nivel)

    # Alterar os valores dos gráficos (exemplo: multiplicar a quantidade ou valor por um fator)
    if valor_input:
        fig1_agentes.update_traces(y=[y * valor_input for y in fig1_agentes.data[0].y])  # Exemplo de alteração da quantidade
        fig2_agentes.update_traces(y=[y * valor_input for y in fig2_agentes.data[0].y])  # Exemplo para o gráfico de salários

    return fig1_agentes, fig2_agentes

# Callback dos gráficos de estagiários
@app.callback(
    [Output("fig1_estagiarios", "figure"),
     Output("fig2_estagiarios", "figure"),
     Output("fig3_estagiarios", "figure")],
    [Input('dropdown-cargo-estagiarios', 'value'),
     Input('dropdown-nivel-estagiarios', 'value'),
     Input('input-valor', 'value')]  # Novo input para capturar o valor
)
def update_estagiarios_graph(cargo, nivel, valor_input):
    # Lógica para alteração do valor ou quantidade
    if valor_input:
        valor_input = float(valor_input)  # Garantir que o valor seja numérico

    # Criar os gráficos com a alteração dos valores, se necessário
    fig1_estagiarios, fig2_estagiarios, fig3_estagiarios = create_estagiarios_figure(cargo, nivel)

    # Alterar os valores dos gráficos (exemplo: multiplicar a quantidade ou valor por um fator)
    if valor_input:
        fig1_estagiarios.update_traces(y=[y * valor_input for y in fig1_estagiarios.data[0].y])  # Exemplo de alteração da quantidade
        fig2_estagiarios.update_traces(y=[y * valor_input for y in fig2_estagiarios.data[0].y])  # Exemplo para o gráfico de salários
        fig3_estagiarios.update_traces(y=[y * valor_input for y in fig3_estagiarios.data[0].y])

    return fig1_estagiarios, fig2_estagiarios, fig3_estagiarios

# Rodar o servidor
if __name__ == '__main__':
    app.run(debug=True)
