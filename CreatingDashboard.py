import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

# Read the CSV files
snyk_sca_repos = pd.read_csv('Snyk-SCA-Repos.csv')
missing_from_snyk_sca = pd.read_csv('Missing_from_Snyk_SCA.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1('Snyk and Bitbucket Dashboard'),

    html.Div([
        html.H2('Snyk-SCA-Repos'),
        dash_table.DataTable(
            id='snyk-sca-repos-table',
            columns=[{"name": i, "id": i} for i in snyk_sca_repos.columns],
            data=snyk_sca_repos.to_dict('records'),
            style_cell={'textAlign': 'left'},
            style_header={
                'backgroundColor': 'lightgrey',
                'fontWeight': 'bold',
                'textAlign': 'center'
            }
        ),
    ]),

    html.Div([
        html.H2('Missing from Snyk SCA'),
        dash_table.DataTable(
            id='missing-from-snyk-sca-table',
            columns=[{"name": i, "id": i} for i in missing_from_snyk_sca.columns],
            data=missing_from_snyk_sca.to_dict('records'),
            style_cell={'textAlign': 'left'},
            style_header={
                'backgroundColor': 'lightgrey',
                'fontWeight': 'bold',
                'textAlign': 'center'
            }
        ),
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
