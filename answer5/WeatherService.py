# WeatherService.py
# Python 2.x only.

import sys
import json
import httplib

class WeatherService:
  """Interface to Weather Underground for retrieving raw weather history.
     Instantiate without an API key (default) to pull data from a local file instead.
  """

  MOCK_DATA_PATH="weather-history.json"

  DAYS_IN_MONTH=(31,29,31,30,31,30,31,31,30,31,30,31)

  SERVICE_HOST="api.wunderground.com"

  def __init__(self,api_key=None):
    self._validate_api_key(api_key)
    self.api_key=api_key

  def retrieve(self,state,station,date):
    """Synchronously request weather history from Weather Underground.
       (state) is the postal abbreviation and (station) is the weather station name.
       (date) is a string, "YYYYMMDD".
       eg "KCMH" is the Columbus airport.
       If no API key was provided, this uses cached data instead.
    """
    self._validate_state(state)
    self._validate_station(station)
    self._valiDate(date)
    if self.api_key is None:
      return self._retrieve_mock()
    else:
      return self._retrieve_http(state,station,date)

  def is_mock(self):
    return self.api_key is None

#---------- BEGIN PRIVATE -----------------------------------------------------

  def _validate_api_key(self,api_key):
    if api_key is None: return
    if len(api_key)<1 or not api_key.isalnum(): raise Exception("Invalid API key: %r"%(api_key,))

  def _validate_state(self,state):
    if len(state)!=2 or not state.isupper(): raise Exception("Invalid state, expected /[A-Z]{2}/: %r"%(state,))

  def _validate_station(self,station):
    if len(station)<1 or len(filter(lambda x:not x.isalnum() and x!='_',station)):
      raise Exception("Invalid station name: %r"%(station,))

  def _valiDate(self,date):
    """'_valiDate', get it? I'm here all week, folks."""
    
    if len(date)!=8: self._invalid_date(date)
    if not date.isdigit(): self._invalid_date(date)
    
    year=int(date[0:4])
    if not year: self._invalid_date(date) # There isn't a year zero.

    month=int(date[4:6])
    if month<1 or month>12: self._invalid_date(date)

    day=int(date[6:8])
    if day<1 or day>self.DAYS_IN_MONTH[month-1]: self._invalid_date(date)

    if month==2 and day==29 and not self._is_leap_year(year): self._invalid_date(date)

  def _is_leap_year(self,year):
    if year%4: return False
    if year%100: return True
    if year%400: return False
    return True

  def _invalid_date(self,date):
    raise Exception("Invalid date, expected 'YYYYMMDD': %r"%(date,))

  def _retrieve_mock(self):
    src=open(self.MOCK_DATA_PATH,"r").read()
    return self._digest_response(src)

  def _retrieve_http(self,state,station,date):
    path="/api/%s/history_%s/q/%s/%s.json"%(self.api_key,date,state,station)
    connection=httplib.HTTPConnection(self.SERVICE_HOST)
    connection.putrequest("GET",path)
    connection.endheaders()
    response=connection.getresponse()
    if response.status!=200:
      raise Exception("Failed to retrieve weather history for %s/%s/%s, HTTP status %d."%(state,station,date,response.status))
    src=response.read()
    return self._digest_response(src)

  def _digest_response(self,src):
    """Given JSON text straight off the weather service, return the highest observed temperature.
    """
    hitemp=-459.67 # Absolute zero; unlikely to see anything below this, even in winter.
    
    try:
      response=json.loads(src)
    except Exception,e:
      sys.stderr.write("ERROR: Failed to unmarshal JSON response.\n")
      return hitemp

    if type(response) is not dict:
      sys.stderr.write("ERROR: Unmarshalled JSON response is not a dict.\n")
      return hitemp

    try:
      observations=response["history"]["observations"]
    except:
      sys.stderr.write("ERROR: /history/observations not found in JSON response.\n")
      return hitemp
      
    for observation in observations:
      try:
        temp=float(observation["tempi"])
      except:
        sys.stderr.write("ERROR: 'tempi' not found in observation or not a float. Skipping observation.\n")
        continue
      if temp>hitemp: hitemp=temp
      
    return hitemp
