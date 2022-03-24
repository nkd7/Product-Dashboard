import warnings
warnings.simplefilter(action='ignore', category=Warning)
import pandas as pd
import datetime as dt
from math import ceil


class DataHolder():

    def __init__(self):
        self.salesrows = pd.read_excel('GeneratedData.xlsx', sheet_name='Sales', parse_dates=['Order Date'])
        self.salesrows['Order Date'] = pd.to_datetime(self.salesrows['Order Date'])
        self.customersrows = pd.read_excel('GeneratedData.xlsx', sheet_name='Customers')
        self.productsrows = pd.read_excel('GeneratedData.xlsx', sheet_name='Products')
        self.forecastsrows = pd.read_excel('GeneratedData.xlsx', sheet_name='Forecast By Year')
        self.salesbyproductrows = pd.read_excel('GeneratedData.xlsx', sheet_name='Sales By Product')

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

    # m: 1-12 as a string
    # quarter: 1-4 as a string
    # y: 2020, 2021, or 2022 as a string
    # data: Sales, Customers, Forecasts, or Sales by Product as a string
    def time_filter(self, m='', quarter='', y='', data=''):
        df = pd.DataFrame
        temp = None
        if data == 'Sales':
            temp = self.salesrows
            if y != '':
                df = temp[temp['Order Date'].dt.year == int(y)]
            else:
                df = temp
            if m != '':
                df = df[df['Order Date'].dt.month == int(m)]
            elif quarter != '':
                if quarter == '1':
                    df = df[df['Order Date'].dt.month < 4]
                elif quarter == '2':
                    df = df[(df['Order Date'].dt.month < 7) & (df['Order Date'].dt.month > 3)]
                elif quarter == '3':
                    df = df[(df['Order Date'].dt.month < 10) & (df['Order Date'].dt.month > 6)]
                elif quarter == '4':
                    df = df[df['Order Date'].dt.month > 9]

        elif data == 'Customers':
            sale_temp = pd.DataFrame
            sale_temp = self.salesrows[['Order Date', 'Customer ID']]
            # sale_temp['Customer ID'] = self.salesrows[['Customer ID']]
            df = pd.merge(self.customersrows, sale_temp, on='Customer ID')
            if y != '':
                df = df[df['Order Date'].dt.year == int(y)]
            if m != '':
                df = df[df['Order Date'].dt.month == int(m)]
            elif quarter != '':
                if quarter == '1':
                    df = df[df['Order Date'].dt.month < 4]
                elif quarter == '2':
                    df = df[(df['Order Date'].dt.month < 7) & (df['Order Date'].dt.month > 3)]
                elif quarter == '3':
                    df = df[(df['Order Date'].dt.month < 10) & (df['Order Date'].dt.month > 6)]
                elif quarter == '4':
                    df = df[df['Order Date'].dt.month > 9]

        elif data == 'Forecasts':
            temp = self.forecastsrows
            if y == '2020':
                df = temp[['Product', '2020 FC Quantity', '2020 FC Sales']]
                if m != '':
                    df['2020 FC Quantity'] = df['2020 FC Quantity'].apply(lambda x: ceil(float(x / 12)))
                    df['2020 FC Sales'] = df['2020 FC Sales'].apply(lambda x: ceil(float(x / 12)))
                elif quarter != '':
                    df['2020 FC Quantity'] = df['2020 FC Quantity'].apply(lambda x: ceil(float(x / 4)))
                    df['2020 FC Sales'] = df['2020 FC Sales'].apply(lambda x: ceil(float(x / 4)))
                # df['2020 FC Quantity'] = df['2020 FC Quantity'].apply(lambda x: int(x) + 1 if int(x) == 0 else x)
            elif y == '2021':
                df = temp[['Product', '2021 FC Quantity', '2021 FC Sales']]
                if m != '':
                    df['2021 FC Quantity'] = df['2021 FC Quantity'].apply(lambda x: ceil(float(x / 12)))
                    df['2021 FC Sales'] = df['2021 FC Sales'].apply(lambda x: ceil(float(x / 12)))
                elif quarter != '':
                    df['2021 FC Quantity'] = df['2021 FC Quantity'].apply(lambda x: ceil(float(x / 4)))
                    df['2021 FC Sales'] = df['2021 FC Sales'].apply(lambda x: ceil(float(x / 4)))
                # df['2021 FC Quantity'] = df['2021 FC Quantity'].apply(lambda x: int(x) + 1 if int(x) == 0 else x)
            elif y == '2022':
                df = temp[['Product', '2022 FC Quantity', '2022 FC Sales']]
                if m != '':
                    df['2022 FC Quantity'] = df['2022 FC Quantity'].apply(lambda x: ceil(float(x / 12)))
                    df['2022 FC Sales'] = df['2022 FC Sales'].apply(lambda x: ceil(float(x / 12)))
                elif quarter != '':
                    df['2022 FC Quantity'] = df['2022 FC Quantity'].apply(lambda x: ceil(float(x / 4)))
                    df['2022 FC Sales'] = df['2022 FC Sales'].apply(lambda x: ceil(float(x / 4)))
                # df['2022 FC Quantity'] = df['2022 FC Quantity'].apply(lambda x: int(x) + 1 if int(x) == 0 else x)
            else:
                df = temp

        elif data == 'Sales by Product':
            temp = self.salesbyproductrows
            df = temp
            if y == '2020':
                df = temp[['Product', '2020 Quantity', '2020 Sales']]
                df.rename(columns={'2020 Quantity': 'Quantity', '2020 Sales': 'Sales'})
            elif y == '2021':
                df = temp[['Product', '2021 Quantity', '2021 Sales']]
                df.rename(columns={'2021 Quantity': 'Quantity', '2021 Sales': 'Sales'})
            elif y == '2022':
                df = temp[['Product', '2022 Quantity', '2022 Sales']]
                df.rename(columns={'2022 Quantity': 'Quantity', '2022 Sales': 'Sales'})
            else:
                df = temp
            if m != '' or quarter != '':
                if m != '':
                    temp_sales = self.salesrows[self.salesrows['Order Date'].dt.month == int(m)]
                    temp = temp_sales[temp_sales['Order Date'].dt.year == int(y)]
                if quarter != '':
                    if quarter == '1':
                        temp_sales = self.salesrows[self.salesrows['Order Date'].dt.month < 4]
                        temp = temp_sales[temp_sales['Order Date'].dt.month < 4]
                    elif quarter == '2':
                        temp_sales = self.salesrows[(self.salesrows['Order Date'].dt.month < 7) & (self.salesrows['Order Date'].dt.month > 3)]
                        temp = temp_sales[(temp_sales['Order Date'].dt.month < 7) & (temp_sales['Order Date'].dt.month > 3)]
                    elif quarter == '3':
                        temp_sales = self.salesrows[(self.salesrows['Order Date'].dt.month < 10) & (self.salesrows['Order Date'].dt.month > 6)]
                        temp = temp_sales[(temp_sales['Order Date'].dt.month < 10) & (temp_sales['Order Date'].dt.month > 6)]
                    elif quarter == '4':
                        temp_sales = self.salesrows[self.salesrows['Order Date'].dt.month > 9]
                        temp = temp_sales[temp_sales['Order Date'].dt.month > 9]
                df = temp

        elif data == 'Products':
            df = self.productsrows

        return df

    # state: valid state in the US
    # sex: male or female
    # data: pandas dataframe with 'State' and 'Sex' columns
    def demographic_filter(self, state='', sex='', data=pd.DataFrame):
        if state != '':
            data = data[data['Customer State'] == state]
        if sex != '':
            data = data[data['Sex'] == sex]
        return data

    def merge_tables(self, left, right, column):
        return pd.merge(left, right, on=column)

    def get_data(self, inputs):
        df = self.time_filter(quarter=inputs['quarter'], m=inputs['month'], y=inputs['year'], data=inputs['data'])
        if inputs['data'] in ['Sales', 'Customers']:
            df = self.demographic_filter(state=inputs['state'], sex=inputs['sex'], data=df)
        if inputs['data'] == 'Customers':
            df.drop_duplicates(subset=['Customer ID'])
        return df