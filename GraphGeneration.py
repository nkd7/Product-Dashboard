import pandas as pd
import json
import plotly
import plotly.express as px


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
            self.data = None
            self.figure = None
        elif position == 'topRight':
            # sales vs forecast by product
            self.data = None
            self.figure = None
        elif position == 'bottomLeft':
            # stock prices throughout the previous year
            self.data = None
            self.figure = None
        elif position == 'bottomRight':
            # total sales by region
            self.data = None
            self.figure = None
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
