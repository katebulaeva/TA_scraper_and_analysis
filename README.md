**TRIPADVISOR SCRAPING & ANALYSIS**

This project is composed of 2 features:
- The TA scraper, that got restaurants data for given cities, curated them and aggregated them all together from separate csv files to form a dataset (Jupyte Notebook & Python files)
 - The Analysis Notebooks to explore the dataset and create visualizations
- The TA scraper, that got restaurants data for given cities, curated them and aggregated them all together from separate csv files to form a dataset (Jupyte Notebook & Python files) ;
- The Analysis Notebooks to explore the dataset and create visualizations and stories, using the Matplotlib, Seaborn and Bokeh libraries.


The dataset has been uploaded on Kaggle, feel free to create new kernels and share your results: https://www.kaggle.com/damienbeneschi/krakow-ta-restaurans-data-raw


**TA SCRAPER**

"TA_Scraper.py" is the command line Python script version take takes as an argument the name of a city using '-c cityname'.
"1.TA_scraper" is the Jupyter Notebook that contains the scripts for scraping data, scraping the European capitals restaurants info, curate the raw datasets (*raw.csv* files) and aggregate all the curated datasets into one.

The scraper creates a .csv file named "*TA_cityname_restaurants_raw.csv*" for each city that contains scraped data from TA about restaurants, separated by commas. The information are taken from the HTML code of pages such as https://www.tripadvisor.com/RestaurantSearch-g274772

The header of the csv file contains for restaurants (in random order):
- Name
- TA_ID
- TA_URL
- Ranking
- Rating
- Cuisine style (in a list object)
- Number of reviews
- 2 reviews (list of 2 lists: one with 2 reviews, one with the dates of the 2 reviews)

Each curated dataset is saved as "*TA_cityname_restaurants_curated.csv*" in the current directory.
The aggregated dataset is saved as "*TA_restaurants_curated.csv*". It contains the restaurants information for all the cities that have been scraped, curated in order to be able to analyse them and take interesting information out of them.


**ANALYSIS AND VISUALIZATION**

The "2.Analysis.ipynb" notebook contains the analysis carried out in order to answer several questions about the dataset, such as:
- What is the Price Range repartition per city?
- What are the best city for people that have a special diet (gluten, etc.) ?
- What are the common point between the top restaurants ?
- an many others.



**INTERACTIVE VISUALIZATION WITH BOKEH**

Interactive visualization have been prodced in order to have insights of the dataset, on a global way.

An aggregated dataset have been produced at the scale of the cities. This allowed to 

The Visuaization have been embeded to the notebook called "3.Analysis_Bokeh.ipynb", that contains:
- a scatter plot with y=number of reviews , x=ranking, color=price range
- a Bokeh App running on a Bokeh Server that allows to filter the previous plot accordong to the cities and rates selected thanks to a checkbox menu
- 2 linked categorical scatter plots that displays horizontaly the price range and the rate with x=number of reviews
- A Bokeh App running on a Bokeh Server that allows to visualize for each city, selected by a dropdown menu, the repartition of the restaurants according to their price range and rate
- An interactive map that displays the cities analysied in this dataset, showing the number of restaurants and reviews for the city when hovering it.
