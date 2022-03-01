from flask import Blueprint, render_template, request
from flask_login import login_required
from . import db
from .GraphGeneration import GraphGenerator

home = Blueprint('home', __name__)

LeftMainGenerator = GraphGenerator('topLeft')
CenterMainGenerator = GraphGenerator('topRight')
RightMainGenerator = GraphGenerator('bottomLeft')
SmallChartLeft = GraphGenerator('bottomRight')
SmallChartRight = GraphGenerator('bottomRight')
SmallChartCenter = GraphGenerator('bottomRight')

@home.route('/', methods=["POST", "GET"])
@login_required
def home_page():
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


@home.route('/charts/')
@login_required
def charts():
    return render_template("ChartPage.html", page_title='Product Dashboard', topLeft=LeftMainGenerator.generatechart(), topRight=CenterMainGenerator.generatechart(), bottomLeft=RightMainGenerator.generatechart(), bottomRight=SmallChartLeft.generatechart())