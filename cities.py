# coding: utf-8

# Import packages

import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup


# Return HTML of website

website_url = requests.get("https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population").text


# View tags

soup = BeautifulSoup(website_url,"lxml")
print(soup.prettify())


# Get the table of the cities

My_table = soup.find('table',{'class':"wikitable sortable"})
My_table


# Build upon the empty arrays

i = 0
df = pd.DataFrame()
onlycities = []
population = []
descriptor = []
for row in My_table.tbody.findAll('tr'):
    if i >= 1:
        onlycities.append(row.findAll('td')[1].contents[0].getText())
        population.append(row.findAll('td')[3].contents[0])
        link = "https://en.wikipedia.org" + row.findAll('td')[1].findAll('a')[0]['href']
        website_url = requests.get(link).text
        soup = BeautifulSoup(website_url,"lxml")
        tab = soup.find('table', {'class':"infobox geography vcard"})
        print(soup.find('title'))
        try:
            descriptor.append(tab.find_all('div', class_ = "postal-code")[0].getText())
            print(tab.find_all('div', class_ = "postal-code")[0].getText())
        except:
            descriptor.append('N/A')
            print('N/A')
    i += 1
df['City'] = onlycities
df['Population'] = population
df['Zip Codes'] = descriptor


# Print the dataframe

df


# Convert to csv

df.to_csv("cities.csv")

