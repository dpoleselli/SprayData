# Spray Generation

This Python program scrapes the website of college baseball teams for
play-by-play data and then generates spray charts for each player.

## Description

Using BeautifulSoup, this program goes out to a specified webpage and scrapes
it for relevant play-by-play data. It then creates spray charts for the
players specified in the input csv. It is designed to function with
external systems where players have an Id. After collecting the spray 
information, the program outputs a csv file with percentage x and y 
coordinates to be plotted on a html canvas.  
This program was designed to serve as an input for 
[In-Game Edge](ingameedge.com) or [IGE-Spray](ige-spray.herokuapp.com). 
Those projects are both still in development, so for more information 
on them, please reach out to me directly.


## Input Parameters

1. url to be scraped
2. path to input csv
3. name of output file



