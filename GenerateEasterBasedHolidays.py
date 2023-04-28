#!/usr/bin/env python3

# Generate Easter-based holiday VEVENT entries for ICS files, e.g
#   Easter, Good Friday, Palm Sunday, Ash Wednesday, Mardi Gras
#
# Usage:
#   GenerateEasterBasedHolidays.py holiday-name offset-before-Easter
# Output is written to stdout.

import datetime
import argparse

weekdays = ( 'MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU' )
args = None

rules = [
  { 'first': (1901, 4,  7), 'last': (2186, 4,  9), 'month':  4, 'day':  4, 'weekday':6 },
  { 'first': (1902, 3, 30), 'last': (2187, 3, 25), 'month':  3, 'day': 24, 'weekday':6 },
  { 'first': (1903, 4, 12), 'last': (2188, 4, 13), 'month':  4, 'day': 12, 'weekday':6 },
  { 'first': (1904, 4,  3), 'last': (2189, 4,  5), 'month':  4, 'day':  1, 'weekday':6 },
  { 'first': (1905, 4, 23), 'last': (2190, 4, 25), 'month':  4, 'day': 19, 'weekday':6 },
  { 'first': (1906, 4, 15), 'last': (2191, 4, 10), 'month':  4, 'day':  9, 'weekday':6 },
  { 'first': (1907, 3, 31), 'last': (2173, 4,  4), 'month':  3, 'day': 29, 'weekday':6 },
  { 'first': (1908, 4, 19), 'last': (2193, 4, 21), 'month':  4, 'day': 17, 'weekday':6 },
  { 'first': (1909, 4, 11), 'last': (2194, 4,  6), 'month':  4, 'day':  6, 'weekday':6 },
  { 'first': (1910, 3, 27), 'last': (2195, 3, 29), 'month':  3, 'day': 26, 'weekday':6 },
  { 'first': (1911, 4, 16), 'last': (2196, 4, 17), 'month':  4, 'day': 14, 'weekday':6 },
  { 'first': (1912, 4,  7), 'last': (2197, 4,  9), 'month':  4, 'day':  3, 'weekday':6 },
  { 'first': (1913, 3, 23), 'last': (2198, 3, 25), 'month':  3, 'day': 23, 'weekday':6 },
  { 'first': (1914, 4, 12), 'last': (2199, 4, 14), 'month':  4, 'day': 11, 'weekday':6 },
  { 'first': (1915, 4,  4), 'last': (2143, 3, 31), 'month':  3, 'day': 31, 'weekday':6 },
  { 'first': (1916, 4, 23), 'last': (2182, 4, 21), 'month':  4, 'day': 18, 'weekday':6 },
  { 'first': (1917, 4,  8), 'last': (2183, 4, 13), 'month':  4, 'day':  8, 'weekday':6 },
  { 'first': (1918, 3, 31), 'last': (2146, 4,  3), 'month':  3, 'day': 28, 'weekday':6 },
  { 'first': (1919, 4, 20), 'last': (2185, 4, 17), 'month':  4, 'day': 15, 'weekday':6 },
]

class dotdict(dict):
    # dot notation access to dictionary attributes
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

for i in range(len(rules)):
  rules[i] = dotdict(rules[i])


def easter(year):
  rule = rules[(year - 1901) % 19]
  # Figure out how much to add to "rule.day" so that the resulting weekday is "rule.weekday"
  baseDate = datetime.date(year, rule.month, rule.day)
  increment = (rule.weekday + 7 - baseDate.weekday()) % 7
  return baseDate + datetime.timedelta(increment)


def writeRule(first, last, month, day, interval, uidIndex):
  print('BEGIN:VEVENT')
  print('CATEGORIES:Holidays')
  print('CLASS:PUBLIC')
  #print(f'DTSTAMP:{datetime.date.today().strftime("%Y%m%dT%H%M%S")}')
  print(f'DTSTART;VALUE=DATE:{first.strftime("%Y%m%d")}')

  dateOfDay = datetime.date(first.year, month, day)
  days = str(day)
  for i in range(1,7):
    next = dateOfDay + datetime.timedelta(i)
    if next.month == month:
      days += "," + str(next.day)
    else:
      print(f'RRULE:FREQ=YEARLY;INTERVAL={interval};BYMONTH={month};BYMONTHDAY={days};' + \
            f'BYDAY={weekdays[first.weekday()]};UNTIL=20991231')
      month = next.month
      days = str(next.day)

  print(f'RRULE:FREQ=YEARLY;INTERVAL={interval};BYMONTH={month};BYMONTHDAY={days};' + \
        f'BYDAY={weekdays[first.weekday()]};UNTIL=20991231')

  print(f'SUMMARY:{args.holidayName}')
  print(f'UID:EASTER-OFFSET-{args.holidayOffset}-{uidIndex}')
  print('END:VEVENT')


def main():
  if args.holidayOffset < 0 or args.holidayOffset > 80:
    raise Exeption('Offset must be in [0,80].')
  offset = datetime.timedelta(args.holidayOffset)

  # For rules for which subtracting the offset from the starting day
  # results in March 1 or later, generate the usual repeat at 19 year intervals.
  # For other years generate four rules each with a repeat of 76 years,
  # so that it is definitively known that all years are leap years, or all are not.

  uidIndex = 0
  for rule in rules:
    print('\n')
    newFirst = datetime.date(rule.first[0], rule.first[1], rule.first[2]) - offset
    newLast = datetime.date(rule.last[0], rule.last[1], rule.last[2]) - offset
    newDayDate = datetime.date(rule.first[0], rule.month, rule.day) - offset
    if newDayDate.month >= 3:
      # New month and day are correct regardless of whether the rule covers leapyears.
      # Generate repeat at 19 year intervals.
      writeRule(newFirst, newLast, newDayDate.month, newDayDate.day, 19, uidIndex)
      uidIndex += 1
    else:
      # New month and day are correct only for years with same "leap year" attribute.
      # Generate repeat at 76 year intervals.
      # Start years are:
      #   N      the original year
      #   N+57   years one past leap year
      #   N+38   years two past leap year
      #   N+19   years three past leap year
      # Note that this only works in a range of years that all follow the 4-year leap year
      # rule; e.g. 1800, 1900, 2100 and 2200 do not follow that rule.
      # This should be checked, and UNTIL should be adjusted if necessary.
      for yearOffset in range(0,76,19):
        if yearOffset != 0:
          print()
        newFirst = easter(rule.first[0]+yearOffset) - offset
        if yearOffset == 0:
          newLast = datetime.date(rule.last[0]+yearOffset, rule.last[1], rule.last[2]) - offset
        else:
          newLast = datetime.date(rule.last[0]+yearOffset-76, rule.last[1], rule.last[2]) - offset
        newDayDate = datetime.date(rule.first[0]+yearOffset, rule.month, rule.day) - offset
        writeRule(newFirst, newLast, newDayDate.month, newDayDate.day, 76, uidIndex)
        uidIndex += 1

  print()
  print()

if __name__ == "__main__":
  # Parse command line.

  parser = argparse.ArgumentParser(description ='Generate ICS events for Easter-based holidays.')
  parser.add_argument('holidayName', metavar='Holiday Name', type=str, help='Name of the holiday')
  parser.add_argument('holidayOffset', metavar='Holiday Offset', type=int,
                    help='Number of days before Easter')
  args = parser.parse_args()
  main()
