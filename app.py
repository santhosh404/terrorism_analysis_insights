import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objects as go
from dash.dependencies import Input, Output
import plotly.express as px
from dash.exceptions import PreventUpdate


# Creating a class (Dash) and declared it globally..
app = dash.Dash()
server = app.server
#Defining the Loading Data
def load_data():
    dataset_name = 'global_terror.csv'
    
    global df
    df = pd.read_csv(dataset_name)
    global month_list 
    month = {
        
        "January"  : 1,
        "February" : 2,
        "March"    : 3,
        "April"    : 4,
        "May"      : 5,
        "June"     : 6,
        "July"     : 7,
        "Augest"   : 8,
        "September": 9,
        "Octobar"  : 10,
        "November" : 11,
        "December" : 12
        }
        
    
    month_list = [{'label' : key, 'value' : value} for key, value in month.items()]
    
    global date_list
    date_list = [x for x in range(1, 32)]
    
    
    global region_list
    region_list = [{'label' : str(i), 'value' : str(i)} for i in sorted(df['region_txt'].astype(str).unique().tolist() )]
    
    global country_list
    country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()
    
    global state_list
    state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()
    
    global city_list
    city_list = df.groupby("provstate")["city"].unique().apply(list).to_dict()
    
    global attack_type_list
    attack_type_list = [{'label' : str(i), 'value' : str(i)} for i in sorted(df['attacktype1_txt'].astype(str).unique().tolist())]
    
    
    global year_list
    
    year_list = sorted( df['iyear'].unique().tolist())
     
    global year_dict
     
    year_dict = { str(year) : str(year) for year in year_list}
    
    global chart_dropdown_values 
    chart_dropdown_values = {"Terrorist Organization" : 'gname',
                             "Target Nationality" :"natlty1_txt",
                             "Target Type" : "targtype1_txt",
                             "Type of Attack" : "attacktype1_txt",
                             "Weapon Type" : "weaptype1_txt",
                             "Region" : "region_txt",
                             "Country Attacked" : "country_txt"
                             }
    chart_dropdown_values = [{"label" : keys, "value" : values} for keys, values in chart_dropdown_values.items()]
    
    
 
    
    
# Creating the Interface of my app ie..UI    
    
def create_app_ui():


    main_layout = html.Div([ 
        
    
    html.Br(),
    html.H1(children = 'Terrorism Analysis with Insights', id = 'main_title', style = {"textAlign" : "center","background-color": "coral"}),
    html.Br(),
    dcc.Tabs(id = "Tabs", value = "Map",children = [
                dcc.Tab(label = "Map Tool", id = "Map Tool",value="Map", children = [
                dcc.Tabs(id = "subtabs", value = "WorldMap", children = [
                dcc.Tab(label = "World Map Tool", id = "World",value = "WorldMap"),
                dcc.Tab(label = "India Map Tool", id = "India",value = "IndiaMap")
      ]),
                      dcc.Dropdown(id = 'month_dropdown',
                     options = month_list , 
                     placeholder = 'Select Month', 
                     multi =True),
                        
                     dcc.Dropdown(id = 'date_dropdown',
                     placeholder = "Select Date", 
                     multi = True),
      
                     dcc.Dropdown(id = 'region_dropdown',
                     options = region_list,
                     placeholder = "Select Region",  
                     multi = True),
      
                     dcc.Dropdown(id = 'country_dropdown',
                     options = [{'label' : "All", 'value' : "All"}], 
                     placeholder="Select a Country", 
                     multi = True),
       
                     dcc.Dropdown(id = 'state_dropdown',
                     options = [{'label' : 'All', 'value' : 'All'}],
                     placeholder = "Select a State",  
                     multi = True),
       
                     dcc.Dropdown(id = 'city_dropdown',
                     options = [{'label' : 'All', 'value' : 'All'}], 
                     placeholder = "Select a City",  
                     multi = True),
    
                     dcc.Dropdown(id = 'attacktype_dropdown',
                     options = attack_type_list, 
                     placeholder = "Select a Attack Type", 
                     multi = True),
   
            
   
        html.H3("Select Year from the slider below.."),
        dcc.RangeSlider(
            
            id = 'year_slider',
            min = min(year_list),
            max = max(year_list),
            value = [min(year_list), max(year_list)],
            marks = year_dict,
            step = None
            
            
            ),

       html.Br(),
       ]),
    dcc.Tab(label = "Chart Tool", id = "chart tool", value = "Chart", children = [
                dcc.Tabs(id = "subtabs2",value = "WorldChart", children = [
                dcc.Tab(label = "World Chart Tool", id = "WorldC", value = "WorldChart"),
                dcc.Tab(label = "India Chart Tool", id = "IndiaC", value = "IndiaChart")]),
                html.Br(),
                html.Br(),
                dcc.Dropdown(id = "Chart_Dropdown", options = chart_dropdown_values, placeholder = "Select Option", value = "region_txt"),
               html.Br(),
               html.Br(),
             
               dcc.Input(id = "search", placeholder = "Search Filter"),
               html.Br(),
               html.Br(),
               html.Hr(style = {"border" : "1 px solid black"}),
               html.Br(),
               dcc.RangeSlider(
                       id = "cyear_slider",
                       min = min(year_list),
                       max = max(year_list),
                       value = (min(year_list), max(year_list)),
                       marks = year_dict,
                       step = None
                       ),
             html.Br()
             ]),
    ]),
     
    html.Div(id = "graph-object", children = "Graph will shown Here....")
],style = {"background-color": "coral"})
            
    return main_layout


# Call Back mechanism..


@app.callback(
    
    dash.dependencies.Output('graph-object', 'children'),
    [dash.dependencies.Input('month_dropdown', 'value'),
     dash.dependencies.Input('date_dropdown', 'value'),
     dash.dependencies.Input('region_dropdown', 'value'),
     dash.dependencies.Input('country_dropdown', 'value'),
     dash.dependencies.Input('state_dropdown', 'value'),
     dash.dependencies.Input('city_dropdown', 'value'),
     dash.dependencies.Input('attacktype_dropdown', 'value'),
     dash.dependencies.Input('year_slider', 'value'),
     dash.dependencies.Input("Tabs", "value"),
     dash.dependencies.Input("cyear_slider", "value"),
     dash.dependencies.Input("Chart_Dropdown", "value"),
     dash.dependencies.Input("search", "value"),
     dash.dependencies.Input("subtabs2", "value")
    ]   
    )     

def update_app_ui(month_value, date_value, region_value, country_value, state_value, city_value, attacktype_value, year_value, Tabs, chart_year_selector, chart_dp_value, search, subtabs2):
    fig = None
    
    if Tabs == "Map":
        print("Data Type of Month = ", str(type(month_value)))
        print("Data of the Month = ", month_value)
    
        print("Data Type of Day = ", str(type(date_value)))
        print("Data of the Day = ", date_value)
    
    
        print("Data Type of Region = ", str(type(region_value)))
        print("Data of the Region = ", region_value)
    
    
        print("Data Type of Country = ", str(type(country_value)))
        print("Data of the Country = ", country_value)
        
    
        print("Data Type of State = ", str(type(state_value)))
        print("Data of the State = ", state_value)
        
    
        print("Data Type of City = ", str(type(city_value)))
        print("Data of the City = ", city_value)
    
        print("Data Type of Attack_Type = ", str(type(attacktype_value)))
        print("Data of the Attack_Type = ", attacktype_value)
    
    
        print("Data Type of Year = ", str(type(year_value)))
        print("Data of the Year = ", year_value)
    
        
    
        # Year Filter
        year_range = range(year_value[0], year_value[1] + 1)
        new_df = df[df["iyear"].isin(year_range)]
    
    
        # Month Filter
    
        if month_value == [] or month_value is None:
            pass
        else:
            if (date_value == [] or date_value is None):
                new_df = new_df[new_df["imonth"].isin(month_value)]
            else:
                new_df = new_df[(new_df["imonth"].isin(month_value)) & (new_df["iday"].isin(date_value))]
    
        #  Region, Country, State, City Filter.
        if region_value == [] or region_value is None:
            pass
        else:
            if country_value == [] or country_value is None:
                new_df = new_df[new_df["region_txt"].isin(region_value)]
            else:
                if state_value == [] or state_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value)) & 
                                (new_df["country_txt"].isin(country_value))]
                else:
                    if city_value == [] or city_value is None:
                            new_df = new_df[(new_df["region_txt"].isin(region_value)) & 
                                    (new_df["country_txt"].isin(country_value))&
                                    (new_df["provstate"].isin(state_value))]
                    else:
                        new_df = new_df[(new_df["region_txt"].isin(region_value)) & 
                                    (new_df["country_txt"].isin(country_value))&
                                    (new_df["provstate"].isin(state_value))&
                                    (new_df["city"].isin(city_value))]
                    
        if attacktype_value == [] or attacktype_value is None:
            pass
        else:
            new_df = new_df[new_df["attacktype1_txt"].isin(attacktype_value)]
        
        mapFigure = go.Figure()
        
        if new_df.shape[0]:
            pass
        else:
            new_df = pd.DataFrame(columns = ["iyear", "imonth", "iday", "country_txt", "region_txt", "provstate", "city", "latitude", "longitude", "attacktype1_txt", "nkill"])
            new_df.loc[0] = [0, 0, 0, None, None, None, None, None, None, None, None]
                
    
    
        
        # GraphObject or Figure has 2 things 1.Data 2.Layout
        mapFigure = px.scatter_mapbox(new_df,
                               lat = "latitude",
                               lon = "longitude",
                               color = "attacktype1_txt",
                               hover_data= ["region_txt", "country_txt", "provstate", "city", "attacktype1_txt", "nkill", "iyear"],
                               zoom = 1)
    
        mapFigure.update_layout(mapbox_style = "open-street-map",
                        autosize = True,
                        margin = dict(l=0, r=0, t=25, b=20)
                        ) 
    

        fig = mapFigure
    elif Tabs == "Chart":
        fig = None
        
        year_range_c = range(chart_year_selector[0], chart_year_selector[1]+1)
        chart_df = df[df["iyear"].isin(year_range_c)]
        
        if subtabs2 == "WorldChart":
            pass
        elif subtabs2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"] == "South Asia")&(chart_df["country_txt"] == "India")]
        if chart_dp_value is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                chart_df = chart_df[chart_df[chart_dp_value].str.contains(search, case = False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                
        if chart_df.shape[0]:
            pass
        else:
            chart_df = pd.DataFrame(columns = ["iyear", "count", chart_dp_value])
            chart_df.loc[0] = [0, 0, "No data"]
        fig = px.area(chart_df, x = "iyear", y = "count", color = chart_dp_value)
        
    return dcc.Graph(figure = fig)


@app.callback(
    
    Output("date_dropdown", "options"),
    [Input("month_dropdown", "value")],
    
    )
def update_date(month_value):
    date_list = [x for x in range(1, 32)]
    options = []
    if month_value:
        options = [{"label" : m, "value": m} for m in date_list]
    return options

@app.callback(
    
    [Output("region_dropdown", "value"),
    Output("region_dropdown", "disabled"),
    Output("country_dropdown", "value"),
    Output("country_dropdown", "disabled")],
    [Input("subtabs", "value")]
        
    )


def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    
    if tab == "WorldMap":
        pass
    elif tab == "IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c
        
@app.callback(
    
    Output("country_dropdown", "options"),
    [Input("region_dropdown", "value")]
    
    )

def set_country_options(region_value):
    options = []
    
    if region_value is None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                options.extend(country_list[var])
    return [{"label": m, "value": m} for m in options]    
@app.callback(
    
    Output("state_dropdown", "options"),
    [Input("country_dropdown", "value")]

    
    )  

def set_state_options(country_value):
    options = []
    
    if country_value is None:
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                options.extend(state_list[var])
    return [{"label": m, "value": m} for m in options]


@app.callback(
    
    Output("city_dropdown", "options"),
    [Input("state_dropdown", "value")]
    
    
    )

def set_city_options(state_value):
    options = []
    
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                options.extend(city_list[var])
    return [{"label" : m, "value": m} for m in options]

def main():
    print('Starting the main Function..')
    
    load_data()
    #print(df.sample(5))
    global app
    app.layout = create_app_ui()
    app.title = 'Terrorism Analysis with Insights'
    app.run_server(debug = False)
    
    df = None
    app = None

    
    print('Main Function is Ending..')
if __name__ == '__main__':
    print('My project is Starting..')
    main()
    print('My project is ending..')
