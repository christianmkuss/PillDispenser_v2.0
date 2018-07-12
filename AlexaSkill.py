from flask import Flask
from flask_ask import Ask, statement, convert_errors
import logging
import requests
from bs4 import BeautifulSoup

# Some initial setup for an Alexa skill using Flask-Ask
app = Flask(__name__)
ask = Ask(app, '/')

# To determine the correct grammar
# #SorryForUsingGlobalVariables
first = True

# No idea what this does
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


# A function to turn the lists into strings
def string_from_lists(hourlist, minutelist, am_or_pm, pill_name):
    # Yes I am using a global variable
    global first

    # initialize empty string
    pills = ''

    # Some loops to throw everything into speech format
    for x in range(len(hourlist)):
        if hourlist[x] > 12:
            # You don't say 15 o'clock
            hourlist[x] %= 12
            am_or_pm.append(' PM ')
        else:
            am_or_pm.append(' AM ')
        if first:
            # Basically this is necessary so Alexa doesn't say "You have and ..."
            pills = str(hourlist[x]) + ' ' + str(minutelist[x]) + am_or_pm[x]
            first = False
        else:
            # Now you use "and ..."
            pills += ' and ' + str(hourlist[x]) + ' ' + str(minutelist[x]) + am_or_pm[x]
    # Tell them what pill and when"
    return pill_name + ' at ' + pills + '. '


# The intent name goes into the quotations
@ask.intent('GPIOControlIntent', mapping={})
def gpio_control():
    # Create the output speech string, the lists to store the scrapings, and a list for am or pm
    global first
    pills = ''
    pill1_hour_list = []
    pill1_minute_list = []
    pill2_hour_list = []
    pill2_minute_list = []
    pill3_hour_list = []
    pill3_minute_list = []
    am_or_pm = []

    # Open the local host port 80 for scraping
    r = requests.get("http://0.0.0.0:80")

    # Grab and transcribe the raw html using Beautiful Soup
    data = r.content
    page_soup = BeautifulSoup(data, "html.parser")

    # Attempt to scrape everything
    try:
        pill1 = page_soup.findAll("td", {"class": "pill1Time"})
        pill2 = page_soup.findAll("td", {"class": "pill2Time"})
        pill3 = page_soup.findAll("td", {"class": "pill3Time"})
        pill1name = page_soup.find("p", {"id": "pill1name"}).text
        pill2name = page_soup.find("p", {"id": "pill2name"}).text
        pill3name = page_soup.find("p", {"id": "pill3name"}).text

        # Loop through all elements in the list of pill times and store them in lists
        for element in pill1:
            this_time = element.text.split()
            pill1_hour_list.append(int(this_time[0]))
            pill1_minute_list.append(int(this_time[2]))

        for element in pill2:
            this_time = element.text.split()
            pill2_hour_list.append(int(this_time[0]))
            pill2_minute_list.append(int(this_time[2]))

        for element in pill3:
            this_time = element.text.split()
            pill3_hour_list.append(int(this_time[0]))
            pill3_minute_list.append(int(this_time[2]))

        # If there are no pills when asked tell them that
        if len(pill1_hour_list) == 0 and len(pill2_hour_list) == 0 and len(pill3_hour_list) == 0:
            return statement('You have no pills')

        # If any of the pills have times to dispense go to the function and determine the speech output
        if len(pill1_hour_list) > 0:
            first = True
            pills += string_from_lists(pill1_hour_list, pill1_minute_list, am_or_pm, pill1name)
        if len(pill2_hour_list) > 0:
            first = True
            pills += string_from_lists(pill2_hour_list, pill2_minute_list, am_or_pm, pill2name)
        if len(pill3_hour_list) > 0:
            first = True
            pills += string_from_lists(pill3_hour_list, pill3_minute_list, am_or_pm, pill3name)

        # Return the statement of the pills formatted with the correct speech
        return statement('You have {}'.format(pills))
    # If it doesn't work say we have an error
    except Exception as e:
        return statement('There was an error')


if __name__ == '__main__':
    # We will host this one on port 5000
    app.run(host='0.0.0.0', port=5000)
