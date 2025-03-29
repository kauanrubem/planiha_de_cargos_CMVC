import dash
import dash_bootstrap_components as dbc

# Criação da instância do Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

# Expondo o servidor
server = app.server

# Definindo a configuração para servir os arquivos localmente (se necessário)
app.scripts.config.serve_locally = True
