from flask import Flask, render_template
from GraphGeneration import GraphGenerator

app = Flask(__name__)

topLeftChartGenerator = GraphGenerator('topLeft')
topRightChartGenerator = GraphGenerator('topRight')
bottomLeftChartGenerator = GraphGenerator('bottomLeft')
bottomRightChartGenerator = GraphGenerator('bottomRight')


# will send GraphGenerator.generatechart() output as input to populate the charts

@app.route('/')
def home():
    return render_template("ChartPage.html", page_title='Product Dashboard', topLeft=topLeftChartGenerator.generatechart(), topRight=topRightChartGenerator.generatechart(), bottomLeft=bottomLeftChartGenerator.generatechart(), bottomRight=bottomRightChartGenerator.generatechart())


@app.route('/charts/')
def charts():
    return render_template("ChartPage.html", page_title='Product Dashboard', topLeft=topLeftChartGenerator.generatechart(), topRight=topRightChartGenerator.generatechart(), bottomLeft=bottomLeftChartGenerator.generatechart(), bottomRight=bottomRightChartGenerator.generatechart())


if __name__ == '__main__':
    app.run(debug=True)
