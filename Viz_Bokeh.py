#! /usr/bin/env python3
# coding: utf-8

import logging
import ast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#For Bokeh app
from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CategoricalColorMapper, HoverTool, CheckboxGroup, CheckboxButtonGroup, Button, Toggle
from bokeh.layouts import widgetbox, row, column #,gridplot, Tabs, Panel

#Enable display of info messages
logging.basicConfig(level=logging.INFO)

#load dataset
dataset = pd.read_csv('/Users/Damien/Documents/Python Dev/Trainings/Tripadvisor_scrapping/TA_restaurants_curated.csv', encoding='utf8', index_col=0)

#Replace NaN values by 'Unknown'
dataset['Cuisine Style'] = dataset['Cuisine Style'].fillna('Unknown')
#dataset['Ranking'] = dataset['Ranking'].fillna('Unknown')
dataset['Rating'] = dataset['Rating'].fillna('?').astype(str)
dataset['Price Range'] = dataset['Price Range'].fillna('?')
dataset['Number of Reviews'] = dataset['Number of Reviews'].fillna(0)
print(dataset.info())

#Create a plot from global dataset
plot = figure(plot_width=900, plot_height=500, x_axis_label='Rank of the restaurant', 
              y_axis_label='Number of reviews', title='Global restaurants overview',
              tools='pan,box_zoom,wheel_zoom,tap,save,lasso_select')
#Data sources for each price range category, in order to have separate legends and hide them
price_ranges = dataset['Price Range'].unique().tolist()
source_low = ColumnDataSource(dataset[dataset['Price Range'] == '$'])
source_mid = ColumnDataSource(dataset[dataset['Price Range'] == '$$ - $$$'])
source_high = ColumnDataSource(dataset[dataset['Price Range'] == '$$$$'])
source_unknown = ColumnDataSource(dataset[dataset['Price Range'] == '?'])
sources = [source_low, source_mid, source_high, source_unknown]

#Separated glyphs for price range in order to use legend hide functionality
for pr, color, source in zip(price_ranges, ['yellow', 'red', 'green', 'gray'], sources):
    plot.circle('Ranking', 'Number of Reviews', source=source, color=color, size=4,
                alpha=0.5, legend=pr)
    #Hover tool hat displays name and city over point
    hover = HoverTool(tooltips=[('Restaurant Name', '@Name' ), ('City', '@City'),
                                ('Rate', '@Rating'), ('Rank', '@Ranking')])
    plot.add_tools(hover)  
    
#Legend customization
plot.legend.location='top_right'
plot.legend.click_policy="hide"

#output_file("Bokeh/Global_Viz.html")
#show(plot)

#BOKEH SERVER with interactive widgets to choose city, price range or rate (checkbox)
#Checkboxes objects added to the layout (#1st step: plots already created)
cities_list = dataset['City'].unique().tolist()
rates_list = dataset['Rating'].unique().tolist()
city_checkbox = CheckboxGroup(labels=cities_list, active=list(range(len(cities_list))))
rate_checkbox = CheckboxButtonGroup(labels=rates_list, active=list(range(len(rates_list))))
#Select_all  and refresh buttons
selectall_button = Button(label='Select all parameters')
refresh_button = Toggle(label='Refresh plot', button_type='success')

#Callback functions
def select_all(active):
    city_checkbox.active = list(range(len(cities_list)))
    rate_checkbox.active = list(range(len(rates_list)))
selectall_button.on_click(select_all)

def refresh(active):
    #Get choices from checkboxes (indexes of activated boxes)
    cities_choice = [cities_list[i] for i in city_checkbox.active]    
    rates_choice = [rates_list[i] for i in rate_checkbox.active]
    #update sources of the glyphs by filtering the dataset according to cities and rates selected
    filtered_dataset = dataset[dataset['City'].isin(cities_choice)]
    source_low.data = ColumnDataSource(filtered_dataset[filtered_dataset['Price Range'] == '$']).data
    source_mid.data = ColumnDataSource(filtered_dataset[filtered_dataset['Price Range'] == '$$ - $$$']).data
    source_high.data = ColumnDataSource(filtered_dataset[filtered_dataset['Price Range'] == '$$$$']).data
    source_unknown.data = ColumnDataSource(filtered_dataset[filtered_dataset['Price Range'] == 'Unknown']).data
refresh_button.on_click(refresh)

#Creation of the global layout displaying the checkboxes and the plot altogether
layout = row(widgetbox(city_checkbox),
             column(row(widgetbox(refresh_button, selectall_button)), widgetbox(rate_checkbox), plot))
    
#Link the checkboxes to the plot
curdoc().add_root(layout)
