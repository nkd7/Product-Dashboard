# The views.py file stores information about the view routes.
# It is accessed from the __init__.py file.
from flask import Blueprint, render_template, request
from GraphGeneration import GraphGenerator

# Create a new blueprint
views = Blueprint("view", __name__)

# Generate charts
topLeftChartGenerator = GraphGenerator('topLeft')
topRightChartGenerator = GraphGenerator('topRight')
bottomLeftChartGenerator = GraphGenerator('bottomLeft')
bottomRightChartGenerator = GraphGenerator('bottomRight')

# Add routes
# Will send GraphGenerator.generatechart() output as input to populate the charts
@views.route('/home', methods=["POST", "GET"])
def home():
    if request.method == "POST":  # True if a form was submitted. Otherwise, the default homepage with default charts is given
        if request.form['selectChartLocation'] == 'Top Left':
            topLeftChartGenerator.getdata([request.form["selectContent"], request.form["selectTimeFrame"], request.form["startDate"], request.form["endDate"], request.form["selectDemographics"]])
        elif request.form['selectChartLocation'] == 'Top Right':
            topRightChartGenerator.getdata([request.form["selectContent"], request.form["selectTimeFrame"], request.form["startDate"], request.form["endDate"], request.form["selectDemographics"]])
        elif request.form['selectChartLocation'] == 'Bottom Left':
            bottomLeftChartGenerator.getdata([request.form["selectContent"], request.form["selectTimeFrame"], request.form["startDate"], request.form["endDate"], request.form["selectDemographics"]])
        elif request.form['selectChartLocation'] == 'Bottom Right':
            bottomRightChartGenerator.getdata([request.form["selectContent"], request.form["selectTimeFrame"], request.form["startDate"], request.form["endDate"], request.form["selectDemographics"]])
    return render_template("ChartPage.html", page_title='Product Dashboard', topLeft=topLeftChartGenerator.generatechart(), topRight=topRightChartGenerator.generatechart(), bottomLeft=bottomLeftChartGenerator.generatechart(), bottomRight=bottomRightChartGenerator.generatechart())
    
@views.route('/charts/')
def charts():
    return render_template("ChartPage.html", page_title='Product Dashboard', topLeft=topLeftChartGenerator.generatechart(), topRight=topRightChartGenerator.generatechart(), bottomLeft=bottomLeftChartGenerator.generatechart(), bottomRight=bottomRightChartGenerator.generatechart())