from bs4 import BeautifulSoup
import RPi.GPIO as GPIO
import requests
import datetime
import serial
import time
import os
import subprocess

# Will communicate to the Arduino using the serial library over usb
arduinoSerialData = serial.Serial('/dev/ttyUSB0', 9600)

# Setting up the pins for the motors
GPIO.setmode(GPIO.BOARD)

# Which GPIO pin to which motor
waterMotor = 29
Servo1Pin = 31
Servo2Pin = 32
Servo3Pin = 33
Servo4Pin = 35
Servo5Pin = 36
Servo6Pin = 37

# Specify them as outputs
GPIO.setup(waterMotor, GPIO.OUT)
GPIO.setup(Servo1Pin, GPIO.OUT)
GPIO.setup(Servo2Pin, GPIO.OUT)
GPIO.setup(Servo3Pin, GPIO.OUT)
GPIO.setup(Servo4Pin, GPIO.OUT)
GPIO.setup(Servo5Pin, GPIO.OUT)
GPIO.setup(Servo6Pin, GPIO.OUT)

Servo1 = GPIO.PWM(Servo1Pin, 50)
Servo2 = GPIO.PWM(Servo2Pin, 50)
Servo3 = GPIO.PWM(Servo3Pin, 50)
Servo4 = GPIO.PWM(Servo4Pin, 50)
Servo5 = GPIO.PWM(Servo5Pin, 50)
Servo6 = GPIO.PWM(Servo6Pin, 50)

# Turn everything off
Servo1.start(0)
Servo2.start(0)
Servo3.start(0)
Servo4.start(0)
Servo5.start(0)
Servo6.start(0)
GPIO.output(waterMotor, GPIO.LOW)

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

    pill4_hour_list = []
    pill4_minute_list = []
    pill4_numpills = []

    pill5_hour_list = []
    pill5_minute_list = []
    pill5_numpills = []

    pill6_hour_list = []
    pill6_minute_list = []
    pill6_numpills = []

    # Get the website data from the URL
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

    numpill1 = page_soup.findAll("td", {"class": "pill1num"})
    numpill2 = page_soup.findAll("td", {"class": "pill2num"})
    numpill3 = page_soup.findAll("td", {"class": "pill3num"})
    numpill4 = page_soup.findAll("td", {"class": "pill4num"})
    numpill5 = page_soup.findAll("td", {"class": "pill5num"})
    numpill6 = page_soup.findAll("td", {"class": "pill6num"})

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

    for x in range(len(pill4)):
        # Add the number of pills in the list
        pill4_numpills.append(int(numpill4[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill4[x].text.split()
        pill4_hour_list.append(this_time[0])
        pill4_minute_list.append(this_time[2])

    for x in range(len(pill5)):
        # Add the number of pills in the list
        pill5_numpills.append(int(numpill5[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill5[x].text.split()
        pill5_hour_list.append(this_time[0])
        pill5_minute_list.append(this_time[2])

    for x in range(len(pill6)):
        # Add the number of pills in the list
        pill6_numpills.append(int(numpill6[x].text))

        # Split the pill times into hours and minutes and add to respective lists
        this_time = pill6[x].text.split()
        pill6_hour_list.append(this_time[0])
        pill6_minute_list.append(this_time[2])

    # Update the current time
    now = datetime.datetime.now()
    print(now)
    sleep = 0
    watering = False

    STEPS = 10  # the number of steps either side of nominal
    NOMINAL = 7.5  # the 'zero' PWM %age
    RANGE = 1.0  # the maximum variation %age above/below NOMINAL

    for x in range(len(pill1_hour_list)):
        # Compare the current hour to the hour in the list and the current minute to the minute in the list
        if now.hour == int(pill1_hour_list[x]) and now.minute == int(pill1_minute_list[x]):
            dutycycle = NOMINAL + (-1) * .5 * 20 / 10
            Servo1.ChangeDutyCycle(dutycycle)
            sleep += pill1_numpills[x] * 1.1
            time.sleep(pill1_numpills[x] * 1.1)
            Servo1.ChangeDutyCycle(0)
            # Allows you to see it actually working
            print("Dispensing Pill")
            watering = True

    for x in range(len(pill2_hour_list)):
        # Compare the current hour to the hour in the list and the current minute to the minute in the list
        if now.hour == int(pill2_hour_list[x]) and now.minute == int(pill2_minute_list[x]):
            dutycycle = NOMINAL + (-1) * .5 * 20 / 10
            Servo2.ChangeDutyCycle(dutycycle)
            sleep += pill1_numpills[x] * 1.1
            time.sleep(pill1_numpills[x] * 1.1)
            Servo2.ChangeDutyCycle(0)
            # Allows you to see it actually working
            print("Dispensing Pill")
            watering = True

    for x in range(len(pill3_hour_list)):
        # Compare the current hour to the hour in the list and the current minute to the minute in the list
        if now.hour == int(pill3_hour_list[x]) and now.minute == int(pill3_minute_list[x]):
            dutycycle = NOMINAL + (-1) * .5 * 20 / 10
            Servo3.ChangeDutyCycle(dutycycle)
            sleep += pill1_numpills[x] * 1.1
            time.sleep(pill1_numpills[x] * 1.1)
            Servo3.ChangeDutyCycle(0)
            # Allows you to see it actually working
            print("Dispensing Pill")
            watering = True

    for x in range(len(pill4_hour_list)):
        # Compare the current hour to the hour in the list and the current minute to the minute in the list
        if now.hour == int(pill4_hour_list[x]) and now.minute == int(pill4_minute_list[x]):
            dutycycle = NOMINAL + (-1) * .5 * 20 / 10
            Servo4.ChangeDutyCycle(dutycycle)
            sleep += pill1_numpills[x] * 1.1
            time.sleep(pill1_numpills[x] * 1.1)
            Servo4.ChangeDutyCycle(0)
            # Allows you to see it actually working
            print("Dispensing Pill")
            watering = True

    for x in range(len(pill5_hour_list)):
        # Compare the current hour to the hour in the list and the current minute to the minute in the list
        if now.hour == int(pill5_hour_list[x]) and now.minute == int(pill5_minute_list[x]):
            dutycycle = NOMINAL + (-1) * .5 * 20 / 10
            Servo5.ChangeDutyCycle(dutycycle)
            sleep += pill1_numpills[x] * 1.1
            time.sleep(pill1_numpills[x] * 1.1)
            Servo5.ChangeDutyCycle(0)
            # Allows you to see it actually working
            print("Dispensing Pill")
            watering = True

    for x in range(len(pill6_hour_list)):
        # Compare the current hour to the hour in the list and the current minute to the minute in the list
        if now.hour == int(pill6_hour_list[x]) and now.minute == int(pill6_minute_list[x]):
            dutycycle = NOMINAL + (-1) * .5 * 20 / 10
            Servo6.ChangeDutyCycle(dutycycle)
            sleep += pill1_numpills[x] * 1.1
            time.sleep(pill1_numpills[x] * 1.1)
            Servo6.ChangeDutyCycle(0)
            # Allows you to see it actually working
            print("Dispensing Pill")
            watering = True

    if watering:
        arduinoSerialData.write('y')
        sleep += 12
        GPIO.output(waterMotor, GPIO.HIGH)
        time.sleep(9)
        GPIO.output(waterMotor, GPIO.LOW)
        os.system('pills.mp3')
    else:
        arduinoSerialData.write('n')

    # This is dependent on how fast the machine is. For us it would generally take a second to run through the code
    time.sleep(60 - sleep)
