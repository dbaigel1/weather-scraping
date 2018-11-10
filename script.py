#A script to scrape music data from the web and analyze the data using beautiful soup and pandas etc.

from bs4 import BeautifulSoup
#library for getting html from url
#import urllib -- this wasn't working...
import requests


websiteURL = requests.get("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168") #https://pitchfork.com/reviews/albums/

if websiteURL.status_code != 200:
    print(websiteURL.status_code + "\n")
    print("Something is wrong...")
    sys.exit("Check website status code")

soup = BeautifulSoup(websiteURL.content, 'html.parser')

#Learning example, how to navigate a page
#html = list(soup.children)[2]
#body = list(html.children)[3]
#pTag = list(body.children)[1]
#print(pTag.get_text())

#how to find all tags of a specific type on a page

