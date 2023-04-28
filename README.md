# GenerateEasterBasedHolidays
Generate sets of VEVENT entries for holidays at a fixed offset from Easter

Usage:

  GenerateEasterBasedHolidays.py holiday-name offset-before-easter

Writes to stdout.

For holidays that never occur before March, generates 19 VEVENT entries.
Otherwise generates up to 76 VEVENT entries, to handle the inability of RRULE to automatically adjust BYMONTHDAY
for leap years, making it necessary to generate up to four sets of 19 VEVENTs so that leap years and non-leap
years are separated.

Only works from 1901 to 2099 because 1900 and 2100 do not follow the simple "years divisible by 4" leap year rule.

Examples:
  GenerateEasterBasedHolidays.py Easter           0
  GenerateEasterBasedHolidays.py "Good Friday"    2
  GenerateEasterBasedHolidays.py "Palm Sunday"    7
  GenerateEasterBasedHolidays.py "Ash Wednesday" 46
  GenerateEasterBasedHolidays.py "Mardi Gras"    47
