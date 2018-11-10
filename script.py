#A script to scrape music data from the web and analyze the data using beautiful soup and pandas etc.

from bs4 import BeautifulSoup
import requests
import pandas as pd



websiteURL = requests.get("https://forecast.weather.gov/MapClick.php?lat=40.7146&lon=-74.0071") #https://pitchfork.com/reviews/albums/

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

#difference between find and find_all is that find returns one object while find_all returns all objects
#zone in on specific area of website to scrape
forecastContainer = soup.find(id="seven-day-forecast")
forecast7 = forecastContainer.find_all(class_="tombstone-container")

periodTags = forecastContainer.select(".tombstone-container .period-name")

periods = [pt.get_text() for pt in periodTags]
descriptions = [desc.get_text() for desc in forecastContainer.select(".tombstone-container .short-desc")]
temps = [temp.get_text() for temp in forecastContainer.select(".tombstone-container .temp")]

print(periods)
print(descriptions)
print(temps)

#now create dataframe using pandas
weatherTable = pd.DataFrame({
    "Period" : periods,
    "Description" : descriptions,
    "Temperature" : temps

	})
#Before analysis
print(weatherTable)

#do some analysis (figure out weekly avg temp)
tempNums = weatherTable["Temperature"].str.extract("(?P<temp_num>\d+)", expand=False)
weatherTable["Temp Num"] = tempNums.astype('int')

avgTemp = weatherTable["Temp Num"].mean()

weatherTable["Avg Weekly Temp"] = avgTemp


#now figure out avg nightly temp and avg day temp
isNight = weatherTable["Temperature"].str.contains("Low")
weatherTable["Night"] = isNight

row = 0
avgNightlyTemps = []
avgDailyTemps = []
for temp in weatherTable["Temp Num"]:
	if weatherTable["Night"][row] == True:
	
		avgNightlyTemps.append(temp)
	else:
		avgDailyTemps.append(temp)
	row += 1

avgDaily = sum(avgDailyTemps)/len(avgDailyTemps)
avgNightly = sum(avgNightlyTemps)/len(avgNightlyTemps)

weatherTable["Avg D Temp"] = avgDaily
weatherTable["Avg N Temp"] = avgNightly

#after analysis
print(weatherTable)










