#! /usr/bin/env python3
# coding: utf-8

"""
===========================
Takes a city as an argument and scrape the
summary data of each restaurants of the city
through the TA restaurants display pages
===================================================================== """

import argparse
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import numpy as np
import logging

#Variables that will be used globally through the script
url0 = 'https://www.tripadvisor.com'
today = datetime.datetime.now()
today_date = str(today.year) + '/' + str(today.month) + '/' + str(today.day)

#Enable display of info messages
logging.basicConfig(level=logging.INFO)

def get_argument():
    """Get the city name to scrape from command invite"""
    #Request for arguments of the function in command line
    parser = argparse.ArgumentParser(description='Which city would you like to scrape ?')
    #Add the type of source as an arugment
    parser.add_argument("-c", "--city",
                        help="""city name in English to be scraped for restaurants info""")
    return parser.parse_args()


def main():
    ARGS = get_argument()
    CITY = ARGS.city
    try:
        scraper(CITY)
    except:
        logging.error("Wrong city nam entered, please try again with a valid city name")
    

def scraper(city):
    query = '/TypeAheadJson?action=API&startTime='+today_date+'&uiOrigin=GEOSCOPE&source=GEOSCOPE&interleaved=true&type=geo&neighborhood_geos=true&link_type=eat&details=true&max=12&injectNeighborhoods=true&query='+city
    url = url0 + query
    #Query the API ad get a JSON answer readable by Python as dictionnaries objects
    api_response = requests.get(url).json()
    geo = api_response['results'][0]['url']  #Get the URL from the results/1st element/Url key
    restaurants_url = url0 + geo
    print(restaurants_url)

    #Prepare the scrolling requests using a URL such as
    #https://www.tripadvisor.com/RestaurantSearch-g1225481-oa15
    scroll_url0= 'https://www.tripadvisor.com/RestaurantSearch-'
    b = restaurants_url.find('-')
    e = restaurants_url.find('-', b+1)
    city_id = restaurants_url[b+1:e]
    
    #Initialize the lists of parameters to scrape and the dataframe containing all data
    inc_page=0
    resto_dict = {}
    dataset = pd.DataFrame(resto_dict)
    #columns=['Name', 'URL_TA', 'ID_TA', 'Rating', 'Ranking', 'Price Range', 'Cuisine Style', 'Number of Reviews', 'Reviews'])
    
    #Get the total number of pages
    r = requests.get(scroll_url0+city_id,
                     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',},
                     cookies= {"SetCurrency":"EUR"})
    soup = BeautifulSoup(r.text, "lxml")
    page_tag = soup.find_all(class_="pageNumbers")[0] #tag that displays number of pages at bottom of webpage
    a_tags = page_tag.find_all('a')  #last item of the returned list is the last page button
    tot_pages=int(a_tags[-1].contents[0])  #integer from text content of the <a>
    logging.info("{} pages to explore".format(tot_pages))
    
    #Explore all the pages that display restaurants
    for page_index in range (1, tot_pages+1):
        
        #URL of the current webpage
        scroll_url = scroll_url0 + city_id + '-oa' + str(inc_page)
        print("Scraping page n°{}".format(page_index))
        print(scroll_url)

        #Scrape HTML content of the current webpage using the library BeautifulSoup
        r = requests.get(scroll_url,
                 headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',},
                cookies= {"SetCurrency":"EUR"})
        soup = BeautifulSoup(r.text, "lxml")


        #Restaurants list starts with tag <div id="EATERY_SEARCH_RESULTS">
        data_bloc = soup.find_all(attrs={"id": "EATERY_SEARCH_RESULTS"}) #contains the data bloc in a list object
        data_bloc = data_bloc[0]  #easier to manipulate

    #First restaurant of page has a particular class attribute
        if data_bloc.find_all(class_="listing rebrand listingIndex-1 first") != []:
            resto_soup = data_bloc.find_all(class_="listing rebrand listingIndex-1 first")[0]
        else:
            resto_soup = data_bloc.find_all(class_="listing rebrand first")[0]

        #Get the url, id and name of restaurants
        url_name_tag = resto_soup.find_all(class_="property_title")[0] #tag containing the data
        #Get restaurant URL
        resto_dict['URL_TA'] = url_name_tag.get('href')
        #Get the restaurant ID within its URL (-dxxxxxxx-Reviews)
        b = url_name_tag.get('href').find('-d')
        e= url_name_tag.get('href').find('-R')
        resto_dict['ID_TA'] = url_name_tag.get('href')[b+1:e]
        #Get names
        resto_dict['Name'] = url_name_tag.contents[0][1:-1]

        #Get the ranking of the restaurant
        if resto_soup.find_all(class_="popIndex rebrand popIndexDefault") != []:
            ranking_tag = resto_soup.find_all(class_="popIndex rebrand popIndexDefault")[0]
            resto_dict['Ranking'] = ranking_tag.contents[0][1:-1]
        else:
            resto_dict['Ranking'] = np.nan #put a NaN instead

        #Get the rating of the restaurant from <span> tags
        if resto_soup.find_all('span') != []:
            span_tags = resto_soup.find_all('span')
            for tag in span_tags:
                if tag.get('alt') is not None:
                    resto_dict['Rating'] = tag.get('alt')
        else:
            resto_dict['Rating'] = np.nan

        #Information from <div class="cuisines">  
        #!! some resaurants don't have pricerange nor cuisine styles, instead <div class="cuisine_margin">
        cuisines_tags = resto_soup.find_all(class_="cuisines") #1 element of the list is 1 restaurant
        if resto_soup.find_all(class_="cuisines") != []:
            for item in cuisines_tags:
                #Get price range from <span class="item price">
                if item.find(class_="item price") is not None:
                    price_range = item.find(class_="item price") #unique tag with price range
                    resto_dict['Price Range'] = price_range.contents[0]
                else:
                     resto_dict['Price Range'] = np.nan
                #Get cuisine styles from <span class="item cuisine"> tags (several/restaurant)
                if item.find_all(class_="item cuisine") != []:
                    cuisines = item.find_all(class_="item cuisine")  # list of <a> tags with the cuisine style as text
                    resto_dict['Cuisine Style'] = [tag.contents[0] for tag in cuisines]
                else:
                    resto_dict['Cuisine Style'] = np.nan

        #Get number of reviews
        if resto_soup.find_all(class_="reviewCount") != []:
            numb_tag = resto_soup.find_all(class_="reviewCount")[0]
            resto_dict['Number of Reviews'] = numb_tag.find('a').contents[0][1:-9]
        else:
            resto_dict['Number of Reviews'] = np.nan
            
        #Get 2 reviews (text+date) from <ul class="review_stubs review_snippets rebrand"> and <li> tags within
        ul_tags = resto_soup.find_all(class_="review_stubs review_snippets rebrand")
        if ul_tags != []:
            for reviews_set in ul_tags:
                rev_texts = reviews_set.find_all(dir="ltr")
                rev_dates = reviews_set.find_all(class_="date")
                resto_dict['Reviews'] = [[tag.find('a').contents[0] for tag in rev_texts], #text is in a <a> tag
                                          [tag.contents[0] for tag in rev_dates]]
        else:
            resto_dict['Reviews'] = np.nan
            
        #Append the dataset
        dataset = pd.concat([dataset, pd.DataFrame([resto_dict])])
            
    #For the rest of the list from 2 to 30:
        try:
            inc_rest = 0
            for i in range (2, 31):
                resto_dict = {}
                resto_bloc_id = "listing rebrand listingIndex-" + str(i)
                if data_bloc.find_all(class_=resto_bloc_id) != []:
                    resto_soup = data_bloc.find_all(class_=resto_bloc_id)[0] #Bloc for one restaurant

                    #Get the url, id and name of restaurants
                    url_name_tag = resto_soup.find_all(class_="property_title")[0] #tag containing the data
                    #Get restaurant URL
                    resto_dict['URL_TA'] = url_name_tag.get('href')
                    #Get the restaurant ID within its URL (-dxxxxxxx-Reviews)
                    b = url_name_tag.get('href').find('-d')
                    e= url_name_tag.get('href').find('-R')
                    resto_dict['ID_TA'] = url_name_tag.get('href')[b+1:e]
                    #Get names
                    resto_dict['Name'] = url_name_tag.contents[0][1:-1]

                    #Get the ranking of the restaurant
                    if resto_soup.find_all(class_="popIndex rebrand popIndexDefault") != []:
                        ranking_tag = resto_soup.find_all(class_="popIndex rebrand popIndexDefault")[0]
                        resto_dict['Ranking'] = ranking_tag.contents[0][1:-1]
                    else:
                        resto_dict['Ranking'] = np.nan

                    #Get the rating of the restaurant from <span> tags
                    span_tags = resto_soup.find_all('span')
                    if resto_soup.find_all('span') != []:
                        for tag in span_tags:
                            if tag.get('alt') is not None:
                                resto_dict['Rating'] = tag.get('alt')
                    else:
                        resto_dict['Rating'] = np.nan

                    #Information from <div class="cuisines">  
                    #!! some resaurants don't have pricerange nor cuisine styles, instead <div class="cuisine_margin">
                    cuisines_tags = resto_soup.find_all(class_="cuisines") #1 element of the list is 1 restaurant
                    if resto_soup.find_all(class_="cuisines") != []:
                        for item in cuisines_tags:
                            #Get price range from <span class="item price">
                            if item.find(class_="item price") is not None:
                                price_range = item.find(class_="item price") #unique tag with price range
                                resto_dict['Price Range'] = price_range.contents[0]
                            else:
                                resto_dict['Price Range'] = np.nan
                            #Get cuisine styles from <span class="item cuisine"> tags (several/restaurant)
                            if item.find_all(class_="item cuisine") != []:
                                cuisines = item.find_all(class_="item cuisine")  # list of <a> tags with the cuisine style as text
                                resto_dict['Cuisine Style'] = [tag.contents[0] for tag in cuisines]
                            else: 
                                resto_dict['Cuisine Style'] = np.nan

                    #Get number of reviews
                    if resto_soup.find_all(class_="reviewCount") != []:
                        numb_tag = resto_soup.find_all(class_="reviewCount")[0]
                        resto_dict['Number of Reviews'] = numb_tag.find('a').contents[0][1:-9]
                    else:
                        resto_dict['Number of Reviews'] = np.nan

                    #Get 2 reviews (text+date) from <ul class="review_stubs review_snippets rebrand"> and <li> tags within
                    ul_tags = resto_soup.find_all(class_="review_stubs review_snippets rebrand")
                    if resto_soup.find_all(class_="review_stubs review_snippets rebrand") != []:
                        for reviews_set in ul_tags:
                            rev_texts = reviews_set.find_all(dir="ltr")
                            rev_dates = reviews_set.find_all(class_="date")
                            resto_dict['Reviews'] = [[tag.find('a').contents[0] for tag in rev_texts], #text is in a <a> tag
                                                  [tag.contents[0] for tag in rev_dates]]
                    else:
                        resto_dict['Reviews'] = np.nan
                    
                    #Append the dataset
                    dataset = pd.concat([dataset, pd.DataFrame([resto_dict])])
                        
                else: #tag of restaurant is instead "listing rebrand"
                    resto_soup = data_bloc.find_all(class_="listing rebrand")[inc_rest]
                    
                    #Get the url, id and name of restaurants
                    url_name_tag = resto_soup.find_all(class_="property_title")[0] #tag containing the data
                    #Get restaurant URL
                    resto_dict['URL_TA'] = url_name_tag.get('href')
                    #Get the restaurant ID within its URL (-dxxxxxxx-Reviews)
                    b = url_name_tag.get('href').find('-d')
                    e= url_name_tag.get('href').find('-R')
                    resto_dict['ID_TA'] = url_name_tag.get('href')[b+1:e]
                    #Get names
                    resto_dict['Name'] = url_name_tag.contents[0][1:-1]

                    #Get the ranking of the restaurant
                    if resto_soup.find_all(class_="popIndex rebrand popIndexDefault") != []:
                        ranking_tag = resto_soup.find_all(class_="popIndex rebrand popIndexDefault")[0]
                        resto_dict['Ranking'] = ranking_tag.contents[0][1:-1]
                    else:
                        resto_dict['Ranking'] = np.nan

                    #Get the rating of the restaurant from <span> tags
                    span_tags = resto_soup.find_all('span')
                    if resto_soup.find_all('span') != []:
                        for tag in span_tags:
                            if tag.get('alt') is not None:
                                resto_dict['Rating'] = tag.get('alt')
                    else:
                        resto_dict['Rating'] = np.nan

                    #Information from <div class="cuisines">  
                    #!! some resaurants don't have pricerange nor cuisine styles, instead <div class="cuisine_margin">
                    cuisines_tags = resto_soup.find_all(class_="cuisines") #1 element of the list is 1 restaurant
                    if resto_soup.find_all(class_="cuisines") != []:
                        for item in cuisines_tags:
                            #Get price range from <span class="item price">
                            if item.find(class_="item price") is not None:
                                price_range = item.find(class_="item price") #unique tag with price range
                                resto_dict['Price Range'] = price_range.contents[0]
                            else:
                                resto_dict['Price Range'] = np.nan
                            #Get cuisine styles from <span class="item cuisine"> tags (several/restaurant)
                            if item.find_all(class_="item cuisine") != []:
                                cuisines = item.find_all(class_="item cuisine")  # list of <a> tags with the cuisine style as text
                                resto_dict['Cuisine Style'] = [tag.contents[0] for tag in cuisines]
                            else: 
                                resto_dict['Cuisine Style'] = np.nan

                    #Get number of reviews
                    if resto_soup.find_all(class_="reviewCount") != []:
                        numb_tag = resto_soup.find_all(class_="reviewCount")[0]
                        resto_dict['Number of Reviews'] = numb_tag.find('a').contents[0][1:-9]
                    else:
                        resto_dict['Number of Reviews'] = np.nan

                    #Get 2 reviews (text+date) from <ul class="review_stubs review_snippets rebrand"> and <li> tags within
                    ul_tags = resto_soup.find_all(class_="review_stubs review_snippets rebrand")
                    if resto_soup.find_all(class_="review_stubs review_snippets rebrand") != []:
                        for reviews_set in ul_tags:
                            rev_texts = reviews_set.find_all(dir="ltr")
                            rev_dates = reviews_set.find_all(class_="date")
                            resto_dict['Reviews'] = [[tag.find('a').contents[0] for tag in rev_texts], #text is in a <a> tag
                                                  [tag.contents[0] for tag in rev_dates]]
                    else:
                        resto_dict['Reviews'] = np.nan
                    
                    #Append the dataset
                    dataset = pd.concat([dataset, pd.DataFrame([resto_dict])])
                    
                    inc_rest += 1
                
            #Increment to next page to display the next 30 restaurants
            inc_page += 30
    
        except IndexError:
            logging.info("Last restaurant reached")
            break
    
    #Save dataframe as csv file
    dataset.to_csv(city + '_TA_restaurants_raw.csv', sep=',', encoding="utf-8")
    print("File created in current directory: {}_TA_restaurants_raw.csv".format(city))

    return(dataset)


if __name__ == '__main__':
    main()
