#import libraries
import base64
import datetime
import io
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import plotly.graph_objs as go
from api_dat import read_api
import pandas as pd
import pickle

#Link to external stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Create dictionary of colors to be called later
colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

#Load Saved Model
model = pickle.load(open('model_solar.pkl','rb'))
model1 = pickle.load(open('model_wind.pkl','rb'))

#HTML Layout
app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Plant Maintenance Schedule File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': 'auto'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),dcc.Graph(id='Mygraph'),
    dcc.Graph(id='Mygraph1'),
],style={'height':'20px','width':'60%','margin-left':'auto',
'margin-right':'auto','margin-top': 'auto','margin-bottom': 'auto'})

#Parsing uploaded maintenance files
def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assuming that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))


        elif 'xls' in filename:
            # Assuming that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'Wrong Filetype For Maintenance File'
        ])
    return df


#Callback for chart 1
@app.callback(Output('Mygraph', 'figure'),
            [
                Input('upload-data', 'contents'),
                Input('upload-data', 'filename')
            ])
#create Function for Solar Predictions
def update_graph(contents, filename):
    fig = {
        'layout': go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"])
    }

    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)

        #read from weather API module
        data1,data2=read_api()
        sol_data=data1
        prediction_sol = model.predict(sol_data)

        #Dataframe Processing
        sol_data["predicted_output(MW)"]=pd.Series(prediction_sol)

        maint=df.rename(columns={"Date Of Month":"Day"})

        df_sol_final=pd.merge(sol_data, maint,how='left').fillna(100)
        df_sol_final['predicted_output(MW)']=(df_sol_final['Capacity Available']/100)*df_sol_final['predicted_output(MW)']
                    
        df_sol_final=df_sol_final[['Month','Day','predicted_output(MW)']]

        df_sol_final['predicted_output(MW)']=round(df_sol_final['predicted_output(MW)'],2)

        #Plot Line graph
        fig = px.line(df_sol_final, x=df_sol_final.index ,y="predicted_output(MW)",template="plotly_dark",
        title="Malpas-Trenton Solar Farm Output 7 Day Forecast",
        labels={"index": "Day of Forecast"})

        dcc.Graph(figure=fig)
 
    return fig

#create Function for Wind Predictions
@app.callback(Output('Mygraph1', 'figure'),
            [
                Input('upload-data', 'contents'),
                Input('upload-data', 'filename')
            ])
def update_graph1(contents, filename):
    fig1 = {
        'layout': go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"])
    }

    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        #read from weather API module
        data1,data2=read_api()
       
        wind_data=data2
        prediction_wind = model1.predict(wind_data)

        #Dataframe Processing
        wind_data["predicted_output(MW)"]=pd.Series(prediction_wind)

        maint=df.rename(columns={"Date Of Month":"Day"})
        df_wind_final=pd.merge(wind_data, maint,how='left').fillna(100)
        df_wind_final['predicted_output(MW)']=(df_wind_final['Capacity Available']/100)*df_wind_final['predicted_output(MW)']
        df_wind_final=df_wind_final[['Month','Day','predicted_output(MW)']]

        
        df_wind_final['predicted_output(MW)']=round(df_wind_final['predicted_output(MW)'],2)

        #Plot Line graph
        fig1 = px.line(df_wind_final, x=df_wind_final.index ,y="predicted_output(MW)",template="plotly_dark",
        title="Klushof Wind Farm Output 7 Day Forecast",
        labels={"index": "Day of Forecast"})

        dcc.Graph(figure=fig1)
    
    return fig1



if __name__ == '__main__':
    app.run_server(debug=True)
