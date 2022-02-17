from flask import Flask, render_template, request
from GraphGeneration import GraphGenerator
import json

app = Flask(__name__)

topLeftChartGenerator = GraphGenerator('topLeft')
topRightChartGenerator = GraphGenerator('topRight')
bottomLeftChartGenerator = GraphGenerator('bottomLeft')
bottomRightChartGenerator = GraphGenerator('bottomRight')


# will send GraphGenerator.generatechart() output as input to populate the charts

@app.route('/', methods=["POST", "GET"])
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


@app.route('/charts/')
def charts():
    return render_template("ChartPage.html", page_title='Product Dashboard', topLeft=topLeftChartGenerator.generatechart(), topRight=topRightChartGenerator.generatechart(), bottomLeft=bottomLeftChartGenerator.generatechart(), bottomRight=bottomRightChartGenerator.generatechart())


if __name__ == '__main__':
    app.run(debug=True)
