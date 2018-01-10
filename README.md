"TA_scrapper" 

TA_Scraper.py is the command line Python script take takes as an argument the name of a city using '-c cityname'.

It creates a .csv file named "TA_cityname_restaurants_raw.csv" that contains scraped data from TA about restaurants of the given city, separated by commas.

The header of the csv file contains for restaurants:
- Name
- TA ID
- TA_URL
- Ranking
- Rate
- Cuisine style (in a list object)
- Number of reviews
- 2 revies (list of 2 lists: one with 2 reviews, one with the dates of the 2 reviews)
