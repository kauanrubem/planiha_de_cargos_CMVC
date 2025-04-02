import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from _components.efetivos import create_efetivos_figure, efetivos_layout, df_efetivos
from _components.comissionados import create_comissionados_figure, comissionados_layout, df_comissionados
from _components.inativos import create_inativos_figure, inativos_layout, df_inativos
from _components.agentes_politicos import create_agentes_figure, agentes_politicos_layout, df_agentes
from _components.estagiarios import create_estagiarios_figure, estagiarios_layout, df_estagiarios
from _components.inicial import inicial_layout

# Criação da instância do Dash e do servidor
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
server = app.server  # Servidor será exportado do app para uso externo (se necessário)
app.config.suppress_callback_exceptions = True

# Layout principal com duas colunas: esquerda (card) e direita (conteúdo dinâmico)
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(inicial_layout, xs=12, md=3, lg=2),
        dbc.Col(html.Div(id='dynamic-content'), xs=12, md=9, lg=10),
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
    
    # Callback para atualizar as opções do dropdown de nível com base no cargo selecionado
@app.callback(
    Output('dropdown-nivel', 'options'),  # Atualiza as opções do dropdown de nível
    Input('dropdown-cargo', 'value')  # Quando o cargo for alterado
)
def update_nivel_options(cargo_selecionado):
    # Filtra os dados de acordo com o cargo selecionado
    if cargo_selecionado:
        df_filtrado = df_efetivos[df_efetivos['Cargo'] == cargo_selecionado]
        niveis = df_filtrado['Nível'].unique()  # Obtém os níveis disponíveis para o cargo
    else:
        niveis = df_efetivos['Nível'].unique()  # Se nenhum cargo for selecionado, exibe todos os níveis

    # Atualiza as opções do dropdown de nível
    return [{'label': nivel, 'value': nivel} for nivel in niveis]

# Callback para atualizar o dropdown de nível dos Comissionados
@app.callback(
    Output('dropdown-nivel-comissionados', 'options'),
    Input('dropdown-cargo-comissionados', 'value')
)
def update_nivel_comissionados(cargo_selecionado):
    if cargo_selecionado:
        df_filtrado = df_comissionados[df_comissionados['Cargo'] == cargo_selecionado]
        niveis = df_filtrado['Nível'].unique()
    else:
        niveis = df_comissionados['Nível'].unique()

    return [{'label': nivel, 'value': nivel} for nivel in niveis]


# Callback para atualizar o dropdown de nível dos Inativos
@app.callback(
    Output('dropdown-nivel-inativos', 'options'),
    Input('dropdown-cargo-inativos', 'value')
)
def update_nivel_inativos(cargo_selecionado):
    if cargo_selecionado:
        df_filtrado = df_inativos[df_inativos['Cargo'] == cargo_selecionado]
        niveis = df_filtrado['Nível'].unique()
    else:
        niveis = df_inativos['Nível'].unique()

    return [{'label': nivel, 'value': nivel} for nivel in niveis]


# Callback para atualizar o dropdown de nível dos Agentes Políticos
@app.callback(
    Output('dropdown-nivel-agentes', 'options'),
    Input('dropdown-cargo-agentes', 'value')
)
def update_nivel_agentes(cargo_selecionado):
    if cargo_selecionado:
        df_filtrado = df_agentes[df_agentes['Cargo'] == cargo_selecionado]
        niveis = df_filtrado['Nível'].unique()
    else:
        niveis = df_agentes['Nível'].unique()

    return [{'label': nivel, 'value': nivel} for nivel in niveis]


# Callback para atualizar o dropdown de nível dos Estagiários
@app.callback(
    Output('dropdown-nivel-estagiarios', 'options'),
    Input('dropdown-cargo-estagiarios', 'value')
)
def update_nivel_estagiarios(cargo_selecionado):
    if cargo_selecionado:
        df_filtrado = df_estagiarios[df_estagiarios['Cargo'] == cargo_selecionado]
        niveis = df_filtrado['Nível'].unique()
    else:
        niveis = df_estagiarios['Nível'].unique()

    return [{'label': nivel, 'value': nivel} for nivel in niveis]

# Callback dos gráficos de efetivos
# Callback dos gráficos de efetivos + totais dinâmicos
@app.callback(
    [Output("fig1_efetivos", "figure"),
     Output("fig2_efetivos", "figure"),
     Output("fig3_efetivos", "figure"),
     Output("fig4_efetivos", "figure"),
     Output("fig5_efetivos", "figure"),
     Output("fig6_efetivos", "figure"),
     Output("total-fig1", "children"),
     Output("total-fig2", "children"),
     Output("total-fig3", "children"),
     Output("total-fig4", "children"),
     Output("total-fig5", "children"),
     Output("total-fig6", "children")],
    [Input('dropdown-cargo', 'value'),
     Input('dropdown-nivel', 'value')]
)
def update_graph_and_totals(cargo, nivel):
    from _components.efetivos import df_efetivos, abreviacoes

    figs = create_efetivos_figure(cargo, nivel)

    df = df_efetivos.copy()
    if cargo:
        cargo_abrev = abreviacoes.get(cargo, cargo)
        df = df[df["Cargo Abreviado"] == cargo_abrev]
    if nivel:
        df = df[df["Nível"] == nivel]

    total1 = f"Total de Efetivos: {df['Quantidade'].sum()} servidores"
    total2 = f"Valor Total do Salário Base: R$ {df['Salário Base Total'].sum():,.2f}"
    total3 = f"Valor Total das Categorias (Complementos): R$ {df[['Quinquênio','Vencimento Complementar','Periculosidade','Horas Extras 50%','Horas Extras 100%','Fiscal I','Diária','Estabilidade Econômica']].sum().sum():,.2f}"
    total4 = f"Valor Total de Incentivos: R$ {df[['Incentivo Nível Superior','Incentivo De Pós-Graduação','Incentivo - Nível Médio']].sum().sum():,.2f}"
    total5 = f"Valor Total de Categorias Especiais: R$ {df[['Aprimoramento Profissional','GCET','GAEL-EAP','GAEL - GESTOR DE CONTRATOS','GAEL - AGENTE DE CONTRATACAO']].sum().sum():,.2f}"
    total6 = f"Valor Total de Comissões (FGs): R$ {df[['Fg 01: Integrante De Comissao','Fg 03: Comissões: Pres., Sec.','Fg 04: Servicos De Apoio / Sup','Fg 05: Serv. Contante Locomoca','Fg 06: Atividades Supervisão','Fg 09: Fiscal De Contratos','Fg 10: Serv. Externo']].sum().sum():,.2f}"

    return (*figs, total1, total2, total3, total4, total5, total6)

# Callback dos gráficos de comissionados


@app.callback(
    [Output("fig1_comissionados", "figure"),
     Output("fig2_comissionados", "figure"),
     Output("fig3_comissionados", "figure"),
     Output("fig4_comissionados", "figure"),
     Output("total-fig1-comissionados", "children"),
     Output("total-fig2-comissionados", "children"),
     Output("total-fig3-comissionados", "children"),
     Output("total-fig4-comissionados", "children")],
    [Input('dropdown-cargo-comissionados', 'value'),
     Input('dropdown-nivel-comissionados', 'value')]
)
def update_comissionados_graph_and_totals(cargo, nivel):
    figs = create_comissionados_figure(cargo, nivel)

    df = df_comissionados.copy()
    if cargo:
        df = df[df["Cargo"] == cargo]
    if nivel:
        df = df[df["Nível"] == nivel]

    total1 = f"Total de Comissionados: {df['Quantidade'].sum()} servidores"
    total2 = f"Valor Total do Salário Base: R$ {df['Salário Base Total'].sum():,.2f}"
    total3 = f"Valor Total das Categorias: R$ {df[['Incentivo Nível Superior','Incentivo De Pós-Graduação','Incentivo - Nível Médio','Diária','Retroativo De Graduação/Pós','GCET','GAEL-EAP']].sum().sum():,.2f}"
    total4 = f"Valor Total de Fg 03 e Diária: R$ {df[['Fg 03: Comissões: Pres., Sec.','Diária']].sum().sum():,.2f}"

    return (*figs, total1, total2, total3, total4)

# Callback dos gráficos de inativos


@app.callback(
    [Output("fig1_inativos", "figure"),
     Output("fig2_inativos", "figure"),
     Output("total-fig1-inativos", "children"),
     Output("total-fig2-inativos", "children")],
    [Input('dropdown-cargo-inativos', 'value'),
     Input('dropdown-nivel-inativos', 'value')]
)
def update_inativos_graph_and_totals(cargo, nivel):
    figs = create_inativos_figure(cargo, nivel)

    df = df_inativos.copy()
    if cargo:
        df = df[df["Cargo"] == cargo]
    if nivel:
        df = df[df["Nível"] == nivel]

    total1 = f"Total de Inativos: {df['Quantidade'].sum()} pessoas"
    total2 = f"Valor Total da Aposentadoria/Pensão: R$ {df['Aposentadoria/Pensão por morte Total'].sum():,.2f}"

    return (*figs, total1, total2)


# Callback dos gráficos de agentes políticos
@app.callback(
    [Output("fig1_agentes", "figure"),
     Output("fig2_agentes", "figure"),
     Output("total-fig1-agentes", "children"),
     Output("total-fig2-agentes", "children")],
    [Input('dropdown-cargo-agentes', 'value'),
     Input('dropdown-nivel-agentes', 'value')]
)
def update_agentes_graph_and_totals(cargo, nivel):
    figs = create_agentes_figure(cargo, nivel)

    df = df_agentes.copy()
    if cargo:
        df = df[df["Cargo"] == cargo]
    if nivel:
        df = df[df["Nível"] == nivel]

    total1 = f"Total de Agentes Políticos: {df['Quantidade'].sum()} pessoas"
    total2 = f"Valor Total do Subsídio: R$ {df['Subsídio Total'].sum():,.2f}"
    return (*figs, total1, total2)


# Callback dos gráficos de estagiários
@app.callback(
    [Output("fig1_estagiarios", "figure"),
     Output("fig2_estagiarios", "figure"),
     Output("fig3_estagiarios", "figure"),
     Output("total-fig1-estagiarios", "children"),
     Output("total-fig2-estagiarios", "children"),
     Output("total-fig3-estagiarios", "children")],
    [Input('dropdown-cargo-estagiarios', 'value'),
     Input('dropdown-nivel-estagiarios', 'value')]
)
def update_estagiarios_graph_and_totals(cargo, nivel):
    figs = create_estagiarios_figure(cargo, nivel)

    df = df_estagiarios.copy()
    if cargo:
        df = df[df["Cargo"] == cargo]
    if nivel:
        df = df[df["Nível"] == nivel]

    total1 = f"Total de Estagiários: {df['Quantidade'].sum()} pessoas"
    total2 = f"Valor Total da Bolsa Estágio: R$ {df['Bolsa Estagio Total'].sum():,.2f}"
    total3 = f"Valor Total do Auxílio Transporte: R$ {df['Auxilio Transporte Total'].sum():,.2f}"

    return (*figs, total1, total2, total3)

# Rodar o servidor com o servidor do app importado de app.py
if __name__ == '__main__':
    app.run(debug=True)