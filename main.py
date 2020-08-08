import csv
import urllib.request
import codecs
import datetime

DATE = 0
COUNTY = 1
STATE = 2
FIPS = 3
CASES = 4
DEATHS = 5

NEVER = 1
RARELY = 2
SOMETIMES = 3
FREQUENTLY = 4
ALWAYS = 5

POPULATION = 18

state = input("Enter in your state name: ")
county = input("Enter in your county name: ")
#date = input("Enter in the date you want to look at: ")

def get_time():
  now = datetime.date.today()
  day = now - datetime.timedelta(days = 2)
  today = "20" + day.strftime("%y") + "-" + day.strftime("%m") + "-" + day.strftime("%d")
  return today

def get_yesterday():
  now = datetime.date.today()
  day = now - datetime.timedelta(days = 9)
  yesterday = "20" + day.strftime("%y") + "-" + day.strftime("%m") + "-" + day.strftime("%d")
  return yesterday

def get_county_data(day):
  url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
  ftpstream = urllib.request.urlopen(url)
  csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
  for line in csvfile:
    if(line[DATE] == day and line[COUNTY] == county.title() and line[STATE] == state.title()):
      if(line[COUNTY] == "New York City"):
        line[FIPS] = '36061'
      return line

def get_mask_use(fips):
  url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/mask-use/mask-use-by-county.csv"
  ftpstream = urllib.request.urlopen(url)
  csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
  for line in csvfile:
    if(line[0] == fips):
      return line

def get_pop_data(county1, state1):
  url = "https://raw.githubusercontent.com/YashRavipati1/HelixHacks/master/Copy%20of%20co-est2019-alldata-2.csv"
  ftpstream = urllib.request.urlopen(url)
  csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
  if(county1 == "New York City"):
        return str(8065035)
  else:
    for line in csvfile:
      if(line[5] == state1 and county1 in line[6]):
          return line[POPULATION]

def get_secondary_attack():
  secondary_attack_rate = (int(current_cases[CASES]) - int(yesterday_cases[CASES])) / (int(yesterday_cases[CASES])*7)

  return secondary_attack_rate

def get_susceptibility():
  uninfected = int(total_pop) - float(current_cases[CASES])
  susceptible = uninfected * (1 - float(mask_usage[ALWAYS]) - 0.5*float(mask_usage[FREQUENTLY]))
  susceptibility = susceptible / int(total_pop)
  return susceptibility

def get_B():
  B = get_secondary_attack() / susceptibility_frac
  return B

def get_reproduction_ratio():
  risk = get_B() / removal_rate
  return risk

def get_threshold():
  if (risk1 <= 0.3):
    return 'Low Risk'
  elif (0.3 < risk1 <= 0.7):
    return 'Semi Risk'
  elif (0.7 < risk1 <= 1):
    return 'Risky'
  else:
    return 'Very Risky'

current_time = get_time()
yesterday_time = get_yesterday()
current_cases = get_county_data(current_time)
mask_usage = get_mask_use(current_cases[FIPS])
yesterday_cases = get_county_data(yesterday_time)
total_pop = get_pop_data(county.title(), state.title())
susceptibility_frac = get_susceptibility()
removal_rate = 0.1
risk1 = get_reproduction_ratio()
risklevel = get_threshold()



  
