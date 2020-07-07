# -*- coding: utf-8 -*-
"""
Created on 07072020 10:38

@author: Azemar David
"""
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State, MATCH, ALL
import dash_bootstrap_components as dbc
import dash_table 
from dash.exceptions import PreventUpdate
from dash_table import DataTable
from sqlalchemy import create_engine
import sqlite3

import pandas as pd
import base64
import numpy as np
import math
import io
import json
from pandas.io.json import json_normalize
import time
from datetime import datetime

import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
from plotly.subplots import make_subplots


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],meta_tags=[{"name": "viewport", "content": "width=device-width"}])
app.config.suppress_callback_exceptions = True
server = app.server

VALID_USERNAME_PASSWORD_PAIRS = {
    'tsc@supplier_scorecard': 'tsc@456123789'
}

auth = dash_auth.BasicAuth(
   app,
   VALID_USERNAME_PASSWORD_PAIRS
)

##############################################
################ data ########################
##############################################


data1 = pd.read_csv("assets/data_final_report.csv", delimiter=",",decimal=".",encoding = "ISO-8859-1",engine='python')
#list for dropdown

# list_cat=data1['CAT_NAME'].unique()
# list_cat=np.sort(list_cat)
# list_cat2=[{'label':x.replace(', Category', ''), 'value': x} for x in list_cat]
# list_all={'All':'All'}
# list_cat3=[{'label':x.replace(', Category', ''), 'value': x} for x in list_cat]

# list_dep=data1['DEPT_NAME'].unique()
# list_dep=np.sort(list_dep)
# list_cat4=[{'label':x.replace(', Category', ''), 'value': x} for x in list_dep]

# list_store=data1['STORE_NAME'].unique()
# list_store=np.sort(list_store)
# list_store2=[{'label':x.replace(', Category', ''), 'value': x} for x in list_store]
# list_store=[{'label':'All','value':'All'}]+[{'label':x.replace(', Category', ''), 'value': x} for x in list_store]

list_supp=data1['PRIMARY_SUPP'].unique()
list_supp=np.sort(list_supp)
list_supp=[{'label':'None','value':'None'}]+[{'label':x.replace(', Category', ''), 'value': x} for x in list_supp]



#############################################
#####   figures  ############################
#############################################

fig_1=dcc.Graph(id='chart_1')
fig_2=dcc.Graph(id='chart_2')
fig_3=dcc.Graph(id='chart_3')
fig_4=dcc.Graph(id='chart_4')
fig_5=dcc.Graph(id='chart_5')
fig_6=dcc.Graph(id='chart_6')
fig_7=dcc.Graph(id='chart_7')
fig_8=dcc.Graph(id='chart_8')
fig_9=dcc.Graph(id='chart_9')
fig_10=dcc.Graph(id='chart_10')

fig_12=dash_table.DataTable(id='table_1',
                            # export_columns='all',
                            sort_mode="multi",
                            sort_action="native",                            
                            # export_format='csv',
                            # export_headers='names',
                            #style_as_list_view=True,
                            page_current=0,
                            page_size=15,
							style_header={
                                        'backgroundColor': '#00224e',
									    'color': 'white',			  
										'fontWeight': 'bold',
                                        'fontSize':14,
                                        'font-family':'sans-serif'},
							style_cell={'textAlign': 'left',
                                        'fontSize':12,
                                        'backgroundColor': 'white',
                                        'color': 'black',
                                        'font-family':'sans-serif'},
                            style_data_conditional=[
                                        {'if': {
                                                 'filter_query': '{Cat R/H%} < 0',
                                                 'column_id': 'Cat R/H%'
                                               },
                                         'color': 'red'
                                        },                            
                                       {'if': {
                                                 'filter_query': '{Sales R/H %} < 0',
                                                 'column_id': 'Sales R/H %'
                                               },
                                         'color': 'red'
                                        }, 
                                       {'if': {
                                                 'filter_query': '{Cat R/H%} < 0',
                                                 'column_id': 'Cat R/H%'
                                               },
                                         'color': 'red'
                                        }, 
                                       {'if': {
                                                 'filter_query': '{Wt (R-H)} < 0',
                                                 'column_id': 'Wt (R-H)'
                                               },
                                         'color': 'red'
                                        }, 
                                       {'if': {
                                                 'filter_query': '{Cat R/H%} < 0',
                                                 'column_id': 'Cat R/H%'
                                               },
                                         'color': 'red'
                                        }, 
                                       {'if': {
                                                 'filter_query': '{Gain GP} < 0',
                                                 'column_id': 'Gain GP'
                                               },
                                         'color': 'red'
                                        },
                                       {'if': {
                                                 'filter_query': '{GP Y} < 0',
                                                 'column_id': 'GP Y'
                                               },
                                         'color': 'red'
                                        }, 
                                       {'if': {
                                                 'filter_query': '{GP%} < 0',
                                                 'column_id': 'GP%'
                                               },
                                         'color': 'red'
                                        }, 
                                       {'if': {
                                                 'filter_query': '{Category GP%} < 0',
                                                 'column_id': 'Category GP%'
                                               },
                                         'color': 'red'
                                        }                                                                                                                                                                                                                                                                                                                      
                                        ]                            
                            )




#############################################
#####   callback ############################
#############################################

@app.callback(
    Output('collapse4', 'style'),
    [Input('sup1', 'value')])
def hide_report(sup):
    if str(sup)=="None":
        return {'display':'none'}
    else:
        return {'display':'block'}    


@app.callback(
    [Output('table_1', 'columns'),
     Output('table_1', 'data')],
    [Input('sup1', 'value')])
def update_report(sup):

    t = pd.pivot_table(data1[data1['PRIMARY_SUPP']==str(sup)],
                  index=['CAT_NAME'],
                  values=['COST_ly', 'COST_y', 'GP_ly', 'GP_y', 'SALES_ly', 'SALES_y',
                          'UNITS_ly', 'UNITS_y'],
                  aggfunc='sum',margins=True 
                  ).reset_index()

    t['sales_growth%']=(t['SALES_y']/t['SALES_ly']-1)*100
    t['units_growth%']=(t['UNITS_y']/t['UNITS_ly']-1)*100
    t['cost_growth%']=(t['COST_y']/t['COST_ly']-1)*100
    t['GP_growth%']=(t['GP_y']/t['GP_ly']-1)*100
    t['GP%']=(t['GP_y']/t['SALES_y'])*100
    t['GP2%']=(t['GP_ly']/t['SALES_ly'])*100
    t['Gain_GP']=t['GP%']-t['GP2%']


    t2 = pd.pivot_table(data1,
                  index=['CAT_NAME'],
                  values=['COST_ly', 'COST_y', 'GP_ly', 'GP_y', 'SALES_ly', 'SALES_y',
                          'UNITS_ly', 'UNITS_y'],
                  aggfunc='sum',margins=True 
                  ).reset_index()


    t2['Cat_sales_growth%']=(t2['SALES_y']/t2['SALES_ly']-1)*100
    t2['Cat_units_growth%']=(t2['UNITS_y']/t2['UNITS_ly']-1)*100
    t2['Cat_cost_growth%']=(t2['COST_y']/t2['COST_ly']-1)*100
    t2['Cat_GP_growth%']=(t2['GP_y']/t2['GP_ly']-1)*100
    t2['Category_GP%']=(t2['GP_y']/t2['SALES_ly'])*100                         

    t=t.round(2)
    t2=t2.round(2)
    t2=t2[['CAT_NAME','SALES_y','Cat_sales_growth%','Category_GP%']]
    t2.columns=['CAT_NAME','Cat_SALES_y','Cat_sales_growth%','Category_GP%']
    t=t.merge(t2,left_on="CAT_NAME",right_on="CAT_NAME",how='left')




    t['% Wt']=(t['SALES_y']/t[t['CAT_NAME']!='All']['SALES_y'].sum())*100
    t['% Wt2']=(t['SALES_ly']/t[t['CAT_NAME']!='All']['SALES_ly'].sum())*100
    t['Wt (R-H)']=t['% Wt']-t['% Wt2']

    t['Supp. share%']=(t['SALES_y']/t['Cat_SALES_y'])*100

    t=t.round(2)

    t = t.sort_values(by='SALES_y',ascending=False)

    t=t[['CAT_NAME','Cat_sales_growth%','SALES_y','sales_growth%','% Wt','Wt (R-H)','Supp. share%','UNITS_y','units_growth%','GP_y','GP%','Gain_GP','Category_GP%']]
    t.columns=['Categories','Cat R/H%','Sales Y','Sales R/H %','% Wt','Wt (R-H)','Supp. share%','Qty sold Y', 'Qty R/H%','GP Y','GP%','Gain GP','Category GP%']

    t['Sales Y']=t['Sales Y'].round(0)
    t['Qty sold Y']=t['Qty sold Y'].round(0)
    t['GP Y']=t['GP Y'].round(0)

    t_total=t[t['Categories']=='All']
    t_total['Supp. share%']=0

    t = t.head(11)
    t = t.iloc[1:]

    t=t.append(t_total,ignore_index=True)

    t=t[['Categories','Cat R/H%','Sales Y','Sales R/H %','% Wt','Wt (R-H)','Supp. share%','GP Y','GP%','Gain GP','Category GP%']]


    columns_fig=[{"name": i, "id": i} for i in t.columns]
    data_fig=t.to_dict('records')

    return columns_fig,data_fig


@app.callback(
    Output('chart_1', 'figure'),
    [Input('sup1', 'value')])
def update_chart1(sup):

    t = pd.pivot_table(data1,
                  index=['PRIMARY_SUPP'],
                  values=['COST_ly', 'COST_y', 'GP_ly', 'GP_y', 'SALES_ly', 'SALES_y',
                          'UNITS_ly', 'UNITS_y'],
                  aggfunc='sum').reset_index()

    t['sales_growth%']=(t['SALES_y']/t['SALES_ly']-1)*100
    t['units_growth%']=(t['UNITS_y']/t['UNITS_ly']-1)*100
    t['cost_growth%']=(t['COST_y']/t['COST_ly']-1)*100
    t['GP_growth%']=(t['GP_y']/t['GP_ly']-1)*100
    t['GP%']=(t['GP_y']/t['SALES_y'])*100
    t['GP2%']=(t['GP_ly']/t['SALES_ly'])*100
    t['Gain_GP']=t['GP%']-t['GP2%']

    t['Selection']=np.where(t['PRIMARY_SUPP']==str(sup),str(sup),"others")

    t=t[(t['sales_growth%']<=100)&(t['sales_growth%']>=-100)]
    t=t[(t['GP%']<=100)&(t['GP%']>=-100)]

    fig35 = px.scatter(t,x="sales_growth%",
                             y="GP%",
                             size="SALES_y",
                             hover_data=['PRIMARY_SUPP'],
                             color="Selection")
					        #  hover_data=['cat_name'])
    fig35.update_layout(title="Sales & growth% per supplier",height=500)
    # t = t.sort_values(by='SALES_y',ascending=False)

    return fig35


@app.callback(
    Output('chart_2', 'figure'),
    [Input('sup1', 'value')])
def update_chart2(sup):

    t = pd.pivot_table(data1[data1['PRIMARY_SUPP']==str(sup)],
                  index=['STORE_NAME'],
                  values=['COST_ly', 'COST_y', 'GP_ly', 'GP_y', 'SALES_ly', 'SALES_y',
                          'UNITS_ly', 'UNITS_y'],
                  aggfunc='sum').reset_index()

    t['sales_growth%']=(t['SALES_y']/t['SALES_ly']-1)*100
    t['units_growth%']=(t['UNITS_y']/t['UNITS_ly']-1)*100
    t['cost_growth%']=(t['COST_y']/t['COST_ly']-1)*100
    t['GP_growth%']=(t['GP_y']/t['GP_ly']-1)*100
    t['GP%']=(t['GP_y']/t['SALES_y'])*100
    t['GP2%']=(t['GP_ly']/t['SALES_ly'])*100
    t['Gain_GP']=t['GP%']-t['GP2%']

    # t['Selection']=np.where(t['PRIMARY_SUPP']==str(sup),str(sup),"others")

    t=t[(t['sales_growth%']<=100)&(t['sales_growth%']>=-100)]
    t=t[(t['GP%']<=100)&(t['GP%']>=-100)]

    t=t.sort_values(by='SALES_y',ascending=False)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(
             x=t["STORE_NAME"],
             y=t["SALES_y"],name="Sales"),secondary_y=False)

    fig.add_trace(go.Scatter(
             x=t["STORE_NAME"],
             y=t["sales_growth%"],name="Sales growth%"),secondary_y=True)

    fig.update_layout(title="Sales & growth% per store",height=500)

             
    fig.update_yaxes(title_text="Sales", secondary_y=False)
    fig.update_yaxes(title_text="Sales growth%", secondary_y=True)         


    return fig


@app.callback(
    Output('cat1', 'options'),
    [Input('table_1', 'derived_virtual_data')])
def dropdown_top_category(rows):

    data=pd.DataFrame(rows)
    list_cat=data[data['Categories']!='All']['Categories'].unique()
    list_cat=np.sort(list_cat)
    list_cat2=[{'label':x.replace(', Category', ''), 'value': x} for x in list_cat]
    
    return list_cat2


@app.callback(
    [Output('chart_3', 'figure'),
    Output('chart_4', 'figure')],
    [Input('cat1', 'value'),
    Input('sup1', 'value')])
def update_chart3(cat,sup):

    t = pd.pivot_table(data1[data1['CAT_NAME']==str(cat)],
                  index=['PRIMARY_SUPP'],
                  values=['COST_ly', 'COST_y', 'GP_ly', 'GP_y', 'SALES_ly', 'SALES_y',
                          'UNITS_ly', 'UNITS_y'],
                  aggfunc='sum').reset_index()

    t['sales_growth%']=(t['SALES_y']/t['SALES_ly']-1)*100
    t['units_growth%']=(t['UNITS_y']/t['UNITS_ly']-1)*100
    t['cost_growth%']=(t['COST_y']/t['COST_ly']-1)*100
    t['GP_growth%']=(t['GP_y']/t['GP_ly']-1)*100
    t['GP%']=(t['GP_y']/t['SALES_y'])*100
    t['GP2%']=(t['GP_ly']/t['SALES_ly'])*100
    t['Gain_GP']=t['GP%']-t['GP2%']

    t['Selection']=np.where(t['PRIMARY_SUPP']==str(sup),str(sup),"others")

    t=t.sort_values(by='SALES_y',ascending=False)
    
    t=t.round(2)

    t2=t.head(5)
    t2=t2[['PRIMARY_SUPP','SALES_y','SALES_ly','GP%','Selection']]

    tt_sales_y = t['SALES_y'].sum()
    tt_sales_ly = t['SALES_ly'].sum()   

    other_sales_y=tt_sales_y-t2['SALES_y'].sum()
    other_sales_ly=tt_sales_ly-t2['SALES_ly'].sum()
    other_growth = (other_sales_y/other_sales_ly-1)*100
    


    data_temp={'PRIMARY_SUPP':["Other suppliers"],
               'SALES_y':[other_sales_y],
               'SALES_ly':[other_sales_ly],
               'GP%':[other_growth],
               'Selection':["Other"]}

    temp=pd.DataFrame(data_temp,columns=['PRIMARY_SUPP','SALES_y','SALES_ly','GP%','Selection'])
    temp['PRIMARY_SUPP']="Other suppliers"
    temp['SALES_y']=other_sales_y
    temp['SALES_ly']=other_sales_ly    
    temp['GP%']=other_growth
    temp['Selection']="others"

    print(temp)

    t2=t2.append(temp,ignore_index=True)   

    fig = px.pie(t2,
                 values='SALES_y',
                 names='PRIMARY_SUPP')

    fig.update_layout(title="TOP 5 supplier in category",height=500)  

    fig35 = px.scatter(t,x="sales_growth%",
                             y="GP%",
                             size="SALES_y",
                             color="Selection",
                             hover_data=['PRIMARY_SUPP'])

    fig35.update_layout(title="Sales & growth% per supplier",height=500)




    return fig,fig35             


@app.callback(
    [Output('chart_5', 'figure'),
     Output('chart_6', 'figure'),
     Output('chart_7', 'figure'),
     Output('chart_8', 'figure'),
     Output('chart_9', 'figure')],
    [Input('sup1', 'value')])
def update_indicator(sup):

    t = pd.pivot_table(data1[data1['PRIMARY_SUPP']==str(sup)],
                  index=['SALES_TYPE'],
                  values=['COST_ly', 'COST_y', 'GP_ly', 'GP_y', 'SALES_ly', 'SALES_y',
                          'UNITS_ly', 'UNITS_y'],
                  aggfunc='sum',margins=True
                  ).reset_index()
    
    tt_sales_y = t[t['SALES_TYPE']=='All']['SALES_y'].sum()
    tt_sales_ly = t[t['SALES_TYPE']=='All']['SALES_ly'].sum()    
    sales_growth = (tt_sales_y/tt_sales_ly-1)*100

    clearance_sales = t[t['SALES_TYPE']=='CLEARANCE']['SALES_y'].sum()
    clearance_weight = clearance_sales / tt_sales_y*100

    promo_sales = t[t['SALES_TYPE']=='PROMOTION']['SALES_y'].sum()
    promo_weight = (promo_sales/tt_sales_y)*100
    
    tt_units_y = t[t['SALES_TYPE']=='All']['UNITS_y'].sum()
    tt_units_ly = t[t['SALES_TYPE']=='All']['UNITS_ly'].sum()     
    units_growth = (tt_units_y/tt_units_ly-1)*100

    tt_margin_y = t[t['SALES_TYPE']=='All']['GP_y'].sum()
    tt_margin_ly = t[t['SALES_TYPE']=='All']['GP_ly'].sum()
    margin_ly = (tt_margin_ly/tt_sales_ly)*100
    margin_y = (tt_margin_y/tt_sales_y)*100


    fig1 = go.Figure(go.Indicator(
                             mode = "number",
                             value = tt_sales_y,
                             number={'font':{'color':"black",'size':25}},
                             title = {"text": "Total Sales Y",'font':{'color':"black",'size':18}}
                             ))     

    fig2 = go.Figure(go.Indicator(
                             mode = "number",
                             value = sales_growth,
                             number={'suffix':" %",'valueformat': '.2f','font':{'color':"black",'size':25}},
                             title = {"text": "Sales Growth",'font':{'color':"black",'size':18}}
                             ))     
    fig3 = go.Figure(go.Indicator(
                             mode = "number",
                             value = units_growth,
                             number={'suffix':" %",'valueformat': '.2f','font':{'color':"black",'size':25}},
                             title = {"text": "Units Growth",'font':{'color':"black",'size':18}}
                             ))
    fig4 = go.Figure(go.Indicator(
                             mode = "number",
                             value = promo_weight,
                             number={'suffix':" %",'valueformat': '.2f','font':{'color':"black",'size':25}},
                             title = {"text": "Promo weight",'font':{'color':"black",'size':18}}
                             ))
    fig5 = go.Figure(go.Indicator(
                             mode = "number",
                             value = margin_y,
                             number={'suffix':" %",'valueformat': '.2f','font':{'color':"black",'size':25}},
                             title = {"text": "Gross profit",'font':{'color':"black",'size':18}}
                             ))

    return fig1,fig2,fig3,fig4,fig5                         
#############################################
#####   layout   ############################
#############################################



app.layout = dcc.Loading(             
              dbc.Container([
                  html.Br(),
                  html.H1("TSC - Supplier Scorecard"),
                  html.Br(),
                  html.Br(),                  
                  dbc.Row([
                      dbc.Col([html.H6("Select the supplier"),
							   dcc.Dropdown(id = 'sup1',
					                               options=list_supp, 
                                                   optionHeight=40,
                                                   value='None',
                                                   clearable=False,
                                                   placeholder="Select a supplier",
                                                   style={'height':'40px','font-size': "90%",'color': 'black'})
                              ],md=4),
                             ]),
                  html.Br(),                             
                #   dbc.Row([
                #       dbc.Col([dbc.Button("Refresh report",id="report_1", color="info", className="mr-1")   
                #           ],width={"size": 2, "offset": 1})
                #           ]),
                  html.Br(),
                  html.Br(),  
                  html.Div(children=[
                  html.Br(),     
                  dbc.Row([
                          dbc.Col([dbc.Card(fig_5)]),
                          dbc.Col([dbc.Card(fig_6)]),
                          dbc.Col([dbc.Card(fig_7)]),
                          dbc.Col([dbc.Card(fig_8)]),
                          dbc.Col([dbc.Card(fig_9)]),                                                        
                              ]), 
                  html.Br(),
                  html.Br(),                  
                  dbc.Row([html.H5("TOP 10 Categories - selected supplier", style={'margin-top': 10,'margin-left': 15})]),     
                  html.Br(),  
                  dbc.Row([                      
                      dbc.Col([html.Div(children=fig_12,style={'margin-top': 20,'margin-left': 15,'margin-right': 15})],md=12),
                          ]),
                  html.Br(),      
                  dbc.Row([
                      dbc.Col([html.H6("Select a category among TOP 10"),
							   dcc.Dropdown(id = 'cat1',
                                                   optionHeight=40,
                                                   value='None',
                                                   clearable=False,
                                                   placeholder="Select a category",
                                                   style={'height':'40px','font-size': "90%",'color': 'black'})
                              ],md=4),
                             ]),
                  html.Br(),
                  dbc.Row([                      
                      dbc.Col([html.Div(children=fig_3,style={'margin-top': 20,'margin-left': 5})],md=6),
                      dbc.Col([html.Div(children=fig_4,style={'margin-top': 20,'margin-left': 5})],md=6),
                          ]),                              
                  html.Br(),  
                  dbc.Row([html.H5("Performance per store : selected supplier", style={'margin-top': 10,'margin-left': 15})]), 
                  dbc.Row([                      
                      dbc.Col([html.Div(children=fig_2,style={'margin-top': 20,'margin-left': 5})],md=12),
                          ]),                              
                  html.Br(),                               
                  dbc.Row([html.H5("Performance comparison - other suppliers", style={'margin-top': 10,'margin-left': 15})]), 
                  dbc.Row([                      
                      dbc.Col([html.Div(children=fig_1,style={'margin-top': 20,'margin-left': 5})],md=12),
                              ]),

                  ],id="collapse4"), 
                ],fluid=True ),fullscreen=True) 




if __name__ == '__main__':
    #app.run_server(debug=False,host='10.200.134.14',port='3306')
    app.run_server(debug=False)



