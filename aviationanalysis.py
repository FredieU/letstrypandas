#! /usr/local/bin/python3

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
data = pd.read_csv(dir_path + '/summary_traffic_data_2017_Q2.csv')

# Transforming 'year' column to datetime format
data.year = pd.to_datetime(data.year, format='%Y')
data.year = data.year.dt.year

# Truncating data frame until the end of 2016 for complete years only
data = data[data.year < 2017]

# Creating a column to show months in quarters for ease of visualisation
data.insert(2, 'months', value = '')
months = ('Jan-Mar', 'Apr-Jun', 'Jul-Sep', 'Oct-Dec')
quarter_months = dict(
    [
        (1, 'Jan-Mar'), 
        (2, 'Apr-Jun'), 
        (3, 'Jul-Sep'), 
        (4, 'Oct-Dec')
    ])
data.months = data.quarter
def quarter_to_months(idx):
    return quarter_months[idx]
data.months = data.quarter.apply(quarter_to_months)

# Passengers per quarter
by_quarter = data.groupby('quarter').sum()
by_quarter.passengers.plot.pie(
    title='Passengers per quarter',
    labels=months,
    label='',
    figsize=(5, 5))

# Cargo tonnage per quarter
plt.figure()
by_quarter = data.groupby('quarter').sum()
by_quarter.cargo_tonnage.plot(
    kind='bar',
    title='Cargo tonnage per quarter',
    figsize=(5, 5))

# Quantity of passengers year on year
plt.figure()
by_year = data.groupby('year').sum()
by_year.passengers.plot(
    title = 'Flight passengers in the UK (1990 to 2016)',
    xticks=np.arange(data.year.loc[0], data.year.loc[data.shape[0]-1]+2, 2),
    figsize=(10,5))
plt.plot(
    [2008,2008], 
    [0,by_year.passengers.loc[2008]], 
    color='r', 
    linestyle='--')

# Granular look at the change in quantity of passengers
plt.figure()
change = by_year.flights.diff()
change.plot(
    title='Variation in quantity of flights per year',
    xticks=np.arange(data.year.loc[0], data.year.loc[data.shape[0] - 1] + 2, 2),
    figsize=(10, 5))
plt.fill_between(
    change.index, 
    change, 
    where=(change>0), 
    interpolate = True, 
    facecolor = 'g', 
    alpha = 0.5)
plt.fill_between(
    change.index, 
    change, 
    where=(change<0), 
    interpolate = True, 
    facecolor = 'r', 
    alpha = 0.5)

plt.show()
