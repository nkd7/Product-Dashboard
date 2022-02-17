import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go


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
                'Fruit': ['Apples', 'Bananas', 'Oranges'],
                'Amount': [7, 2, 3]
            })
            self.figure = px.bar(self.data, x='Fruit', y='Amount', title='Fruit Inventory')
        elif position == 'topRight':
            # sales vs forecast by product
            self.data = pd.DataFrame({
                'Cars': ['Honda', 'Toyota', 'Ford'],
                'Amount': [3, 5, 9]
            })
            self.figure = px.bar(self.data, x='Cars', y='Amount', title='Car Inventory')
        elif position == 'bottomLeft':
            # stock prices throughout the previous year
            self.data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                'Sales (thousands)': [12.3, 13.9, 14.2, 13.1, 16.8]
            })
            self.figure = px.scatter(self.data, x='Month', y='Sales (thousands)', title='Car Sales by Month')
        elif position == 'bottomRight':
            # total sales by region
            self.figure = go.Figure(data=[go.Table(header=dict(values=['Product', 'Percent over Forecast']), cells=dict(values=[['Product A', 'Product B', 'Product C', 'Product D'], [1.78, 3.45, -7.23, 2.01]]))])
        else:
            self.data = None
            self.figure = None

    def getdata(self, query):
        # get data from database
        # data retrieval is a big thing we need to discuss
        # we need to have the database set up before we start pulling the data
        self.data = None

    def generatechart(self):
        return json.dumps(self.figure, cls=plotly.utils.PlotlyJSONEncoder)
