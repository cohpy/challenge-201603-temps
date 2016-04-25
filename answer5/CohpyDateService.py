import sys
import time

class CohpyDateService:
  """Identifies the dates of COHPy meetings.
     No, this is not a romantic match-making service.
     Not that COHPy meetings aren't romantic, of course.
  """

  FIRST_MEETING_TIME=1254110400 # 28 September 2009

  def __init__(self):
    pass

  def get_meeting_date(self,year,month):
    """Calculate a single meeting date, one year and one month.
       See get_meeting_dates().
    """
    dates=self.get_meeting_dates(year,year,month,month)
    if len(dates)<1: return "# NO MEETING IN MONTH %d OF YEAR %d\n"%(month,year)
    return dates[0]

  def get_meeting_dates(self,first_year=2009,last_year=2099,first_month=1,last_month=12):
    """Calculate the date for all meetings in the given range of years and months.
       Years are limited by default to 2009..2099, extend as far as you like.
       Months are one-based; 1=January through 12=December.
       For sanity's sake, years clamp to 1..9999 (the weather service only accepts four-digit years).
    """

    # Sanitize arguments.
    if first_year<1: first_year=1
    if last_year>9999: last_year=9999
    if first_year>last_year: return []
    if first_month<1: first_month=1
    if last_month>12: last_month=12
    if first_month>last_month: return []

    results=[]
    for year in xrange(first_year,last_year+1):
      for month in xrange(first_month,last_month+1):
        date=self._get_meeting_date(year,month)
        if date is not None: results.append(date)

    return results

#--------------- BEGIN PRIVATE ------------------------------------------------

  DAYS_IN_MONTH=(31,28,31,30,31,30,31,31,30,31,30,31)
  SECONDS_IN_DAY=86400 # Leap seconds won't matter.

  def _get_meeting_date(self,year,month):
    """Return formatted date (YYYYMMDD) of this month's meeting, or None if no meeting.
       We *do* report meeting dates before September 2009, as if the same rules existed back to the beginning of time.
    """

    # We never meet in November. Because fuck November.
    if month==11: return None

    # December is weird: first Monday, but no earlier than the third day.
    if month==12:

      # Get a struct_time for the first day of the month.
      timestamp=time.strptime("1 12 %d 12:00"%(year,),"%d %m %Y %H:%M")

      # If the first is Monday or Sunday, we are looking for the second Monday.
      day_of_month=1
      if timestamp.tm_wday==0: # 1st is Monday, meet on the 8th
        day_of_month=8
      elif timestamp.tm_wday==6: # 1st is Sunday, meet on the 9th
        day_of_month=9
      else: # Meet on the first Monday.
        day_of_month=8-timestamp.tm_wday

      return "%04d12%02d"%(year,day_of_month)

    # All other months (including oddballs February and May)...
    else:

      # Get a struct_time for the last day of the month.
      day=self.DAYS_IN_MONTH[month-1]
      if month==2 and self._is_leap_year(year): day+=1
      timestamp=time.strptime("%d %d %d 12:00"%(day,month,year),"%d %m %Y %H:%M")
      #sys.stdout.write(">>> timestamp: %r\n"%(timestamp,))

      # Subtract days based on timestamp.tm_wday -- we want Monday, ie wday zero.
      seconds_since_monday=timestamp.tm_wday*self.SECONDS_IN_DAY
      #sys.stdout.write(">>> seconds_since_monday: %r\n"%(seconds_since_monday,))
      monday_seconds=time.mktime(timestamp)-seconds_since_monday

      # In May, the meeting is one week earlier.
      if month==5:
        monday_seconds-=self.SECONDS_IN_DAY*7

      # From our UNIX timestamp, get the new struct_time and return it nicely formatted.
      meeting_timestamp=time.localtime(monday_seconds)
      if meeting_timestamp.tm_wday!=0:
        sys.stderr.write("ERROR: Expected wday zero. year=%r, month=%r, monday_seconds=%r\n"%(year,month,monday_seconds))
        return None
      return "%04d%02d%02d"%(meeting_timestamp.tm_year,meeting_timestamp.tm_mon,meeting_timestamp.tm_mday)

  def _is_leap_year(self,year):
    if year%4: return False
    if year%100: return True
    if year%400: return False
    return True
