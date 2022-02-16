from flask import Flask, render_template
from GraphGeneration import GraphGenerator

app = Flask(__name__)

topLeftChartGenerator = GraphGenerator()
topRightChartGenerator = GraphGenerator()
bottomLeftChartGenerator = GraphGenerator()
bottomRightChartGenerator = GraphGenerator()


# will send GraphGenerator.generatechart() as input to populate the charts

@app.route('/')
def home():
    return render_template("Homepage.html", page_title='Product Dashboard', topLeft=topLeftChartGenerator.generatechart(), topRight=topRightChartGenerator.generatechart(), bottomLeft=bottomLeftChartGenerator.generatechart(), bottomRight=bottomRightChartGenerator())


@app.route('/charts/')
def charts():
    return render_template("Homepage.html", page_title='Product Dashboard', topLeft=topLeftChartGenerator.generatechart(), topRight=topRightChartGenerator.generatechart(), bottomLeft=bottomLeftChartGenerator.generatechart(), bottomRight=bottomRightChartGenerator())


if __name__ == '__main__':
    app.run(debug=True)
