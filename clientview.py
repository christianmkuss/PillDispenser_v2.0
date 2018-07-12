from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

URL = "0.0.0.0:80"  # Get the website data from the URL which is hosted locally


@app.route("/")
def main():
    # Create a list for hours and minutes of each pill and how many pills and a string for each pill name
    pill1_name = ''
    pill1_hour_list = []
    pill1_minute_list = []
    pill1_num = []

    pill2_hour_list = []
    pill2_minute_list = []
    pill2_name = ''
    pill2_num = []

    pill3_hour_list = []
    pill3_minute_list = []
    pill3_name = ''
    pill3_num = []

    pill4_name = ''
    pill4_hour_list = []
    pill4_minute_list = []
    pill4_num = []

    pill5_hour_list = []
    pill5_minute_list = []
    pill5_name = ''
    pill5_num = []

    pill6_hour_list = []
    pill6_minute_list = []
    pill6_name = ''
    pill6_num = []

    # Open the html page for scraping
    r = requests.get("http://0.0.0.0:80")

    # Grab and transcribe the raw html using Beautiful Soup
    data = r.content
    page_soup = BeautifulSoup(data, "html.parser")

    # Find and store all the time elements on the web page
    pill1 = page_soup.findAll("td", {"class": "pill1Time"})
    pill2 = page_soup.findAll("td", {"class": "pill2Time"})
    pill3 = page_soup.findAll("td", {"class": "pill3Time"})
    pill4 = page_soup.findAll("td", {"class": "pill4Time"})
    pill5 = page_soup.findAll("td", {"class": "pill5Time"})
    pill6 = page_soup.findAll("td", {"class": "pill6Time"})

    pill1_name = page_soup.find("p", {"id": "pill1name"}).text
    pill2_name = page_soup.find("p", {"id": "pill2name"}).text
    pill3_name = page_soup.find("p", {"id": "pill3name"}).text
    pill4_name = page_soup.find("p", {"id": "pill4name"}).text
    pill5_name = page_soup.find("p", {"id": "pill5name"}).text
    pill6_name = page_soup.find("p", {"id": "pill6name"}).text

    numpill1 = page_soup.findAll("td", {"class": "pill1num"})
    numpill2 = page_soup.findAll("td", {"class": "pill2num"})
    numpill3 = page_soup.findAll("td", {"class": "pill3num"})
    numpill4 = page_soup.findAll("td", {"class": "pill4num"})
    numpill5 = page_soup.findAll("td", {"class": "pill5num"})
    numpill6 = page_soup.findAll("td", {"class": "pill6num"})

    # Loop through all elements in the list of pill times and store them in lists
    for x in range(len(pill1)):
        # Add the number of pills in the list
        pill1_num.append(int(numpill1[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill1[x].text.split()
        pill1_hour_list.append(this_time[0])
        pill1_minute_list.append(this_time[2])

    for x in range(len(pill2)):
        # Add the number of pills in the list
        pill2_num.append(int(numpill2[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill2[x].text.split()
        pill2_hour_list.append(this_time[0])
        pill2_minute_list.append(this_time[2])

    for x in range(len(pill3)):
        # Add the number of pills in the list
        pill3_num.append(int(numpill3[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill3[x].text.split()
        pill3_hour_list.append(this_time[0])
        pill3_minute_list.append(this_time[2])

    for x in range(len(pill4)):
        # Add the number of pills in the list
        pill4_num.append(int(numpill4[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill4[x].text.split()
        pill4_hour_list.append(this_time[0])
        pill4_minute_list.append(this_time[2])

    for x in range(len(pill5)):
        # Add the number of pills in the list
        pill5_num.append(int(numpill5[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill5[x].text.split()
        pill5_hour_list.append(this_time[0])
        pill5_minute_list.append(this_time[2])

    for x in range(len(pill6)):
        # Add the number of pills in the list
        pill6_num.append(int(numpill6[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill6[x].text.split()
        pill6_hour_list.append(this_time[0])
        pill6_minute_list.append(this_time[2])

    templateData = {
        'pill1_hour_list': pill1_hour_list,
        'pill1_minute_list': pill1_minute_list,
        'Pill1_Name': pill1_name,
        'pill1_num': pill1_num,

        'pill2_hour_list': pill2_hour_list,
        'pill2_minute_list': pill2_minute_list,
        'pill2_name': pill2_name,
        'pill2_num': pill2_num,

        'pill3_hour_list': pill3_hour_list,
        'pill3_minute_list': pill3_minute_list,
        'pill3_name': pill3_name,
        'pill3_num': pill3_num,

        'pill4_hour_list': pill4_hour_list,
        'pill4_minute_list': pill4_minute_list,
        'Pill4_Name': pill4_name,
        'pill4_num': pill4_num,

        'pill5_hour_list': pill5_hour_list,
        'pill5_minute_list': pill5_minute_list,
        'pill5_name': pill5_name,
        'pill5_num': pill5_num,

        'pill6_hour_list': pill6_hour_list,
        'pill6_minute_list': pill6_minute_list,
        'pill6_name': pill6_name,
        'pill6_num': pill6_num
    }

    # Render the template with the data above and the file clientview.html
    return render_template('clientview.html', **templateData)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
