# gigaChad

This is a web scrapping project that extracts restaurant/menu data from Deliveroo's website using beautifulsoup4 and the requests pacakges in Python. Deliveroo is an online food delivery company, and the here we scrape UAE's deliveroo's data. This project fetches top 10 restaurants for each cuisine (10 each for American, Arabic, Asian, etc.) having top offers, scrapes the menu items for each, gets a short description for each item and writes data to a CSV file. 

## Overview

This project uses Python to extract the restaurant names, their menu items- including prices and a short description from UAE Deliveroo's website for Abu Dhabi/Saadiyat area. The main steps are:

1. Scrape Deliveroo's website to get 10 restaurant names for all availabe cuisines, their menu, prices, description, and individual URLs. 

2. Write and save all that data to a CSV file. 

3. .... (User part?)

## Features
1. After the program is run, the user is prompeted with a few questions regarding their age, weight, gender, etc. 

2. The prigram then uses the data in our CSV file to provie restaurants and the food recommendations to meet the calorie requirement as proposed by the user. 

## Usage

- Run the main() function in the python file (main.py)
    main() calls the other two functions used for scrapping/retrieving data and storing it to the CSV file/ 

- (Anything specific when asking for user inputs ??)

## Limitations

1. We have only scrapped 10 restaurants for each cuisine. If a larger data set is required, we modify the code accordingly. 

2. Since the data is being acquired from multiple links for different cuisines, it might take some time to write teh data to the CSV file and might also take some time to fetch the data back from teh CSV file upon user request. 