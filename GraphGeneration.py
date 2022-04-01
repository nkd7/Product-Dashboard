from datetime import datetime as dt
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import Layout
from plotly.subplots import make_subplots
from DataHolder import DataHolder


# Link explaining the process from plotly to json:
# https://towardsdatascience.com/web-visualization-with-plotly-and-flask-3660abf9c946
# Flask requires that the chart be a json file, which is converted using json.dumps
class GraphGenerator:
    # position will be topLeft, topRight, bottomLeft, or bottomRight
    # there will be a corresponding default chart for each of those positions (we can change these, I just put in a
    # couple random ones for now)
    # the variable self.data will change in getdata() when a new query is run
    def __init__(self, position):
        self.for_per = 0
        self.position = position
        self.input_dis = 'Hello'
        dh = DataHolder()
        if position == 'sales':
            # total sales throughout the year
            mons = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            mon_sal = []
            df = dh.salesrows
            self.tot_sales = 0
            for month in mons:
                mon_sal.append(int(df[df['Order Date'].dt.month == month]['Price'].sum()))
                self.tot_sales = self.tot_sales + mon_sal[month - 1]
            self.data = pd.DataFrame({
                'Month': mons,
                'Sales ($)': mon_sal
            })
            self.figure = px.scatter(self.data, x='Month', y='Sales ($)', trendline='lowess')
        elif position == 'gromar':
            # gross margin
            mons = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            df_cogs = dh.get_cogs({'month': '', 'quarter': '', 'year': '', 'data': 'Sales', 'state': '', 'sex': ''})
            mon_sal = []
            mon_cogs = []
            mon_gross = []
            df = dh.salesrows
            for month in mons:
                mon_sal.append(int(df[df['Order Date'].dt.month == month]['Price'].sum()))
                mon_cogs.append(int(df_cogs[df_cogs['Order Date'].dt.month == month]['COGS'].sum()))
            self.gro_mar = 0
            for i in range(12):
                mon_gross.append(mon_sal[i]-mon_cogs[i])
                self.gro_mar = self.gro_mar + mon_gross[i]
            self.data = pd.DataFrame({
                'Month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                         'October', 'November', 'December'],
                'Gross Margin': mon_gross
            })
            self.figure = px.bar(self.data, x='Month', y='Gross Margin')
        elif position == 'forecasts':
            # forecast vs actual
            mons = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            mon_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'June', 7: 'July', 8: 'Aug', 9: 'Sept', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
            mon_sal = []
            mon_for = []
            df_s = dh.salesrows
            df_f = dh.forecastsrows
            self.for_per = 0
            for month in mons:
                mon_sal.append(int(df_s[df_s['Order Date'].dt.month == month]['Price'].sum()))
                mon_cols = [col for col in df_f.columns if mon_dict[month] in col]
                mon_cols = [col for col in mon_cols if 'Sales' in col]
                temp_df = df_f[mon_cols]
                mon_for.append(temp_df.sum().sum())
            self.for_per = sum(mon_sal) / sum(mon_for)
            df = pd.DataFrame({
                'Month': mons,
                'Sales': mon_sal,
                'Forecast': mon_for
            })
            self.figure = make_subplots()

            self.figure.add_trace(go.Scatter(x=mons, y=mon_sal, name="Sales Values"))
            self.figure.add_trace(go.Scatter(x=mons,
                                     y=mon_for,
                                     name="Forecast Values"))
            self.figure.update_xaxes(title_text='Month')
            self.figure.update_yaxes(title_text='Amount ($)')
            self.figure.update_layout(legend=dict(
                yanchor="bottom",
                y=0.01,
                xanchor="left",
                x=0.01
            ))
        elif position == 'bottomRight':
            # total sales by region
            self.figure = go.Figure(data=[go.Table(header=dict(values=['Name', 'Value']), cells=dict(values=[['Total Revenue', 'Cost of Goods Sold', 'Gross Margin', 'Operating Expenses', 'Deprec/Apprec', 'Operating Income', 'Taxes', 'Net Income'], [1034503, 561123, 1034503-561123, 179000, 12534, 1034503-561123-179000-12534, 56369, (1034503-561123-179000-12534)-54369]]))])
        else:
            self.data = None
            self.figure = None
        self.jsonFigure = json.dumps(self.figure, cls=plotly.utils.PlotlyJSONEncoder)

    def getdata(self, input_dict):
        inputs = {'quarter': 0, 'month': '', 'year': input_dict['year'], 'state': '', 'sex': ''}
        if inputs['year'] == 'All':
            inputs['year'] = ''
        if 'timeframe' in input_dict:
            if input_dict['window'] == 'M':
                inputs['month'] = str(dt.strptime(input_dict['timeframe'], "%B").month)
            if input_dict['window'] == 'Q':
                if input_dict['timeframe'] == 'First Quarter':
                    inputs['quarter'] = 1
                elif input_dict['timeframe'] == 'Second Quarter':
                    inputs['quarter'] = 2
                elif input_dict['timeframe'] == 'Third Quarter':
                    inputs['quarter'] = 3
                elif input_dict['timeframe'] == 'Fourth Quarter':
                    inputs['quarter'] = 4
                else:
                    inputs['quarter'] = 0
        dh = DataHolder()
        if self.position == 'sales':
            inputs['data'] = 'Sales'
            df = dh.get_data(inputs)
            mons = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            mon_sal = []
            self.tot_sales = 0
            for month in mons:
                mon_sal.append(int(df[df['Order Date'].dt.month == month]['Price'].sum()))
                self.tot_sales = self.tot_sales + mon_sal[month - 1]
            self.data = pd.DataFrame({
                'Month': mons,
                'Sales ($)': mon_sal
            })
            self.figure = px.scatter(self.data, x='Month', y='Sales ($)', trendline='lowess')
        elif self.position == 'gromar':
            # gross margin
            mons = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            inputs['data'] = 'Sales'
            df_cogs = dh.get_cogs(inputs)
            mon_sal = []
            mon_cogs = []
            mon_gross = []
            inputs['data'] = 'Sales'
            df = dh.get_data(inputs)
            for month in mons:
                mon_sal.append(int(df[df['Order Date'].dt.month == month]['Price'].sum()))
                mon_cogs.append(int(df_cogs[df_cogs['Order Date'].dt.month == month]['COGS'].sum()))
            self.gro_mar = 0
            for i in range(12):
                mon_gross.append(mon_sal[i] - mon_cogs[i])
                self.gro_mar = self.gro_mar + mon_gross[i]
            self.data = pd.DataFrame({
                'Month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                          'October', 'November', 'December'],
                'Gross Margin': mon_gross
            })
            self.figure = px.bar(self.data, x='Month', y='Gross Margin')
        elif self.position == 'forecasts':
            # forecast vs actual
            mons = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            mon_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'June', 7: 'July', 8: 'Aug', 9: 'Sept',
                        10: 'Oct', 11: 'Nov', 12: 'Dec'}
            mon_sal = []
            mon_for = []
            inputs['data'] = 'Sales'
            df_s = dh.get_data(inputs)
            inputs['data'] = 'Forecasts'
            df_f = dh.get_data(inputs)
            self.for_per = 0
            for month in mons:
                mon_sal.append(int(df_s[df_s['Order Date'].dt.month == month]['Price'].sum()))
                mon_cols = [col for col in df_f.columns if mon_dict[month] in col]
                mon_cols = [col for col in mon_cols if 'Sales' in col]
                temp_df = df_f[mon_cols]
                mon_for.append(temp_df.sum().sum())
            self.for_per = sum(mon_sal) / sum(mon_for)
            df = pd.DataFrame({
                'Month': mons,
                'Sales': mon_sal,
                'Forecast': mon_for
            })
            self.figure = make_subplots()

            self.figure.add_trace(go.Scatter(x=mons, y=mon_sal, name="Sales Values"))
            self.figure.add_trace(go.Scatter(x=mons,
                                             y=mon_for,
                                             name="Forecast Values"))
            self.figure.update_xaxes(title_text='Month')
            self.figure.update_yaxes(title_text='Amount ($)')
            self.figure.update_layout(legend=dict(
                yanchor="bottom",
                y=0.01,
                xanchor="left",
                x=0.01
            ))
        self.input_dis = inputs
        self.jsonFigure = json.dumps(self.figure, cls=plotly.utils.PlotlyJSONEncoder)

    def generatechart(self):
        return self.jsonFigure

    def total_sales(self):
        return self.tot_sales

    def gross_margin(self):
        return self.gro_mar

    def forecast_percent(self):
        return round(self.for_per, 2)
