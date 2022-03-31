import warnings

warnings.simplefilter(action='ignore', category=Warning)
import pandas as pd
import datetime as dt
from math import ceil
import random
import numpy as np


class DataHolder():

    def __init__(self):
        self.salesrows = pd.read_excel('GeneratedData.xlsx', sheet_name='Sales', parse_dates=['Order Date'])
        self.salesrows['Order Date'] = pd.to_datetime(self.salesrows['Order Date'])
        self.customersrows = pd.read_excel('GeneratedData.xlsx', sheet_name='Customers')
        self.productsrows = pd.read_excel('GeneratedData.xlsx', sheet_name='Products')
        self.forecastsrows = pd.read_excel('GeneratedData.xlsx', sheet_name='Monthly Forcast')

    def allsales(self):
        return self.salesrows

    def allcustomers(self):
        return self.customersrows

    def allproducts(self):
        return self.productsrows

    def allforecasts(self):
        return self.forecastsrows

    # m: 1-12 as a string
    # quarter: 1-4 as a string
    # y: 2020, 2021, or 2022 as a string
    # data: Sales, Customers, Products, or Forecasts as a string
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
            elif quarter != 0:
                if quarter == 1:
                    df = df[df['Order Date'].dt.month < 4]
                elif quarter == 2:
                    df = df[(df['Order Date'].dt.month < 7) & (df['Order Date'].dt.month > 3)]
                elif quarter == 3:
                    df = df[(df['Order Date'].dt.month < 10) & (df['Order Date'].dt.month > 6)]
                elif quarter == 4:
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
            elif quarter != 0:
                if quarter == 1:
                    df = df[df['Order Date'].dt.month < 4]
                elif quarter == 2:
                    df = df[(df['Order Date'].dt.month < 7) & (df['Order Date'].dt.month > 3)]
                elif quarter == 3:
                    df = df[(df['Order Date'].dt.month < 10) & (df['Order Date'].dt.month > 6)]
                elif quarter == 4:
                    df = df[df['Order Date'].dt.month > 9]

        elif data == 'Forecasts':
            df = self.forecastsrows
            if y != '':
                y_cols = ['Product_Id']
                if y == '2020':
                    y_cols.append([col for col in df.columns if '2020' in col])
                elif y == '2021':
                    y_cols.append([col for col in df.columns if '2021' in col])
                elif y == '2022':
                    y_cols.append([col for col in df.columns if '2022' in col])
                df = df[y_cols]

            if m != '':
                m_cols = ['Product_Id']
                if m == '1':
                    m_cols.append([col for col in df.columns if 'Jan' in col])
                elif m == '2':
                    m_cols.append([col for col in df.columns if 'Feb' in col])
                elif m == '3':
                    m_cols.append([col for col in df.columns if 'Mar' in col])
                elif m == '4':
                    m_cols.append([col for col in df.columns if 'Apr' in col])
                elif m == '5':
                    m_cols.append([col for col in df.columns if 'May' in col])
                elif m == '6':
                    m_cols.append([col for col in df.columns if 'June' in col])
                elif m == '7':
                    m_cols.append([col for col in df.columns if 'July' in col])
                elif m == '8':
                    m_cols.append([col for col in df.columns if 'Aug' in col])
                elif m == '9':
                    m_cols.append([col for col in df.columns if 'Sept' in col])
                elif m == '10':
                    m_cols.append([col for col in df.columns if 'Oct' in col])
                elif m == '11':
                    m_cols.append([col for col in df.columns if 'Nov' in col])
                elif m == '12':
                    m_cols.append([col for col in df.columns if 'Dec' in col])
                df = df[m_cols]

            if quarter != 0:
                q_cols = ['Product_Id']
                if quarter == 1:
                    q_cols.append([col for col in df.columns if 'Jan' in col])
                    q_cols.append([col for col in df.columns if 'Feb' in col])
                    q_cols.append([col for col in df.columns if 'Mar' in col])
                elif quarter == 2:
                    q_cols.append([col for col in df.columns if 'Apr' in col])
                    q_cols.append([col for col in df.columns if 'May' in col])
                    q_cols.append([col for col in df.columns if 'June' in col])
                elif quarter == 3:
                    q_cols.append([col for col in df.columns if 'July' in col])
                    q_cols.append([col for col in df.columns if 'Aug' in col])
                    q_cols.append([col for col in df.columns if 'Sept' in col])
                elif quarter == 4:
                    q_cols.append([col for col in df.columns if 'Oct' in col])
                    q_cols.append([col for col in df.columns if 'Nov' in col])
                    q_cols.append([col for col in df.columns if 'Dec' in col])
                df = df[q_cols]

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
        s_cols = [col for col in df.columns if 'Sales' in col]
        q_cols = [col for col in df.columns if 'Quantity' in col]
        df_fs = df[s_cols]
        df_fq = df[q_cols]
        for_dict['forS'] = df_fs.sum().sum()
        for_dict['forQ'] = df_fq.sum().sum()
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

    # Function that calculates the sale based on region. Regions include West, Midwast, Southwest, Northeast, and Southeast
    # self:
    #       this current object
    # region: String
    #       Must be "west", "midwest", "southwest", "northeast", or "southeast"
    def get_region_rev(self, region):
        
        # Merge sales with customers to get access to "Quantity", "Price", and "Customer State". Then drop unnecessary columns.
        df = self.allsales()
        df = pd.merge(df, self.customersrows) 
        df.drop(["Order Date", "Order ID", "Customer Name", "Customer ID", "Product ID", "Customer Last Name", "Customer Contact no", "Customer Address", "Customer City", "Sex"], inplace=True, axis=1)
        
        # Create new column for "Sale". Sale = Quantity * Price. Then, create a series that contains total sales by state.
        df['Sale'] = df["Quantity"] * df["Price"]
        series = df.groupby("Customer State")["Sale"].sum()

        west = ["Washington", "Oregon", "California", "Idaho", "Utah", "Nevada", "Montana", "Wyoming", "Colorado", "Alaska", "Hawaii"]
        mid_west = ["North Dakota", "South Dakota", "Nebraska", "Kansas", "Minnesota", "Iowa", "Missouri", "Wisconsin", "Illinois", "Michigan", "Indiana", "Ohio"]
        south_west = ["Arizona", "New Mexico", "Texas", "Oklahoma"]
        north_east = ["Maine", "New Hampshire", "Vermont", "Massachusetts", "New York", "Rhode Island", "Connecticut", "New Jersey", "Pennsylvania", "Delaware", "Maryland"]
        south_east = ["West Virginia", "Kentucky", "Virginia", "Arkansas", "Tennessee", "North Carolina", "South Carolina", "Mississippi", "Alabama", "Georgia", "Louisiana", "Florida"]

        # Sum sales for each state based on region
        regional_sales = 0
        if region == "west":
            for state, sale in series.items():
                if state in west:
                    regional_sales += sale
        elif region == "midwest":
            for state, sale in series.items():
                if state in mid_west:
                    regional_sales += sale
        elif region == "southwest":
            for state, sale in series.items():
                if state in south_west:
                    regional_sales += sale
        elif region == "northeast":
            for state, sale in series.items():
                if state in north_east:
                    regional_sales += sale
        elif region == "southeast":
            for state, sale in series.items():
                if state in south_east:
                    regional_sales += sale
        else:
            print("Error: Region is non-recognizable. Please choose from 'west', 'midwest', 'southwest', 'northeast', or 'southeast'.")

        return regional_sales
