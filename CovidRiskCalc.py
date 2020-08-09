import csv
import urllib.request
import codecs
import datetime
import tkinter as tk

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

#state = input("enter state: ")
#county = input("enter county: ")
removal_rate = 0.1

# date = input("Enter in the date you want to look at: ")

activities = [
    "Opening the mail",
    "Getting restaurant takeout",
    "Pumping gasoline",
    "Playing tennis",
    "Going camping",
    "Grocery shopping",
    "Going for a walk , run , or bike ride with others",
    "Playing golf Staying at a hotel for two nights",
    "Sitting in a doctor's waiting room",
    "Going to a library or museum",
    "Eating in a restaurant ( outside )",
    "Walking in a busy downtown",
    "Spending an hour at a playground",
    "Having dinner at someone else's house",
    "Attending a backyard barbecue",
    "Going to a beach",
    "Shopping at a mall",
    "Sending kids to school , camp , or day care",
    "Working a week in an office building",
    "Swimming in a public pool",
    "Visiting an elderly relative or friend in their home",
    "Going to a hair salon or barbershop",
    "Eating in a restaurant ( inside )",
    "Attending a wedding or funeral",
    "Traveling by plane" "Playing basketball",
    "Playing football",
    "Hugging or shaking hands when greeting a friend",
    "Eating at a buffet",
    "Working out at gym",
    "Going to an amusement park",
    "Going to a movie theater",
    "Attending a large music concert",
    "Going to a sports stadium",
    "Attending a religious service with 500+ worshipers",
    "Going to a bar",
    "Other"
]

def get_time():
    now = datetime.date.today()
    day = now - datetime.timedelta(days=1)
    today = "20" + day.strftime("%y") + "-" + day.strftime("%m") + "-" + day.strftime("%d")
    return today


def get_yesterday():
    now = datetime.date.today()
    day = now - datetime.timedelta(days=8)
    yesterday = "20" + day.strftime("%y") + "-" + day.strftime("%m") + "-" + day.strftime("%d")
    return yesterday


def get_county_data(day):
    url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
    ftpstream = urllib.request.urlopen(url)
    csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
    for line in csvfile:
        if (line[DATE] == day and line[COUNTY] == county.title() and line[STATE] == state.title()):
            if (line[COUNTY] == "New York City"):
                line[FIPS] = '36061'
            return line


def get_mask_use(fips):
    url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/mask-use/mask-use-by-county.csv"
    ftpstream = urllib.request.urlopen(url)
    csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
    for line in csvfile:
        if (line[0] == fips):
            return line


def get_pop_data(county1, state1):
    url = "https://raw.githubusercontent.com/YashRavipati1/HelixHacks/master/Copy%20of%20co-est2019-alldata-2.csv"
    ftpstream = urllib.request.urlopen(url)
    csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
    if (county1 == "New York City"):
        return str(8065035)
    else:
        for line in csvfile:
            if (line[5] == state1 and county1 in line[6]):
                return line[POPULATION]


def get_secondary_attack():
    secondary_attack_rate = (int(current_cases[CASES]) - int(yesterday_cases[CASES])) / (
                int(yesterday_cases[CASES]) * 7)

    return secondary_attack_rate


def get_susceptibility():
    uninfected = int(total_pop) - float(current_cases[CASES])
    susceptible = uninfected * (1 - float(mask_usage[ALWAYS]) - 0.5 * float(mask_usage[FREQUENTLY]))
    susceptibility = susceptible / int(total_pop)
    return susceptibility


def get_B():
    B = get_secondary_attack() / susceptibility_frac
    return B

def get_reproduction_ratio(scaling_factor):
    risk = scaling_factor * (get_B() / removal_rate)
    return risk

def get_scale(choice):
   ci = activities.index(choice)
   if choice in activities:
       if 0 <= ci <= 4:
           return 0.4  # low risk
       elif 5 <= ci <= 13:
           return 0.6  # low-moderate
       elif 14 <= ci <= 21:
           return 0.8  # moderate
       elif 22 <= ci <= 28:
           return 1  # moderate high
       elif 29 <= ci <= 34:
           return 1.4  # high
       elif ci == 35:
           return 1.0

   return ci

def get_threshold():
    if (risk1 <= 0.3):
        return "You are highly unlikely to contract the virus, you should still wear masks and wash\n your hands nevertheless!"
    elif (0.3 < risk1 <= 0.7):
        return "You are unlikely to contract the virus, however you should definitely wear masks and wash\n your hands nevertheless!"
    elif (0.7 < risk1 <= 1):
        return "You are at risk of contracting the virus, please  wear masks and wash your hands to \nslow its spread! Try to limit how much you go outside"
    else:
        return "You are likely to contract the virus if you go outside. Only go outside for necessities.\n Make sure you wear a mask and wash your hands."

def run(s, c, l):
    try:
        global state
        state = s
        global county
        county = c
        global current_time
        current_time = get_time()
        global yesterday_time
        yesterday_time = get_yesterday()
        global current_cases
        current_cases = get_county_data(current_time)
        global mask_usage
        mask_usage = get_mask_use(current_cases[FIPS])
        global yesterday_cases
        yesterday_cases = get_county_data(yesterday_time)
        global total_pop
        total_pop = get_pop_data(county.title(), state.title())
        global susceptibility_frac
        susceptibility_frac = get_susceptibility()
        global scale
        scale = get_scale(l)
        global risk1
        risk1 = get_reproduction_ratio(scale)
        return get_threshold()
    except:
        return "Data not found. Try checking your spelling and don't use the word county when\n entering you county name"




