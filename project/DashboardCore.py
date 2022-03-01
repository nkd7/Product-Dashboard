from flask import Flask, render_template, request
from GraphGeneration import GraphGenerator
import json

app = Flask(__name__)

LeftMainGenerator = GraphGenerator('topLeft')
CenterMainGenerator = GraphGenerator('topRight')
RightMainGenerator = GraphGenerator('bottomLeft')
SmallChartLeft = GraphGenerator('bottomRight')
SmallChartRight = GraphGenerator('bottomRight')
SmallChartCenter = GraphGenerator('bottomRight')


# will send GraphGenerator.generatechart() output as input to populate the charts

@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":  # True if a form was submitted. Otherwise, the default homepage with default charts is given
        if 'product' not in request.form: # CASE: main chart update requested
            LeftMainGenerator.getdata(request.form)
            CenterMainGenerator.getdata(request.form)
            RightMainGenerator.getdata(request.form)
        else: # CASE: small chart update requested
            SmallChartLeft.getdata(request.form)
            SmallChartRight.getdata(request.form)
            SmallChartCenter.getdata(request.form)

    return render_template("ChartPage.html", page_title='KPI Analysis Dashboard', topLeft=LeftMainGenerator.generatechart(), topRight=CenterMainGenerator.generatechart(), bottomLeft=RightMainGenerator.generatechart(), bottomRight=SmallChartLeft.generatechart())


@app.route('/charts/')
def charts():
    return render_template("ChartPage.html", page_title='Product Dashboard', topLeft=LeftMainGenerator.generatechart(), topRight=CenterMainGenerator.generatechart(), bottomLeft=RightMainGenerator.generatechart(), bottomRight=SmallChartLeft.generatechart())


if __name__ == '__main__':
    app.run(debug=True)

# if request.form['selectChartLocation'] == 'Top Left':
#     topLeftChartGenerator.getdata(
#         [request.form["selectContent"], request.form["selectTimeFrame"], request.form["startDate"],
#          request.form["endDate"], request.form["selectDemographics"]])
# elif request.form['selectChartLocation'] == 'Top Right':
#     topRightChartGenerator.getdata(
#         [request.form["selectContent"], request.form["selectTimeFrame"], request.form["startDate"],
#          request.form["endDate"], request.form["selectDemographics"]])
# elif request.form['selectChartLocation'] == 'Bottom Left':
#     bottomLeftChartGenerator.getdata(
#         [request.form["selectContent"], request.form["selectTimeFrame"], request.form["startDate"],
#          request.form["endDate"], request.form["selectDemographics"]])
# elif request.form['selectChartLocation'] == 'Bottom Right':
#     bottomRightChartGenerator.getdata(
#         [request.form["selectContent"], request.form["selectTimeFrame"], request.form["startDate"],
#          request.form["endDate"], request.form["selectDemographics"]])