#! /usr/bin/env python3
# coding: utf-8

import logging
import pandas as pd

#For Bokeh app
from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.widgets import CheckboxGroup, CheckboxButtonGroup, Button
from bokeh.layouts import widgetbox, row, column #,gridplot, Tabs, Panel
from bokeh.transform import jitter

#load dataset
dataset = pd.read_csv('/Users/Damien/Documents/Python Dev/Trainings/Tripadvisor_scrapping/TA_restaurants_curated.csv', encoding='utf8', index_col=0)

#Replace NaN values by 'Unknown'
#dataset['Cuisine Style'] = dataset['Cuisine Style'].astype(list)
#dataset['Ranking'] = dataset['Ranking'].fillna('Unknown')
dataset['Rating'] = dataset['Rating'].fillna('?').astype(str)
dataset['Price Range'] = dataset['Price Range'].fillna('?').astype(str)
dataset['Number of Reviews'] = dataset['Number of Reviews'].fillna(0)
print(dataset.info())

#Create a plot from global dataset
plot = figure(plot_width=1000, plot_height=600, x_axis_label='Rank of the restaurant', 
              y_axis_label='Number of reviews', title='Global restaurants overview',
              x_range=(0, int(dataset['Ranking'].max().tolist())),
              y_range=(0, int(dataset['Number of Reviews'].max().tolist())+500),
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
    plot.circle(x='Ranking', y='Number of Reviews', source=source,
                color=color, size=4, alpha=0.5, legend='Price Range')
    #Hover tool hat displays name and city over point
    hover = HoverTool(tooltips=[('Restaurant Name', '@Name' ), ('City', '@City'),
                                ('Rate', '@Rating'), ('Rank', '@Ranking')])
    plot.add_tools(hover)  
    
#Legend customization
plot.legend.location='top_right'
plot.legend.click_policy="hide"

#Checkboxes and buttons
cities = dataset['City'].unique().tolist()
rates = dataset['Rating'].unique().tolist()
checkbox_cities = CheckboxGroup(labels=cities, active=list(range(len(cities))))
checkbox_rates = CheckboxButtonGroup(labels=rates, active=list(range(len(rates))))
button_refresh =  Button(label='Refresh Data')
button_all = Button(label='Select all settings')

#Callback functions
def select_all(active):
    checkbox_cities.active = list(range(len(cities)))
    checkbox_rates.active = list(range(len(cities)))
button_all.on_click(select_all)

def refresh(active):
    #Get choices from checkboxes (indexes of activated boxes)
    cities_choice = [cities_list[i] for i in city_checkbox.active]    
    rates_choice = [rates_list[i] for i in rate_checkbox.active]
    #update sources of the glyphs by filtering the dataset according to cities and rates selected
    filtered_dataset = dataset[(dataset['City'].isin(cities_choice)) & (dataset['Rating'].isin(rates_choice)]
    source_low.data = ColumnDataSource(filtered_dataset[filtered_dataset['Price Range'] == '$']).data
    source_mid.data = ColumnDataSource(filtered_dataset[filtered_dataset['Price Range'] == '$$ - $$$']).data
    source_high.data = ColumnDataSource(filtered_dataset[filtered_dataset['Price Range'] == '$$$$']).data
    source_unknown.data = ColumnDataSource(filtered_dataset[filtered_dataset['Price Range'] == 'Unknown']).data
button_refresh.on_click(refresh)
    
#Layout
layout = row(widgetbox(checkbox_cities),
             column(row(widgetbox(checkbox_rates), widgetbox(button_refresh, button_all)), plot))
curdoc().add_root(layout)
curdoc().title = "Global restaurants visualization"

#bokeh serve --show "C:\Users\Damien\Documents\Python Dev\Trainings\Tripadvisor_scrapping\Viz_Bokeh.py"

#output_file("Bokeh/Global_Viz.html")
#show(layout)
