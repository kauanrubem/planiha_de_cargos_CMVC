from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd  # Para manipulação dos dados
import dash_bootstrap_components as dbc

# Carregar os dados da planilha fora da função para ser acessível globalmente
file_path = 'dataset/Planilha de cargos - CMVC.xlsx'  # Caminho do arquivo carregado
df_comissionados = pd.read_excel(file_path, sheet_name='Comissionados')  # Carregar dados da planilha

# Função para criar os gráficos de comissionados e salários
def create_comissionados_figure(cargo_selecionado=None, nivel_selecionado=None):
    # Agrupar os dados por 'Cargo' e 'Nível' para calcular a quantidade de comissionados e salários
    df_grouped = df_comissionados.groupby(['Cargo', 'Nível'])[['Quantidade', 'Salário Base', 'Salário Base Total']].sum().reset_index()

    # Se forem fornecidos filtros, aplicar a filtragem
    if cargo_selecionado:
        df_grouped = df_grouped[df_grouped['Cargo'] == cargo_selecionado]
    if nivel_selecionado:
        df_grouped = df_grouped[df_grouped['Nível'] == nivel_selecionado]

    # Criar o gráfico de barras para Salário Base e Salário Base Total (Figura 1)
    fig1_comissionados = px.bar(
        df_grouped,
        x='Cargo',
        y='Quantidade',
        color='Nível',
        title="Quantidade de Comissionados por Cargo e Nível",
        labels={'Quantidade': 'Quantidade de Comissionados'},
        color_discrete_sequence=px.colors.qualitative.Set2,
        barmode='group'  # Barra lado a lado para Cargo e Nível
    )

    # Reshaping dos dados para gráficos de Salário Base e Salário Base Total (Figura 2)
    df_melted = pd.melt(df_grouped, id_vars=['Cargo', 'Nível'], value_vars=['Salário Base', 'Salário Base Total'], 
                        var_name='Tipo de Salário', value_name='Valor')

    # Criar o gráfico de barras para Salário Base e Salário Base Total (Figura 2)
    fig2_comissionados = px.bar(
        df_melted,
        x='Cargo',
        y='Valor',  # Usando o valor das duas colunas empilhadas
        color='Tipo de Salário',
        title="Salário Base e Salário Base Total por Cargo e Nível",
        labels={'Valor': 'Salário', 'Tipo de Salário': 'Tipo de Salário'},
        color_discrete_sequence=px.colors.qualitative.Set2,  # 4 cores para 'Tipo de Salário'
        barmode='group'  # Barra lado a lado para Salário Base e Salário Base Total
    )

    # Adiciona o gráfico para as novas categorias (Incentivos, Diárias, Retroativo, GCET, GAEL-EAP, etc.)
    salary_categories = [
        'Incentivo Nível Superior', 'Incentivo De Pós-Graduação', 'Incentivo - Nível Médio', 'Diária', 
        'Retroativo De Graduação/Pós', 'GCET', 'GAEL-EAP'  # Adicionando as novas categorias
    ]

    # Agrupar os dados para essas categorias
    df_categories = df_comissionados.groupby(['Cargo', 'Nível'])[salary_categories].sum().reset_index()

    # Filtrando com base nos dropdowns
    if cargo_selecionado:
        df_categories = df_categories[df_categories['Cargo'] == cargo_selecionado]
    if nivel_selecionado:
        df_categories = df_categories[df_categories['Nível'] == nivel_selecionado]

    # Transformar as colunas de salários em formato long (long format)
    df_categories_melted = pd.melt(df_categories, id_vars=['Cargo', 'Nível'], value_vars=salary_categories,
                                    var_name='Categoria', value_name='Valor')

    # Criar o gráfico de barras para as categorias restantes
    fig3_comissionados = px.bar(
        df_categories_melted,
        x='Cargo',
        y='Valor',
        color='Categoria',
        title="Valores das Categorias por Cargo e Nível",
        labels={'Valor': 'Valor da Categoria', 'Categoria': 'Categoria'},
        color_discrete_sequence=px.colors.qualitative.Set2,  # 4 cores para as categorias
        barmode='group'  # Barra lado a lado para as categorias
    )

    # Novo gráfico para Fg 03: Comissões: Pres., Sec. e Diária
    fg_diaria_categories = ['Fg 03: Comissões: Pres., Sec.', 'Diária']  # Novas categorias adicionadas

    # Agrupar os dados para Fg 03 e Diária
    df_fg_diaria = df_comissionados.groupby(['Cargo', 'Nível'])[fg_diaria_categories].sum().reset_index()

    # Filtrando com base nos dropdowns
    if cargo_selecionado:
        df_fg_diaria = df_fg_diaria[df_fg_diaria['Cargo'] == cargo_selecionado]
    if nivel_selecionado:
        df_fg_diaria = df_fg_diaria[df_fg_diaria['Nível'] == nivel_selecionado]

    # Transformar os dados para long format
    df_fg_diaria_melted = pd.melt(df_fg_diaria, id_vars=['Cargo', 'Nível'], value_vars=fg_diaria_categories,
                                  var_name='Categoria', value_name='Valor')

    # Criar o gráfico de barras para Fg 03 e Diária
    fig4_comissionados = px.bar(
        df_fg_diaria_melted,
        x='Cargo',
        y='Valor',
        color='Categoria',
        title="Valores de Fg 03: Comissões: Pres., Sec. e Diária por Cargo e Nível",
        labels={'Valor': 'Valor da Categoria', 'Categoria': 'Categoria'},
        color_discrete_sequence=px.colors.qualitative.Set2,  # Cores para Fg 03 e Diária
        barmode='group'  # Barra lado a lado para as categorias
    )

    return fig1_comissionados, fig2_comissionados, fig3_comissionados, fig4_comissionados


# Layout com gráficos em cards separados
comissionados_layout = dbc.Row([
    dbc.Col([  
        html.H1("Comissionados - Gráficos de Quantidade, Salário Base, Salário Base Total e Categorias", 
                style={'font-size': '24px', 'text-align': 'center', 'margin-bottom': '20px'}), 

        # Dropdowns lado a lado
        dbc.Row([ 
            dbc.Col([  
                dcc.Dropdown(
                    id='dropdown-cargo',
                    options=[{'label': cargo, 'value': cargo} for cargo in df_comissionados['Cargo'].unique()],
                    placeholder="Selecione um Cargo",
                    value='ASSESSOR PARLAMENTAR',
                    style={'margin-bottom': '10px'}
                ),
            ], width=6),

            dbc.Col([  
                dcc.Dropdown(
                    id='dropdown-nivel',    
                    options=[{'label': nivel, 'value': nivel} for nivel in df_comissionados['Nível'].unique()],
                    placeholder="Selecione um Nível",
                    style={'margin-bottom': '10px'}
                ),
            ], width=6),  
        ]),

        # Gráficos em cards separados com o estilo igual ao de efetivos.py
        dbc.Row([  
            dbc.Col(dbc.Card(dbc.CardBody([ 
                dcc.Graph(id='fig1_comissionados', style={'height': '400px', 'width': '100%', 'padding': '0'})
            ])), width=12),

            dbc.Col(dbc.Card(dbc.CardBody([ 
                dcc.Graph(id='fig2_comissionados', style={'height': '400px', 'width': '100%', 'padding': '0'})
            ])), width=12),

            dbc.Col(dbc.Card(dbc.CardBody([ 
                dcc.Graph(id='fig3_comissionados', style={'height': '400px', 'width': '100%', 'padding': '0'})
            ])), width=12),

            dbc.Col(dbc.Card(dbc.CardBody([ 
                dcc.Graph(id='fig4_comissionados', style={'height': '400px', 'width': '100%', 'padding': '0'})
            ])), width=12),
        ])
    ], sm=12, md=12) 
])


