from flask import Flask, render_template, request
from GraphGeneration import GraphGenerator
from DataHolder import DataHolder

app = Flask(__name__)

LeftMainGenerator = GraphGenerator('topLeft')
CenterMainGenerator = GraphGenerator('topRight')
RightMainGenerator = GraphGenerator('bottomLeft')
SmallChartLeft = GraphGenerator('bottomRight')
SmallChartRight = GraphGenerator('bottomRight')
SmallChartCenter = GraphGenerator('bottomRight')

tableHeaders = ['Order Date', 'Order Number', 'Customer ID', 'Product', 'Quantity', 'Sale Price ($)']
tableData = [['1/21/21', '123', '12', 'Product 1', '2', '44'], ['2/11/21', '54', '15', 'Product 6', '4', '24'], ['3/23/21', '14', '63', 'Product 12', '1', '25'], ['4/15/21', '46', '78', 'Product 15', '9', '18'], ['5/21/21', '874', '62', 'Product 17', '3', '90'], ['6/30/21', '234', '90', 'Product 24', '1', '20'], ]

dh = DataHolder()


# will send GraphGenerator.generatechart() output as input to populate the charts

@app.route('/', methods=["POST", "GET"])
def home():
    return render_template("HomePage.html", page_title='KPI Analysis Dashboard')


@app.route('/charts/', methods=["POST", "GET"])
def charts():
    if request.method == "POST":  # True if a form was submitted. Otherwise, the default homepage with default charts is given
        if 'product' not in request.form: # CASE: main chart update requested
            LeftMainGenerator.getdata(request.form)
            CenterMainGenerator.getdata(request.form)
            RightMainGenerator.getdata(request.form)
        else: # CASE: small chart update requested
            SmallChartLeft.getdata(request.form)
            SmallChartRight.getdata(request.form)
            SmallChartCenter.getdata(request.form)

    return render_template("ChartPage.html", title='KPI Chart Analysis', topLeft=LeftMainGenerator.generatechart(), topRight=CenterMainGenerator.generatechart(), bottomLeft=RightMainGenerator.generatechart(), bottomRight=SmallChartLeft.generatechart(), cursales="36,173", prevsales="31,651", curgroMar="8,320", prevgroMar="6,102", forPer="+12.4%")


@app.route('/tabular/', methods=["POST", "GET"])
def tabular():
    title = 'Sales in 2021'
    if request.method == 'POST':
        title = request.form['type']
        if request.form['timeframe'] == 'All':
            title = title + " from 2020-2022"
        else:
            title = title + " in " + request.form['timeframe']
        if request.form['demo'] != 'N/A':
            title = title + " by " + request.form['demo']
    return render_template("TabularPage.html", title='Sales and Product Data', chartTitle=title, header=dh.allsales().columns, dat=dh.allsales().values)


@app.route('/inventory/', methods=["POST", "GET"])
def inventory():

    return render_template("Inventory.html", title='Inventory', header=tableHeaders, dat=tableData)

if __name__ == '__main__':
    app.run(debug=True)
