from selenium import webdriver
import os
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random


class WebScrape:
    # open browser in background
    options = Options()
    options.headless = True
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    PATH = f"{curr_dir}\chromedriver.exe"
    driver = webdriver.Chrome(PATH, options=options)

    # loads google maps search for 'food near {address}'
    # googles 'food near me' is unreliable
    # user inputted address works better

    def pickFood(address, driver):
        url = f"https://www.google.com/maps/search/food+near+{address}/"

        driver.get(url)

        # scroll to load more restaurants
        scroll = driver.find_element(By.CLASS_NAME, "hfpxzc")
        for i in range(20):
            scroll.send_keys(Keys.PAGE_DOWN)

        # get html page source
        html = driver.page_source

        # parses html for data with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # finds restaurants names and google maps directions and appends them onto two lists
        names = soup.find_all('a', attrs={'class': 'hfpxzc'})

        names_list = []
        directions_list = []
        
        for name in names:
            names_list.append(name.get('aria-label'))
            directions_list.append(name.get('href'))

        # finds restaurants ratings and appends them onto a list
        ratings = soup.find_all('span', attrs={'class': 'MW4etd'})

        ratings_list = []

        for rating in ratings:
            ratings_list.append(rating.get_text('jsan'))

        # DUE TO FREQUENT UPDATES TO GOOGLE MAPS ON THE CODE FOR RESTAURANT DESCRIPTION, 
        # THIS SECTION IS DISCONTINUED
            # finds restaurants types and appends them onto a list
            # types = soup.find_all(
            #     'span', attrs={'jstcache': '104', 'jsinstance': '0'})

            # types_list = []
            
            # for type in types:
            #     unformatted_text = type.get_text()
            #     formatted_text = unformatted_text[4:len(unformatted_text) - 3]
            #     types_list.append(formatted_text) 

        # zip ratings list and directions list into one info list
        info_list = list(zip(ratings_list, directions_list))

        # zip the list of name with the info list into a dictionary
        res = dict(zip(names_list, info_list))

        # Chooses a random key-value pair from the dictionary and returns the results
        name, info = random.choice(list(res.items()))
        
        rating = info[0] 
        directions = info[1]
        
        return name, rating, directions
    
