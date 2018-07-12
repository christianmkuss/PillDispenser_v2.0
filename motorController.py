from bs4 import BeautifulSoup
import RPi.GPIO as GPIO
import requests
import datetime
import serial
import time
import os

# Will communicate to the Arduino using the serial library over usb
arduinoSerialData = serial.Serial('/dev/ttyUSB0', 9600)

# Setting up the pins for the motors
GPIO.setmode(GPIO.BOARD)

# Which GPIO pin to which motor
waterMotor = 12
Motor1Pin = 16
Motor2Pin = 18
Motor3Pin = 22

# Specify them as outputs
Motor1 = GPIO.PWM(Motor1Pin, 50)
Motor2 = GPIO.PWM(Motor2Pin, 50)
Motor3 = GPIO.PWM(Motor3Pin, 50)
water = GPIO.PWM(waterMotor, 50)

# Turn everything off
Motor1.start(7.5)
Motor2.start(7.5)
Motor3.start(7.5)
water.start(7.5)

# We in this for the long haul
while True:

    pill1_hour_list = []
    pill1_minute_list = []
    pill1_numpills = []
    pill2_hour_list = []
    pill2_minute_list = []
    pill2_numpills = []
    pill3_hour_list = []
    pill3_minute_list = []
    pill3_numpills = []

    # Get the website data from the URL
    r = requests.get("http://0.0.0.0:80")
    
    # Grab and transcribe the raw html using Beautiful Soup
    data = r.content
    page_soup = BeautifulSoup(data, "html.parser")

    # Find and store all the time elements on the web page
    pill1 = page_soup.findAll("td", {"class": "pill1Time"})
    pill2 = page_soup.findAll("td", {"class": "pill2Time"})
    pill3 = page_soup.findAll("td", {"class": "pill3Time"})
    numpill1 = page_soup.findAll("td", {"class": "pill1num"})
    numpill2 = page_soup.findAll("td", {"class": "pill2num"})
    numpill3 = page_soup.findAll("td", {"class": "pill3num"})

    # Loop through all elements in the list of pill times and store them in lists
    for x in range(len(pill1)):
        # Add the number of pills in the list
        pill1_numpills.append(int(numpill1[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill1[x].text.split()
        pill1_hour_list.append(this_time[0])
        pill1_minute_list.append(this_time[2])

    for x in range(len(pill2)):
        # Add the number of pills in the list
        pill2_numpills.append(int(numpill2[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill2[x].text.split()
        pill2_hour_list.append(this_time[0])
        pill2_minute_list.append(this_time[2])

    for x in range(len(pill3)):
        # Add the number of pills in the list
        pill3_numpills.append(int(numpill3[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill3[x].text.split()
        pill3_hour_list.append(this_time[0])
        pill3_minute_list.append(this_time[2])

    # Update the current time
    now = datetime.datetime.now()
    print(now)
    sleep = 0
    watering = False
    for x in range(len(pill1_hour_list)):
        # Compare the current hour to the hour in the list and the current minute to the minute in the list
        if now.hour == int(pill1_hour_list[x]) and now.minute == int(pill1_minute_list[x]):
            Motor1.ChangeDutyCycle(10)
            sleep += pill1_numpills[x]*2.6
            time.sleep(pill1_numpills[x]*2.6)
            Motor1.ChangeDutyCycle(7.5)
            # Allows you to see it actually working
            print("Dispensing Pill")
            watering = True
    for x in range(len(pill2_hour_list)):
        # Compare the current hour to the hour in the list and the current minute to the minute in the list
        if now.hour == int(pill2_hour_list[x]) and now.minute == int(pill2_minute_list[x]):
            sleep += pill2_numpills[x] * 2.6
            Motor2.ChangeDutyCycle(10)
            time.sleep(pill2_numpills[x] * 2.6)
            Motor2.ChangeDutyCycle(7.5)
            # Allows you to see it actually working
            print("Dispensing Pill")
            watering = True
    for x in range(len(pill3_hour_list)):
        # Compare the current hour to the hour in the list and the current minute to the minute in the list
        if now.hour == int(pill3_hour_list[x]) and now.minute == int(pill3_minute_list[x]):
            Motor3.ChangeDutyCycle(10)
            sleep += pill3_numpills[x] * 2.6
            time.sleep(pill3_numpills[x] * 2.6)
            Motor3.ChangeDutyCycle(7.5)
            # Allows you to see it actually working
            print("Dispensing Pill")
            watering = True
    if watering:
        # Set the water servo to 0 degrees
        water.ChangeDutyCycle(2.5)
        arduinoSerialData.write('y')
        sleep += 8
        time.sleep(6)
        water.ChangeDutyCycle(7.5)
        os.system('pills.mp3')
    else:
        arduinoSerialData.write('n')

    # This is dependent on how fast the machine is. For us it would generally take a second to run through the code
    time.sleep(60-sleep)
