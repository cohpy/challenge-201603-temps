#!/usr/bin/env python
import sys,os
import time
from WeatherService import WeatherService
from CohpyDateService import CohpyDateService

# Wunderground:
# http://api.wunderground.com/api/Your_Key/history_YYYYMMDD/q/CA/San_Francisco.json

# As traffic is throttled, I am caching the response to this request:
# curl http://api.wunderground.com/api/{YourKey}/history_20160301/q/OH/KCMH.json
# File "weather-history.json"

# Use None as the API_KEY to read from local cache only.
API_KEY=None

#------------------------------------------------------------------------------

def main_retrieve_hitemp_only():
  """Accept date, state, and station from user and report the high temperature.
  """

  # Read arguments: DATE [STATE STATION]
  if len(sys.argv)==2:
    request_date=sys.argv[1]
    request_state="OH"
    request_station="KCMH"
  elif len(sys.argv)==4:
    request_date=sys.argv[1]
    request_state=sys.argv[2]
    request_station=sys.argv[3]
  else:
    sys.stderr.write("Usage: %s DATE [STATE STATION]\n"%(sys.argv[0],))
    sys.stderr.write("  DATE is 'YYYYMMDD'\n")
    sys.stderr.write("  STATE/STATION defaults to 'OH/KCMH'\n")
    sys.exit(1)

  # Create the service and call it.
  weatherService=WeatherService(API_KEY)
  try:
    hitemp=weatherService.retrieve(request_state,request_station,request_date)
  except Exception,e:
    sys.stderr.write("ERROR: Failed to retrieve weather data: %s\n"%(e.message,))
    sys.exit(1)

  # Tell the user.
  sys.stdout.write("High temperature for date %r at station %r/%r was %r degrees Fahrenheit.\n"%(
    request_date,request_state,request_station,hitemp
  ))
  if weatherService.is_mock():
    sys.stdout.write("NB: This is mock data; the remote service was not called.\n")

#------------------------------------------------------------------------------

def main_test_date_service():
  """Calculate COHPy meeting dates and report them.
  """

  cohpyDateService=CohpyDateService()
  for date in cohpyDateService.get_meeting_dates(2014,2014):
    sys.stdout.write("> %s\n"%(date,))

#------------------------------------------------------------------------------

month_name=[
  "Nulluary",
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
]

def wild_guess(month,day):
  if month>8: distance_from_january=13-month
  else: distance_from_january=month-1
  return 30+distance_from_january*9+day%10

def informed_guess(temps):
  return sum(temps)/len(temps)

def main_predict_weather():
  """Predict the high temperature at the next COHPy meeting.
     We do this by examining the weather for that date, and another day in the month, for the past five years.
     Using two days from each month I think will help iron out anomalous days.
     Also, I don't want *exactly* the same algorithm that every other entrant uses.
     I chose to go back five years because wunderground throttles us to 10 req/min.
     We can run this script only once per minute without paying for it.
     (And only 50 times per day).
  """

  cohpyDateService=CohpyDateService()
  weatherService=WeatherService(API_KEY)

  state="OH"
  station="KCMH"

  # Get the current month.
  now=time.localtime()
  month=now.tm_mon
  next_month=month+1
  next_year=now.tm_year
  if next_month>12: 
    next_month=1
    next_year+=1
  elif next_month==11: 
    next_month=12 # No meeting in November.

  # Get the date of next month's meeting.
  date=cohpyDateService.get_meeting_date(next_year,next_month)

  sys.stdout.write("Predicting weather for our %s %s meeting (%s)...\n"%(month_name[next_month],next_year,date))

  temps=[]
  for dyear in xrange(-1,-6,-1):
  
    date1="%04d"%(next_year+dyear)+date[4:]
    try:
      hitemp=weatherService.retrieve(state,station,date1)
      if hitemp<-400: raise Exception()
    except:
      sys.stdout.write("Failed to retrieve weather for %s.\n"%(date1,))
    else:
      temps.append(hitemp)

    date1=date1[:6]+"01"
    try:
      hitemp=weatherService.retrieve(state,station,date1)
      if hitemp<-400: raise Exception()
    except:
      sys.stdout.write("Failed to retrieve weather for %s.\n"%(date1,))
    else:
      temps.append(hitemp)

  if len(temps)<1:
    sys.stdout.write("No weather data! Making a wild guess.\n")
    guess=wild_guess(next_month,int(date[6:]))
  else:
    guess=informed_guess(temps)

  sys.stdout.write("**********\n")
  sys.stdout.write("HIGH TEMPERATURE FOR THE NEXT COHPY MEETING, ON %s, WILL BE:\n"%(date,))
  sys.stdout.write("  %f DEGREES FAHRENHEIT\n"%(guess,))
  sys.stdout.write("**********\n")

#------------------------------------------------------------------------------

if __name__=="__main__":

  # Python 2.x only, please.
  if sys.version_info.major==2:
    pass
  else:
    sys.stderr.write("You are using Python version %d. This script only works with 2.\n"%(sys.version_info.major))
    sys.exit(1)

  #main_retrieve_hitemp_only()
  #main_test_date_service()
  main_predict_weather()
