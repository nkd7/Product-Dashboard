from datetime import datetime

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
    head = dh.allsales().columns
    vals = dh.allsales().values
    input_dict = {'month': '', 'quarter': '', 'year': '', 'sex': '', 'state': ''}
    if request.method == 'POST':
        file = open('log.txt', 'w')
        title = request.form['type']
        if 'timeframe' in request.form.keys():
            file.write('Timeframe found')
            if request.form['timeframe'] == 'All':
                title = title + " from 2020-2022"
                input_dict['year'] = ''
            else:
                title = title + " in " + request.form['timeframe']
                if request.form['year'] == 'All':
                    title = title + " 2020, 2021, and 2022"
                    input_dict['year'] = ''
                else:
                    title = title + ' ' + request.form['year']
                    input_dict['year'] = request.form['year']
            file.write('Window value: ' + request.form['window'] + '\n')
            file.write('Timeframe value: ' + request.form['timeframe'] + '\n')
            if request.form['window'] == 'M':
                file.write('Month test: ' + str(datetime.strptime(request.form['timeframe'], "%B").month))
                input_dict['month'] = str(datetime.strptime(request.form['timeframe'], "%B").month)
                input_dict['quarter'] = ''
            if request.form['window'] == 'Q':
                input_dict['quarter'] = str(request.form['timeframe'])
        if request.form['state'] != 'N/A':
            input_dict['state'] = request.form['state']
        else:
            input_dict['state'] = ''
        if request.form['sex'] != 'N/A':
            input_dict['sex'] = request.form['sex']
        else:
            input_dict['sex'] = ''
        input_dict['data'] = request.form['type']
        df = dh.get_data(input_dict)
        head = df.columns
        vals = df.values
        file.close
    return render_template("TabularPage.html", title='Sales and Product Data', chartTitle=title, header=head, dat=vals)


@app.route('/inventory/', methods=["POST", "GET"])
def inventory():

    return render_template("Inventory.html", title='Inventory', header=tableHeaders, dat=tableData)


@app.route('/sales/', methods=["POST", "GET"])
def sales():

    return render_template('sales.html', title='Sales', sales_chart=LeftMainGenerator.generatechart(), top_prods=[['Product A', 1332], ['Product D', 1298], ['Product H', 1209], ['Product C', 1108], ['Product D', 1067]], top_cats=['Electronics', 'Home Goods', 'Textbooks'], cursales="36,173", prevsales="31,651", curgroMar="8,320", prevgroMar="6,102")

@app.route('/GM/', methods=["POST", "GET"])
def grossMargin():

    return render_template('GrossMargin.html', title='Gross Margin', gm_chart=CenterMainGenerator.generatechart(), bottomLeft=RightMainGenerator.generatechart(), revenues=[['Product Category 1', 200000], ['Product Category 2', 300000], ['Product Category 3', 100000], ['Product Category 4', 200000], ['Product Category 5', 200000]], expenses=[['Expense 1', 150000], ['Expense 2', 150000], ['Expense 3', 50000], ['Expense 4', 100000], ['Expense 5', 50000]], totalRevenue="1000000", totalExpenses="500000", netProfit ="500000", cursales="36,173", prevsales="31,651", curgroMar="8,320", prevgroMar="6,102")

@app.route('/FvA/', methods=["POST", "GET"])
def ForecastVsActual():

    return render_template('ForecastVsActual.html', title='Forecast vs. Actual', fva_chart=RightMainGenerator.generatechart(), top_prods=[['Product A', 1332], ['Product D', 1298], ['Product H', 1209], ['Product C', 1108], ['Product D', 1067]], top_cats=['Electronics', 'Home Goods', 'Textbooks'], cursales="36,173", prevsales="31,651", curgroMar="8,320", prevgroMar="6,102", forPer="+12.4%")

if __name__ == '__main__':
    app.run(debug=True)
