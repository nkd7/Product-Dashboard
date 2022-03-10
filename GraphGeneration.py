import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Link explaining the process from plotly to json:
# https://towardsdatascience.com/web-visualization-with-plotly-and-flask-3660abf9c946
# Flask requires that the chart be a json file, which is converted using json.dumps
class GraphGenerator:

    # position will be topLeft, topRight, bottomLeft, or bottomRight
    # there will be a corresponding default chart for each of those positions (we can change these, I just put in a
    # couple random ones for now)
    # the variable self.data will change in getdata() when a new query is run
    def __init__(self, position):
        if position == 'topLeft':
            # total sales throughout the year
            self.data = pd.DataFrame({
                'Month': [1,2,3,4,5,6,7,8,9,10,11,12],
                'Sales ($)': [1232,2433,3441,1443,1213,2422,1232,1241,3141,2431,4322,1223]
            })
            self.figure = px.scatter(self.data, x='Month', y='Sales ($)', trendline='lowess')
        elif position == 'topRight':
            # sales vs forecast by product
            self.data = pd.DataFrame({
                'Month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                         'October', 'November', 'December'],
                'Gross Margin': [312,-108,543,-133,235,542,-38,432,134,542,134,233]
            })
            self.figure = px.bar(self.data, x='Month', y='Gross Margin')
        elif position == 'bottomLeft':
            df = pd.DataFrame({
                'Month': [1,2,3,4,5,6,7,8,9,10,11,12],
                'Sales': [1232, 2433, 3441, 1443, 1213, 2422, 1232, 1241, 3141, 2431, 4322, 1223],
                'Forecast': [1123, 2134, 3672, 1578, 809, 3023, 1400, 1232, 3400, 2208, 4521, 2300]
            })
            self.figure = make_subplots()

            self.figure.add_trace(go.Scatter(x=[1,2,3,4,5,6,7,8,9,10,11,12], y=[1232, 2433, 3441, 1443, 1213, 2422, 1232, 1241, 3141, 2431, 4322, 1223], name="Sales Values"))
            self.figure.add_trace(go.Scatter(x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                     y=[1123, 2134, 3672, 1578, 809, 3023, 1400, 1232, 3400, 2208, 4521, 2300],
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
