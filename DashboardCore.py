from datetime import datetime

from flask import Flask, render_template, request
from GraphGeneration import GraphGenerator
from DataHolder import DataHolder

app = Flask(__name__)

LeftMainGenerator = GraphGenerator('sales')
CenterMainGenerator = GraphGenerator('gromar')
RightMainGenerator = GraphGenerator('forecast')

dh = DataHolder()

# will send GraphGenerator.generatechart() output as input to populate the charts

@app.route('/', methods=["POST", "GET"])
def home():
    return render_template("HomePage.html", page_title='KPI Analysis Dashboard')

@app.route('/charts/', methods=["POST", "GET"])
def charts():
    dynamic_title = 'Performance '
    if request.method == "POST":  # True if a form was submitted. Otherwise, the default homepage with default charts is given
        if 'product' not in request.form: # CASE: main chart update requested
            LeftMainGenerator.getdata(request.form)
            CenterMainGenerator.getdata(request.form)
            RightMainGenerator.getdata(request.form)
            if 'timeframe' in request.form.keys():
                if request.form['timeframe'] == 'All':
                    dynamic_title = dynamic_title + " from 2020-2022"
                    request.form['year'] = ''
                else:
                    dynamic_title = dynamic_title + " in " + request.form['timeframe']
                    if request.form['year'] == 'All':
                        dynamic_title = dynamic_title + " 2020, 2021, and 2022"
                    else:
                        dynamic_title = dynamic_title + ' ' + request.form['year']
    else:
        LeftMainGenerator.__init__('sales')
        CenterMainGenerator.__init__('gromar')
        RightMainGenerator.__init__('forecast')
        dynamic_title = dynamic_title + 'from 2020-2022'


    return render_template("ChartPage.html", dynamic_title=dynamic_title, title='KPI Chart Analysis', topLeft=LeftMainGenerator.generatechart(), topRight=CenterMainGenerator.generatechart(), bottomLeft=RightMainGenerator.generatechart(), cursales=LeftMainGenerator.total_sales(), curgroMar=CenterMainGenerator.gross_margin(), forPer=RightMainGenerator.forecast_percent())


@app.route('/tabular/', methods=["POST", "GET"])
def tabular():
    title = 'Sales in 2020, 2021, and 2022'
    head = None
    vals = None
    input_dict = {'month': '', 'quarter': '', 'year': '', 'sex': '', 'state': '', 'data': ''}
    sales_dict = {}
    for_dict = {}
    if request.method == 'GET':
        input_dict['data'] = 'Sales'
        sales_dict = dh.sales_data(input_dict)
        df = dh.get_data(input_dict)
        head = df.columns
        vals = df.values
    if request.method == 'POST':
        title = request.form['type']
        if 'timeframe' in request.form.keys():
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
            if request.form['window'] == 'M':
                input_dict['month'] = str(datetime.strptime(request.form['timeframe'], "%B").month)
                input_dict['quarter'] = ''
            if request.form['window'] == 'Q':
                if request.form['timeframe'] == 'First Quarter':
                    input_dict['quarter'] = 1
                elif request.form['timeframe'] == 'Second Quarter':
                    input_dict['quarter'] = 2
                elif request.form['timeframe'] == 'Third Quarter':
                    input_dict['quarter'] = 3
                elif request.form['timeframe'] == 'Fourth Quarter':
                    input_dict['quarter'] = 4
                else:
                    input_dict['quarter'] = 0
        if request.form['state'] != 'N/A':
            input_dict['state'] = request.form['state']
            title = title + ' in ' + request.form['state']
        else:
            input_dict['state'] = ''
        if request.form['sex'] != 'N/A':
            input_dict['sex'] = request.form['sex']
            title = title + ' (' + request.form['sex'] + ')'
        else:
            input_dict['sex'] = ''
        input_dict['data'] = request.form['type']
        if request.form['type'] == 'Sales':
            sales_dict = dh.sales_data(input_dict)
            df = dh.get_data(input_dict)
            head = df.columns
            vals = df.values
        else:
            df = dh.get_data(input_dict)
            if request.form['type'] == 'Forecasts':
                for_dict = dh.for_data(df, input_dict)
            head = df.columns
            vals = df.values
    return render_template("TabularPage.html", title='Sales and Product Data', chartTitle=title, header=head, dat=vals, sales=sales_dict, forc=for_dict)


@app.route('/inventory/', methods=["POST", "GET"])
def inventory():

    return render_template("Inventory.html", title='Inventory', header=dh.salesrows.columns, dat=dh.salesrows.values)


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
