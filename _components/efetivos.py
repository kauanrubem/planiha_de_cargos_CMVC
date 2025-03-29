from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd  # Para manipulação dos dados
import dash_bootstrap_components as dbc
from app import app

# Carregar os dados da planilha fora da função para ser acessível globalmente
file_path = 'dataset/Planilha de cargos - CMVC.xlsx'  # Caminho do arquivo carregado
df_efetivos = pd.read_excel(file_path, sheet_name='Efetivos')  # Carregar dados da planilha

# Abreviação manual dos nomes de cargos
abreviacoes = {
    "AGENTE DE SERVICOS AUXILIARES": "AG. AUX.",
    "AGENTE LEGISLATIVO": "AG. LEG.",
    "AGENTE PATRIMONIAL": "AG. PATRIM.",
    "JORNALISTA": "JORN.",
    "MOTORISTA": "MOT.",
    "SECRETARIO(A) DE PLENARIO": "SEC. PLEN.",
    "TECNICO DA CONTABILIDADE": "TÉC. CONTAB.",
    "TECNICO EM INFORMATICA": "TÉC. INF.",
    "GERENTE DE ALMOXARIFADO": "GER. ALMOX.",
    "GERENTE DE PATRIMONIO E MANUTENÇÃO PREDIAL": "GER. PATRIM.",
    "DIRETOR FINANCEIRO": "DIR. FIN.",
    "COORDENADOR DE TECNOLOGIA DA INFORMAÇÃO": "COORD. TI",
    "COORDENADOR DE RECURSOS HUMANOS": "COORD. RH",
    "CONTROLADOR INTERNO": "CONT. INTERNO"
}

# Criar uma coluna de "Cargo Abreviado" para usar nos gráficos
df_efetivos["Cargo Abreviado"] = df_efetivos["Cargo"].map(abreviacoes).fillna(df_efetivos["Cargo"])

# Função para criar os gráficos de efetivos e salários
def create_efetivos_figure(cargo_selecionado=None, nivel_selecionado=None):
    # Se o cargo for selecionado, buscamos a abreviação correspondente
    if cargo_selecionado:
        cargo_selecionado_abrev = abreviacoes.get(cargo_selecionado, cargo_selecionado)  # Verifica se tem abreviação, se não, usa o nome completo
    else:
        cargo_selecionado_abrev = None

    # Agrupar os dados por 'Cargo Abreviado' e 'Nível' para calcular a quantidade de efetivos e salários
    df_grouped = df_efetivos.groupby(['Cargo Abreviado', 'Nível'])[['Quantidade', 'Salário Base', 'Salário Base Total']].sum().reset_index()

    # Aplicar os filtros
    if cargo_selecionado_abrev:
        df_grouped = df_grouped[df_grouped['Cargo Abreviado'] == cargo_selecionado_abrev]
    if nivel_selecionado:
        df_grouped = df_grouped[df_grouped['Nível'] == nivel_selecionado]

    # Criar o gráfico de barras vertical para Salário Base e Salário Base Total (Figura 1)
    fig1_efetivos = px.bar(
        df_grouped,
        x='Cargo Abreviado',
        y='Quantidade',  # Mantido vertical
        color='Nível',
        title="Quantidade de Efetivos por Cargo e Nível",
        labels={'Quantidade': 'Quantidade de Efetivos'},
        color_discrete_sequence=px.colors.qualitative.Set2,
        barmode='group'
    )

    # Ajuste para diminuir o tamanho dos nomes dos níveis na lateral do gráfico
    fig1_efetivos.update_layout(
        yaxis=dict(
            tickfont=dict(size=10)  # Ajuste o tamanho da fonte para 10 (ou qualquer valor desejado)
        )
    )

    # Reshaping dos dados para gráficos de Salário Base e Salário Base Total (Figura 2)
    df_melted = pd.melt(df_grouped, id_vars=['Cargo Abreviado', 'Nível'], value_vars=['Salário Base', 'Salário Base Total'], 
                        var_name='Tipo de Salário', value_name='Valor')

    fig2_efetivos = px.bar(
        df_melted,
        x='Cargo Abreviado',
        y='Valor',  # Mantido vertical
        color='Tipo de Salário',
        title="Salário Base e Salário Base Total por Cargo e Nível",
        labels={'Valor': 'Salário', 'Tipo de Salário': 'Tipo de Salário'},
        color_discrete_sequence=px.colors.qualitative.Set2,
        barmode='group'
    )

    fig2_efetivos.update_layout(
        yaxis=dict(
            tickfont=dict(size=10)  # Ajuste o tamanho da fonte para 10 (ou qualquer valor desejado)
        )
    )

    # A mesma atualização de layout se aplica aos outros gráficos
    salary_categories = [
        'Quinquênio', 'Vencimento Complementar', 'Periculosidade', 'Horas Extras 50%', 'Horas Extras 100%',
        'Fiscal I', 'Diária', 'Estabilidade Econômica'
    ]
    df_categories = df_efetivos.groupby(['Cargo Abreviado', 'Nível'])[salary_categories].sum().reset_index()

    if cargo_selecionado_abrev:
        df_categories = df_categories[df_categories['Cargo Abreviado'] == cargo_selecionado_abrev]
    if nivel_selecionado:
        df_categories = df_categories[df_categories['Nível'] == nivel_selecionado]

    df_categories_melted = pd.melt(df_categories, id_vars=['Cargo Abreviado', 'Nível'], value_vars=salary_categories,
                                   var_name='Categoria', value_name='Valor')

    excluded_categories = [
        'Incentivo Nível Superior', 'Incentivo De Pós-Graduação', 'Incentivo - Nível Médio',
        'Fg 01: Integrante De Comissao', 'Fg 03: Comissões: Pres., Sec.', 'Fg 04: Servicos De Apoio / Sup',
        'Fg 05: Serv. Contante Locomoca', 'Fg 06: Atividades Supervisão', 'Fg 09: Fiscal De Contratos',
        'Fg 10: Serv. Externo', 'Aprimoramento Profissional', 'GCET', 'GAEL-EAP',
        'GAEL - GESTOR DE CONTRATOS', 'GAEL - AGENTE DE CONTRATACAO'
    ]

    fig3_data = [col for col in salary_categories if col not in excluded_categories]
    df_categories_melted_filtered = df_categories_melted[df_categories_melted['Categoria'].isin(fig3_data)]

    fig3_efetivos = px.bar(
        df_categories_melted_filtered,
        x='Cargo Abreviado',
        y='Valor',  # Mantido vertical
        color='Categoria',
        title="Valores das Categorias por Cargo e Nível",
        labels={'Valor': 'Valor da Categoria', 'Categoria': 'Categoria'},
        color_discrete_sequence=px.colors.qualitative.Set2,
        barmode='group'
    )

    fig3_efetivos.update_layout(
        yaxis=dict(
            tickfont=dict(size=10)  # Ajuste o tamanho da fonte para 10 (ou qualquer valor desejado)
        )
    )

    # Filtro para Incentivos
    incentivo_cols = ['Incentivo Nível Superior', 'Incentivo De Pós-Graduação', 'Incentivo - Nível Médio']
    df_incentivos = df_efetivos.groupby(['Cargo Abreviado', 'Nível'])[incentivo_cols].sum().reset_index()

    if cargo_selecionado_abrev:
        df_incentivos = df_incentivos[df_incentivos['Cargo Abreviado'] == cargo_selecionado_abrev]
    if nivel_selecionado:
        df_incentivos = df_incentivos[df_incentivos['Nível'] == nivel_selecionado]

    df_incentivos_melted = pd.melt(df_incentivos, id_vars=['Cargo Abreviado', 'Nível'], value_vars=incentivo_cols, 
                                   var_name='Tipo de Incentivo', value_name='Valor Total')

    fig4_efetivos = px.bar(
        df_incentivos_melted,
        x='Cargo Abreviado',
        y='Valor Total',  # Mantido vertical
        color='Tipo de Incentivo',
        title="Total de Incentivos por Cargo e Nível",
        labels={'Valor Total': 'Valor (R$)', 'Tipo de Incentivo': 'Tipo de Incentivo'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig4_efetivos.update_layout(
        yaxis=dict(
            tickfont=dict(size=10)  # Ajuste o tamanho da fonte para 10 (ou qualquer valor desejado)
        )
    )

    # Filtro para Categorias Especiais
    special_categories = [
        'Aprimoramento Profissional', 'GCET', 'GAEL-EAP',
        'GAEL - GESTOR DE CONTRATOS', 'GAEL - AGENTE DE CONTRATACAO'
    ]
    df_special_categories = df_efetivos.groupby(['Cargo Abreviado', 'Nível'])[special_categories].sum().reset_index()

    if cargo_selecionado_abrev:
        df_special_categories = df_special_categories[df_special_categories['Cargo Abreviado'] == cargo_selecionado_abrev]
    if nivel_selecionado:
        df_special_categories = df_special_categories[df_special_categories['Nível'] == nivel_selecionado]

    df_special_categories_melted = pd.melt(df_special_categories, id_vars=['Cargo Abreviado', 'Nível'], value_vars=special_categories,
                                           var_name='Categoria', value_name='Valor')

    fig5_efetivos = px.bar(
        df_special_categories_melted,
        x='Cargo Abreviado',
        y='Valor',  # Mantido vertical
        color='Categoria',
        title="Valores de Categorias Especiais por Cargo e Nível",
        labels={'Valor': 'Valor da Categoria', 'Categoria': 'Categoria Especial'},
        color_discrete_sequence=px.colors.qualitative.Set2,
        barmode='group'
    )

    fig5_efetivos.update_layout(
        yaxis=dict(
            tickfont=dict(size=10)  # Ajuste o tamanho da fonte para 10 (ou qualquer valor desejado)
        )
    )

    # Filtro para Comissões
    fg_categories = [
        'Fg 01: Integrante De Comissao', 'Fg 03: Comissões: Pres., Sec.',
        'Fg 04: Servicos De Apoio / Sup', 'Fg 05: Serv. Contante Locomoca',
        'Fg 06: Atividades Supervisão', 'Fg 09: Fiscal De Contratos', 'Fg 10: Serv. Externo'
    ]
    df_fg_categories = df_efetivos.groupby(['Cargo Abreviado', 'Nível'])[fg_categories].sum().reset_index()

    if cargo_selecionado_abrev:
        df_fg_categories = df_fg_categories[df_fg_categories['Cargo Abreviado'] == cargo_selecionado_abrev]
    if nivel_selecionado:
        df_fg_categories = df_fg_categories[df_fg_categories['Nível'] == nivel_selecionado]

    df_fg_categories_melted = pd.melt(df_fg_categories, id_vars=['Cargo Abreviado', 'Nível'], value_vars=fg_categories,
                                      var_name='Categoria', value_name='Valor')

    fig6_efetivos = px.bar(
        df_fg_categories_melted,
        x='Cargo Abreviado',
        y='Valor',  # Mantido vertical
        color='Categoria',
        title="Valores de Fg (Comissões e Outros) por Cargo e Nível",
        labels={'Valor': 'Valor da Categoria', 'Categoria': 'Categoria Fg'},
        color_discrete_sequence=px.colors.qualitative.Set2,
        barmode='group'
    )

    fig6_efetivos.update_layout(
        yaxis=dict(
            tickfont=dict(size=10)  # Ajuste o tamanho da fonte para 10 (ou qualquer valor desejado)
        )
    )

    return fig1_efetivos, fig2_efetivos, fig3_efetivos, fig4_efetivos, fig5_efetivos, fig6_efetivos

# Layout com os dropdowns para Cargo e Nível (aplicando style para redução do tamanho)
efetivos_layout = dbc.Row([
    dbc.Col([ 
        html.H1("Efetivos - Gráficos de Quantidade, Salário Base, Total e Categorias",
                style={'text-align': 'center', 'font-size': '22px', 'margin-bottom': '20px'}),

        # Dropdowns lado a lado
        dbc.Row([
            dbc.Col([ 
                dcc.Dropdown(
                    id='dropdown-cargo',
                    options=[{'label': c, 'value': c} for c in df_efetivos['Cargo'].unique()],
                    placeholder="Selecione um Cargo",
                    style={'margin-bottom': '10px'}
                )
            ], width=6),
            dbc.Col([ 
                dcc.Dropdown(
                    id='dropdown-nivel',
                    options=[{'label': n, 'value': n} for n in df_efetivos['Nível'].unique()],
                    placeholder="Selecione um Nível",
                    style={'margin-bottom': '10px'}
                )
            ], width=6)
        ]),

        # Gráficos em cards separados
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([ 
                dcc.Graph(id='fig1_efetivos', style={'height': '400px', 'width': '100%', 'padding': '0'})
            ])), width=12),

            dbc.Col(dbc.Card(dbc.CardBody([ 
                dcc.Graph(id='fig2_efetivos', style={'height': '400px', 'width': '100%', 'padding': '0'})
            ])), width=12),

            dbc.Col(dbc.Card(dbc.CardBody([ 
                dcc.Graph(id='fig3_efetivos', style={'height': '400px', 'width': '100%', 'padding': '0'})
            ])), width=12),

            dbc.Col(dbc.Card(dbc.CardBody([ 
                dcc.Graph(id='fig4_efetivos', style={'height': '400px', 'width': '100%', 'padding': '0'})
            ])), width=12),

            dbc.Col(dbc.Card(dbc.CardBody([ 
                dcc.Graph(id='fig5_efetivos', style={'height': '400px', 'width': '100%', 'padding': '0'})
            ])), width=12),

            dbc.Col(dbc.Card(dbc.CardBody([ 
                dcc.Graph(id='fig6_efetivos', style={'height': '400px', 'width': '100%', 'padding': '0'})
            ])), width=12),
        ])
    ])
])
