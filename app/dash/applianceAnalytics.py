from app import app, db, models
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from flask import render_template, render_template_string
from flask_login import current_user
from datetime import datetime as dt
from datetime import timedelta


def init_dashApp(server):

    external_stylesheets = [dbc.themes.BOOTSTRAP]

    dashAppliance = dash.Dash(
        __name__,
        server=server,
        url_base_pathname="/appliance_dash/",
        external_stylesheets=external_stylesheets,
    )


    navbar = html.Div(
        dbc.Navbar(
            [
                html.A(
                    dbc.Row(
                        [
                
                            dbc.Col(dbc.NavbarBrand("PowerPal", className="brand")),
                        ],
                        align="center",
                    ),
                    href="/",
                    style={"text-decoration": "none"},
                    
                ),
                dbc.NavbarToggler(id="navbar-toggler"),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(
                                html.A(
                                    "Appliance Usage",
                                    className="nav-link",
                                    href="/appliance_dash/",
                                )
                            ),
                            dbc.NavItem(
                                html.A(
                                    "Costs and Emissions",
                                    className="nav-link",
                                    href="/usage",
                                )
                            ),
                            dbc.NavItem(
                                html.A(
                                    "Your appliances",
                                    className="nav-link",
                                    href="/your_appliances",
                                )
                            ),
                            dbc.NavItem(
                                html.A(
                                    "Goals",
                                    className="nav-link",
                                    href="/goals",
                                )
                            ),
                            dbc.NavItem(
                                html.A(
                                    "Admin",
                                    className="nav-link",
                                    href="/admin",
                                )
                            ),
                        ],
                        navbar=True,
                        className="ml-auto",
                    ),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ],
            #color="success",
            dark=False,
            className="shadow-sm dash-navbar",
        )
        
    )

    
    dashAppliance.layout = html.Div(
        [   navbar,
            dbc.Row(html.A(
    id='twitter-share',
    href='https://twitter.com/intent/tweet?url=https://powerpal.onrender.com/appliance_dash/',
    className='btn btn-primary',
    n_clicks=0
)
),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.Button('Previous', id='prev-graph-1', n_clicks=0),
                                html.Button('Next', id='next-graph-1', n_clicks=0),
                                dcc.Graph(id="bar-graph"),
                            ]
                        ), 
                        width=6
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Button('Previous', id='prev-graph-2', n_clicks=0),
                                html.Button('Next', id='next-graph-2', n_clicks=0),
                                dcc.Graph(id="line-graph"),
                            ]
                        ), 
                        width=6
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.Button('Previous', id='prev-graph-3', n_clicks=0),
                                html.Button('Next', id='next-graph-3', n_clicks=0),
                                dcc.Graph(id="bar-cost-graph"),
                            ]
                        ), 
                        width=6
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Button('Previous', id='prev-graph-4', n_clicks=0),
                                html.Button('Next', id='next-graph-4', n_clicks=0),
                                dcc.Graph(id="pie-chart"),
                            ]
                        ), 
                        width=6
                    ),
                ]
            )
        ],
        
    )
    dashAppliance.title = "Appliance Analytics"
    init_dashAppCallback(dashAppliance)
    return dashAppliance.server


def get_appliance_data(email,start_date,end_date):

    appliances = (
        models.Appliance.query.filter_by(email=email)
        .filter(models.Appliance.dateUsedOn >= start_date)
        .filter(models.Appliance.dateUsedOn <= end_date)
        .all()
    )

    data = {
        "Appliance": [appliance.applianceName for appliance in appliances],
        "Hours_Used": [appliance.hoursPerDay for appliance in appliances],
        "Carbon_Emissions": [appliance.emissions for appliance in appliances],
        "Cost": [appliance.cost for appliance in appliances],
        "Energy": [appliance.energyUsed for appliance in appliances],
    }

    df = pd.DataFrame(data)

    df_grouped = (
        df.groupby("Appliance")
        .agg(
            {
                "Hours_Used": "sum",
                "Carbon_Emissions": "sum",
                "Cost": "sum",
                "Energy": "sum",
            }
        )
        .reset_index()
    )
    return df_grouped, start_date, end_date
    

def init_dashAppCallback(dashAppliance):

    @dashAppliance.callback(
        [
            Output('twitter-share', 'href'),
        ],
       
        Input('twitter-share', 'n_clicks')
        )
    
    def update_twitter_link(x_clicks):
        url = 'https://powerpal.onrender.com/appliance_dash/' # Replace with the URL of your app
        text = 'Check out my Dash app!' # Replace with the text to be shared
        hashtags = 'dataviz,dashboard' # Replace with the hashtags to be used
        return 'https://twitter.com/intent/tweet?url=https://powerpal.onrender.com/appliance_dash/'
    
    @dashAppliance.callback(
        [
            Output("bar-graph", "figure"),
            Output("line-graph", "figure"),
            Output("bar-cost-graph", "figure"),
            Output("pie-chart", "figure"),
            Output('twitter-share', 'href'),
        ],
        
        Input("prev-graph-1", "n_clicks"),
        Input("next-graph-1", "n_clicks"),
        Input("prev-graph-2", "n_clicks"),
        Input("next-graph-2", "n_clicks"),
        Input("prev-graph-3", "n_clicks"),
        Input("next-graph-3", "n_clicks"),    
        Input("prev-graph-4", "n_clicks"),
        Input("next-graph-4", "n_clicks"),    
        )
    
    def update_graphs(prev_clicks_1,next_clicks_1,prev_clicks_2,next_clicks_2,prev_clicks_3,next_clicks_3,prev_clicks_4,next_clicks_4):
        if current_user.is_authenticated:
            email = current_user.email
        else:
            return (
                go.Figure(),
                go.Figure(),
                go.Figure(),
                go.Figure(),
            )  # Return empty figures if the user is not logged in

        user = models.User.query.filter_by(email=email).first()
        start_date = user.dateCreated.date()
        end_date = start_date + timedelta(days=7)

        while end_date < dt.now().date():
            # Do something with the start_date and end_date

            # Update start and end dates for next iteration
            start_date = end_date + timedelta(days=1)
            end_date = start_date + timedelta(days=7)
        
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if 'prev-graph-1' in changed_id:
            start_date -= timedelta(days=7)
            end_date -= timedelta(days=7)
        elif 'next-graph-1' in changed_id:
            start_date += timedelta(days=7)
            end_date += timedelta(days=7)
        elif 'prev-graph-2' in changed_id:
            start_date -= timedelta(days=7)
            end_date -= timedelta(days=7)    
        elif 'next-graph-2' in changed_id:
            start_date += timedelta(days=7)
            end_date += timedelta(days=7)
        elif 'prev-graph-3' in changed_id:
            start_date -= timedelta(days=7)
            end_date -= timedelta(days=7)    
        elif 'next-graph-3' in changed_id:
            start_date += timedelta(days=7)
            end_date += timedelta(days=7)
        elif 'prev-graph-4' in changed_id:
            start_date -= timedelta(days=7)
            end_date -= timedelta(days=7)    
        elif 'next-graph-4' in changed_id:
            start_date += timedelta(days=7)
            end_date += timedelta(days=7)

        df, start, end = get_appliance_data(email,start_date,end_date)
        
        bar_graph = go.Figure(
        data=[
                go.Bar(
                    x=df["Appliance"],
                    y=df["Hours_Used"],
                    text=df["Hours_Used"],
                    textposition="auto",
                    hovertemplate="%{y}",
                    name="Hours Used this week",
                )
            ],
            layout=go.Layout(
                title="Appliance vs Hours Used from " + str(start) + " to " + str(end)
            ),
        )

        line_graph = go.Figure(
            data=[
                go.Scatter(
                    x=df["Appliance"],
                    y=df["Carbon_Emissions"],
                    text=df["Carbon_Emissions"],
                    textposition="top right",
                    mode="lines+markers",
                    hovertemplate="%{y}",
                    name="Carbon Emissions this week",
                )
            ],
            layout=go.Layout(
                title="Appliance vs Carbon Emissions(kgCO2e) from "
                + str(start)
                + " to "
                + str(end)
            ),
        )

        bar_cost_graph = go.Figure(
            data=[
                go.Bar(
                    x=df["Appliance"],
                    y=df["Cost"],
                    text=df["Cost"],
                    textposition="auto",
                    hovertemplate="%{y}",
                    name="Cost of usage",
                )
            ],
            layout=go.Layout(
                title="Appliance vs Cost(GBP) from " + str(start) + " to " + str(end)
            ),
        )

        pie_chart = go.Figure(
            data=[
                go.Pie(
                    labels=df["Appliance"],
                    values=df["Energy"],
                    hovertemplate="%{label}: %{value:.2f} kWh",
                    name="Energy consumption",
                )
            ],
            layout=go.Layout(title="Energy Consumption(kwH) by Appliance from " + str(start) + " to " + str(end)),
        )
        return bar_graph, line_graph, bar_cost_graph, pie_chart
