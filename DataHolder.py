import csv
import pandas as pd


class DataHolder():
    def __init__(self):
        self.salesrows = pd.read_excel('GeneratedData.xlsx', sheet_name='Sales', parse_dates=True)
        self.customersrows = pd.read_excel('GeneratedData.xlsx', sheet_name='Customers', parse_dates=True)
        self.productsrows = pd.read_excel('GeneratedData.xlsx', sheet_name='Products', parse_dates=True)
        self.forecastsrows = pd.read_excel('GeneratedData.xlsx', sheet_name='Forecast By Year', parse_dates=True)
        self.salesbyproductrows = pd.read_excel('GeneratedData.xlsx', sheet_name='Sales By Product', parse_dates=True)

    def allsales(self):
        return self.salesrows

    def allcustomers(self):
        return self.customersrows

    def allproducts(self):
        return self.productsrows

    def allforecasts(self):
        return self.forecastsrows

    def allSBP(self):
        return self.salesbyproductrows


