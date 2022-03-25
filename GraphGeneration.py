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
        dh = DataHolder()
        if position == 'topLeft':
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
        elif position == 'topRight':
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
        elif position == 'bottomLeft':
            # forecast vs actual
            mons = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            mon_sal = []
            mon_for = []
            df_s = dh.salesrows
            df_f = dh.forecastsrows
            self.for_per = 0
            for month in mons:
                mon_sal.append(int(df_s[df_s['Order Date'].dt.month == month]['Price'].sum()))
                mon_for.append(int((df_f['2020 FC Sales'].sum() / 12)) + int((df_f['2021 FC Sales'].sum() / 12)) + int((df_f['2022 FC Sales'].sum() / 12)))
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
                yanchor="top",
                y=0.99,
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

    # query will come in as a list containing the following in order
    # 0: type of chart desired
    # 1: timeframe
    # 2: start date (optional, only used if the option "Specified Below" is chosen for timeframe)
    # 3: end date (same as start date)
    # 4: demographic differentiator
    def getdata(self, query):
        # get data from database
        self.data = None  # result of query
        # graph figure
        # assign the json dump to self.jsonFigure

    def generatechart(self):
        return self.jsonFigure

    def total_sales(self):
        return self.tot_sales

    def gross_margin(self):
        return self.gro_mar

    def forecast_percent(self):
        return round(self.for_per, 2)