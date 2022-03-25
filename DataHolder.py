import warnings

warnings.simplefilter(action='ignore', category=Warning)
import pandas as pd
import datetime as dt
from math import ceil
import random


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
            df = pd.merge(df, self.customersrows, on='Customer ID')
            df = df[['Order Date', 'Order ID', 'Customer ID', 'Product ID', 'Quantity', 'Price', 'Customer City', 'Customer State', 'Sex']]

        elif data == 'Customers':
            df = pd.merge(self.customersrows, self.salesrows, on='Customer ID')
            df = df[['Customer ID', 'Customer Name', 'Customer Last Name', 'Customer Contact no', 'Customer Address', 'Customer City', 'Customer State', 'Sex', 'Order Date']]
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
                df = df.rename(columns={'2020 FC Quantity': 'Quantity', '2020 FC Sales': 'Sales'})
            elif y == '2021':
                df = temp[['Product', '2021 FC Quantity', '2021 FC Sales']]
                if m != '':
                    df['2021 FC Quantity'] = df['2021 FC Quantity'].apply(lambda x: ceil(float(x / 12)))
                    df['2021 FC Sales'] = df['2021 FC Sales'].apply(lambda x: ceil(float(x / 12)))
                elif quarter != '':
                    df['2021 FC Quantity'] = df['2021 FC Quantity'].apply(lambda x: ceil(float(x / 4)))
                    df['2021 FC Sales'] = df['2021 FC Sales'].apply(lambda x: ceil(float(x / 4)))
                df = df.rename(columns={'2021 FC Quantity': 'Quantity', '2021 FC Sales': 'Sales'})
            elif y == '2022':
                df = temp[['Product', '2022 FC Quantity', '2022 FC Sales']]
                if m != '':
                    df['2022 FC Quantity'] = df['2022 FC Quantity'].apply(lambda x: ceil(float(x / 12)))
                    df['2022 FC Sales'] = df['2022 FC Sales'].apply(lambda x: ceil(float(x / 12)))
                elif quarter != '':
                    df['2022 FC Quantity'] = df['2022 FC Quantity'].apply(lambda x: ceil(float(x / 4)))
                    df['2022 FC Sales'] = df['2022 FC Sales'].apply(lambda x: ceil(float(x / 4)))
                df = df.rename(columns={'2022 FC Quantity': 'Quantity', '2022 FC Sales': 'Sales'})
            else:
                df = temp

        elif data == 'SBP':
            temp = self.salesbyproductrows
            df = temp
            if y == '2020':
                df = temp[['Product', '2020 Quantity', '2020 Sales']]
                df = df.rename(columns={'2020 Quantity': 'Quantity', '2020 Sales': 'Sales'})
            elif y == '2021':
                df = temp[['Product', '2021 Quantity', '2021 Sales']]
                df = df.rename(columns={'2021 Quantity': 'Quantity', '2021 Sales': 'Sales'})
            elif y == '2022':
                df = temp[['Product', '2022 Quantity', '2022 Sales']]
                df = df.rename(columns={'2022 Quantity': 'Quantity', '2022 Sales': 'Sales'})
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

        return self.declutter(df, data)

    # state: valid state in the US
    # sex: male or female
    # data: pandas dataframe with 'State' and 'Sex' columns
    def demographic_filter(self, state='', sex='', data=pd.DataFrame):
        if state != '':
            data = data[data['Customer State'] == state]
            data.drop('Customer State', inplace=True, axis=1)
        if sex != '':
            data = data[data['Sex'] == sex]
            data.drop('Sex', inplace=True, axis=1)
        return data

    def merge_tables(self, left, right, column):
        return pd.merge(left, right, on=column)

    def get_data(self, inputs):
        df = self.time_filter(quarter=inputs['quarter'], m=inputs['month'], y=inputs['year'], data=inputs['data'])
        if inputs['data'] in ['Sales', 'Customers']:
            df = self.demographic_filter(state=inputs['state'], sex=inputs['sex'], data=df)
        return df

    def sales_data(self, sales_dict):
        sd = {'total': '', 'forc': '', 'quan': '', 'cat': ''}
        df_s = self.get_data(sales_dict)
        df_s = df_s[['Product ID', 'Quantity', 'Price']]
        sd['total'] = df_s['Price'].sum()
        sd['quan'] = df_s['Quantity'].sum()
        df_for = self.time_filter(quarter=sales_dict['quarter'], m=sales_dict['month'], y=sales_dict['year'], data='Forecasts')
        sd['forc'] = int(float(sd['total']) * 0.879)
        df_sp = pd.merge(df_s, self.productsrows, on='Product ID')
        sd['cat'] = df_sp['Category'].value_counts().idxmax()
        return sd

    def declutter(self, data, table):
        if table == 'Sales':
            data = data[['Order Date', 'Product ID', 'Quantity', 'Price', 'Customer City', 'Customer State', 'Sex']]
        elif table == 'Customers':
            data = data[['Customer Name', 'Customer Last Name', 'Customer City', 'Customer State', 'Sex']]
            data = data.drop_duplicates(subset=['Customer Last Name'])
        elif table == 'Sale by Product':
            x = 1
        elif table == 'Products':
            data = data[['Product_name', 'Product_Price', 'Product_CostPrice', 'Category']]
            data = data.rename(columns={'Product_name': 'Name', 'Product_Price': 'Price', 'Product_CostPrice': 'Manufacturing Cost', 'Category': 'Category'})
        return data

    def for_data(self, df, in_dict):
        for_dict = {}
        if in_dict['year'] == '':
            for_dict['forS'] = int((df['2020 FC Sales'].sum() + df['2021 FC Sales'].sum() + df['2022 FC Sales'].sum()))
            for_dict['forQ'] = int((df['2020 FC Quantity'].sum() + df['2021 FC Quantity'].sum() + df['2022 FC Quantity'].sum()))
        else:
            for_dict['forS'] = int(df['Sales'].sum())
            for_dict['forQ'] = int(df['Quantity'].sum())
        in_dict['data'] = 'Sales'
        df_s = self.get_data(in_dict)
        for_dict['actS'] = int(df_s['Price'].sum())
        for_dict['actQ'] = int(df_s['Quantity'].sum())
        return for_dict

    def get_cogs(self, in_dict):
        df = self.get_data(in_dict)
        df = pd.merge(df, self.productsrows)
        df = df[['Order Date', 'Product ID', 'Quantity', 'Price', 'Product_name', 'Product_Price', 'Product_CostPrice']]
        df['COGS'] = df['Quantity'] * df['Product_CostPrice']
        return df[['COGS', 'Product ID', 'Quantity', 'Order Date', 'Price']]