# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

print(spacex_df.head())
print(spacex_df.columns)

launch_sites=spacex_df['Launch Site'].unique()
options=[{'label': 'All Sites', 'value': 'ALL'}]
for site in launch_sites:
    options.append({'label':site,'value':site})
print (options)


#  options=[{'label': 'All Sites', 'value': 'ALL'},{'label': 'site1', 'value': 'site1'}, ...]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=options,value='ALL'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(min=0, max=10000, step=1000,
                                value=[min_payload,max_payload],id='payload-slider'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df.groupby(['Launch Site'])['class'].sum().reset_index()
    filtered_df.columns=['Launch Site','class']

    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total success launches'
        )
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df=spacex_df[spacex_df['Launch Site']==entered_site]['class'].to_frame()
        filtered_df=filtered_df['class'].value_counts().reset_index()
        filtered_df.columns=['class','count']       
        fig = px.pie(filtered_df, values='count', 
        names='class', 
        title='Succesfull and unsuccesfull for a site')
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='payload-slider', component_property='value'),
              Input(component_id='site-dropdown', component_property='value'))
def get_scatter_chart(payload,entered_site):
    print (payload)
    print (entered_site)
    filtered_df=spacex_df[(spacex_df['Payload Mass (kg)']>=payload[0]) &
        (spacex_df['Payload Mass (kg)']<=payload[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df,x='Payload Mass (kg)', y='class',
         color='Booster Version Category'
        )
        return fig
    else:
        filtered_df=filtered_df[filtered_df['Launch Site']==entered_site]       
        fig = px.scatter(filtered_df,x='Payload Mass (kg)',y='class',
         color='Booster Version Category'
         )
        return fig



# Run the app
if __name__ == '__main__':
    app.run_server()




