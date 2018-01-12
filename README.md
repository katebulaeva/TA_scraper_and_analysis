**Trip Advisor scraper & Analysis using Jupyter Notebook**

This project is composed of 2 features:
- The TA scraper, that gets automatically restaurants data for given cities, curate them and aggregate them all together to form a dataset (Jupyte Notebook & Python files)
- The Analysis Notebook

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
The aggregated dataset is saved as "*TA_restaurants_curated.csv*". It contains the restaurants information for all the cities that have been scraped, curated in order to be able to analyse them and take interesting information out of tehm.

**ANALYSIS**

*(soon updated)*
