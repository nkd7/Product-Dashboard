from datetime import datetime

from flask import Flask, render_template, request, redirect
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
    return redirect("/charts/")

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
        RightMainGenerator.__init__('forecasts')
        dynamic_title = dynamic_title + 'from 2020-2022'

    return render_template("ChartPage.html", dynamic_title=dynamic_title, title='KPI Chart Analysis', topLeft=LeftMainGenerator.generatechart(), topRight=CenterMainGenerator.generatechart(), bottomLeft=RightMainGenerator.generatechart(), cursales=LeftMainGenerator.total_sales(), curgroMar=CenterMainGenerator.gross_margin(), forPer=RightMainGenerator.forecast_percent())


@app.route('/tabular/', methods=["POST", "GET"])
def tabular():
    title = 'Sales in 2020, 2021, and 2022'
    head = None
    vals = None
    input_dict = {'month': '', 'quarter': 0, 'year': '', 'sex': '', 'state': '', 'data': ''}
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
                input_dict['quarter'] = 0
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
    regions = ['West', 'Midwest', 'Southwest', 'Northeast', 'Southeast']
    region_rev = []
    t_cat = [['Electronics', 1243], ['Home Goods', 1123], ['Textbooks', 987], ['Clothing', 872]]
    dynamic_title = 'Sales '
    if request.method == 'GET':
        for region in regions:
            region_rev.append([region, dh.get_region_rev(region, m='', quarter=0, y='', data='Sales')])
        LeftMainGenerator.__init__('sales')
        dynamic_title = 'Sales from 2020-2022'
        t_cat = dh.cat_sales(month='', quar=0, year='')
    else:
        for region in regions:
            month = ''
            quar = 0
            year = ''
            if request.form['year'] != 'All':
                year = request.form['year']
            if 'timeframe' in request.form.keys():
                if request.form['window'] == 'Q':
                    if request.form['timeframe'] == 'First Quarter':
                        quar = 1
                    elif request.form['timeframe'] == 'Second Quarter':
                        quar = 2
                    elif request.form['timeframe'] == 'Third Quarter':
                        quar = 3
                    elif request.form['timeframe'] == 'Fourth Quarter':
                        quar = 4
                    else:
                        quar = 0
                if request.form['window'] == 'M':
                    month = str(datetime.strptime(request.form['timeframe'], "%B").month)
            region_rev.append([region, dh.get_region_rev(region, m=month, quarter=quar, y=year, data='Sales')])
            t_cat = dh.cat_sales(month=month, quar=quar, year=year)
        if 'product' not in request.form: # CASE: main chart update requested
            LeftMainGenerator.getdata(request.form)
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

    return render_template('sales.html', title='Sales', sales_chart=LeftMainGenerator.generatechart(), top_prods=region_rev, top_cats=t_cat, cursales=dh.sales_total, dyn_tit=dynamic_title)


@app.route('/GM/', methods=["POST", "GET"])
def grossMargin():
    regions = ['West', 'Midwest', 'Southwest', 'Northeast', 'Southeast']
    rev = []
    exp = []
    total_rev = 0
    total_exp = 0
    net_prof = 0

    if request.method == 'GET':
        for region in regions:
            total_rev += dh.get_region_rev(region, m='', quarter=0, y='', data='Sales')
            rev.append([region, dh.get_region_rev(region, m='', quarter=0, y='', data='Sales')])
            total_exp += dh.get_regional_cogs(region, m='', quarter=0, y='', data='Sales')
            exp.append([region, dh.get_regional_cogs(region, m='', quarter=0, y='', data='Sales')])
    else:
        for region in regions:
            total_rev += dh.get_region_rev(region, m='', quarter=0, y='', data='Sales')
            rev.append([region, dh.get_region_rev(region, m='', quarter=0, y='', data='Sales')])
            total_exp += dh.get_regional_cogs(region, m='', quarter=0, y='', data='Sales')
            exp.append([region, dh.get_regional_cogs(region, m='', quarter=0, y='', data='Sales')])

    net_prof = total_rev - total_exp

    return render_template('GrossMargin.html', title='Gross Margin', gm_chart=CenterMainGenerator.generatechart(), bottomLeft=RightMainGenerator.generatechart(), revenues=rev, totalRevenue=total_rev, totalExpenses=total_exp,  expenses=exp, netProfit=net_prof)


@app.route('/FvA/', methods=["POST", "GET"])
def ForecastVsActual():

    return render_template('ForecastVsActual.html', title='Forecast vs. Actual', fva_chart=RightMainGenerator.generatechart(), top_prods=[['Product A', 1332], ['Product D', 1298], ['Product H', 1209], ['Product C', 1108], ['Product D', 1067]], top_cats=['Electronics', 'Home Goods', 'Textbooks'], cursales="36,173", prevsales="31,651", curgroMar="8,320", prevgroMar="6,102", forPer="+12.4%")


if __name__ == '__main__':
    app.run(debug=True)

