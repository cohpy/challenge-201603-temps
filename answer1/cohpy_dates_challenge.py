from __future__ import print_function
from datetime import datetime
from dateutil.relativedelta import relativedelta as delta
import sys
import os

firstDate = datetime(2009, 9, 28)
months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']

def findAllMeetings(month='All', endDate=None, startDate=firstDate):
    '''
    Finds all meetings between two dates that occur in a given month, or all months.
    '''
    
    if endDate == None: endDate = datetime.now()
    dates = []
    
    if not month.isdigit():
        month = months.index(month[:3].lower()) + 1

    while startDate < endDate:
        if startDate.month != month and month != 'All':
            startDate += delta(months=1)
            continue
        
        if startDate.month == 5: #May
            # Find the last day of the month
            startDate += delta(months=1)
            startDate = datetime(startDate.year, startDate.month, 1) - delta(days=1)
            # Subtract out days to get to monday.
            # Monday == 0, so the following line will get to the last
            #  Monday of the month.
            startDate -= delta(days=startDate.weekday())
            #Subtract another 7 days to get the second-to-last Monday.
            startDate -= delta(days=7)
            dates.append(startDate)

        elif startDate.month == 11: #November
            # No meeting in November
            pass # Obviously the hardest part of this program

        elif startDate.month == 12: #December
            # Find the first day of the month
            startDate = datetime(startDate.year, startDate.month, 1)
            # Find the next Monday
            # Uses modulo arithmatic instead of a simple 7-X because
            #  7-0 = 7, where as (-0)%7 = 0. If the given day happens
            #  to be Monday by chance, this version will use it instead
            #  of the Monday after that.
            startDate += delta(days=-startDate.weekday()%7)
            # Add a week if the day is the 1st or 2nd
            if startDate.day in [1,2]:
                startDate += delta(days=7)
            dates.append(startDate)

        else: # All other months
            # Find the last Monday of the month
            # Identical to the condition for May above
            startDate += delta(months=1)
            startDate = datetime(startDate.year, startDate.month, 1) - delta(days=1)
            startDate -= delta(days=startDate.weekday())
            dates.append(startDate)

        startDate += delta(months=1)
    return dates

def getWeatherInfo(getFromInternet=False):
    '''
    Gets weather information, either from a cached file or from a web resource.

    NOTE: Getting weather information from the internet is not implemented
    '''
    
    if getFromInternet:
        pass #not implemented
    else:
        with open('weather_2009-2016.csv', 'r') as f:
            weatherData = f.read()
    # A bit of an ugly line for getting the high temperatures from the csv file.
    # I would have used the csv class, but this is just so simple to implement.
    temperatures = {line.split(',')[0]: int(line.split(',')[1]) for line in weatherData.split('\n')}
    return temperatures

def thify(number):
    '''
    Takes a number as output and returns the number with a 2 letter suffix.

    >>> thify(12)
    '12th'
    >>> thify(63)
    '63rd'
    '''
    
    if number % 10 == 1:
        return str(number) + 'st'
    elif number % 10 == 2:
        return str(number) + 'nd'
    elif number % 10 == 3:
        return str(number) + 'rd'
    elif number < 14:
        return str(number) + 'th'
    else:
        return str(number) + 'th'

if len(sys.argv) == 1:
    print('Usage: ' + os.path.basename(__file__) + ' <month>')
    exit()
month = sys.argv[1]

print('==== PART 1 ====')
dates = findAllMeetings(month)
print('COhPy has met in ' + month + ' on these dates:')
for date in dates:
    print(date.strftime('%B ' + thify(date.day) + ', %Y'))
print

print('==== PART 2 ====')
if False:# Never implemented getting weather from the internet
    print('Getting weather information...')
    weather = getWeatherInfo(True)
else:
    weather = getWeatherInfo(False)
temperatures = [weather['{d.year}-{d.month}-{d.day}'.format(d=date)] for date in dates]
print('The high temperatures for these days are:')
for x in range(len(dates)):
    print(dates[x].strftime('%B ' + thify(dates[x].day) + ', %Y') + ': ' + str(temperatures[x]) + "F")
print()
    
print('==== PART 3 ====')
# Finding the next month here
monthNum = months.index(month[:3].lower())
nextMonth = months[(monthNum+1)%12]
if nextMonth == 'nov':
    nextMonth = 'dec' # COhPy never meets in November

# Getting the temperatures for the next month
dates2 = findAllMeetings(nextMonth)
temperatures2 = [weather['{d.year}-{d.month}-{d.day}'.format(d=date)] for date in dates2]

# Prediction
prediction = int(round(sum(temperatures2) / float(len(temperatures2))))
print('I predict the high temperature on the next ' + nextMonth.capitalize() + ' meeting will be: ' + str(prediction) + 'F')
