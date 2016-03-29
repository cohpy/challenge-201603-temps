#  COhPy March 2016 Challenge
This is the coding challenge for the Central Ohio Python Users Group for March 2016.

Building on last month's challenge, this month's challenge will involve figuring out dates.

This challenge has three parts. Each part builds on the previous part, and feel free to do
all the parts or only some. This challenge is for you, so implement it any way you want. Find
a new module, or way of implementing that scratches your itches.

# Part One

Given a month (say May), return a list of dates in that month that the Central Ohio Python
Users Group met. You can figure out those dates by implementing the following rules:

1. The first COhPy meeting was September 28, 2009.

2. COhPy meets the last Monday of the month, with the following exceptions:

3. COhPy never meets in November.

4. COhPy meets the first Monday of the month in December EXCEPT when that Monday is the 1st or 2nd of December, when it meets on the SECOND Monday.

5. In May, the last Monday of the month is always Memorial Day. In May, COhPy meetings on the second-to-last Monday in May.

# Part Two

Given a set of dates (particularly the dates returned in Part One), return the high temperature in Columbus, Ohio for each of those dates.

Here are a couple of resources to get historical weather observations:

APIs:
 * https://www.wunderground.com/weather/api/d/docs?d=data/history
 * https://developer.forecast.io/docs/v2#time_call
 * https://developer.worldweatheronline.com/api/historical-weather-api.aspx

CSV and other data:
 * http://www.ncdc.noaa.gov/cdo-web/search

# Part Three

Based on the data in Part Two (or whatever data you want) predict the high temperature for the next COhPy meetup. Your
prediction algorithm will run on meetup day the month prior to the one you are predicting.

At the April 2016 meeting we will run your prediction algorithms, and at the May meetup, the algorithm that most closely
predicted the high for the May meetup will receive a Python ball cap! In the event of a tie, the tied algorithms will face
off to predict June (or we'll randomly decide :-)!


