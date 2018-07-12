# PillDispenser

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/V9uTrwy9Qtg/0.jpg)](https://www.youtube.com/watch?v=V9uTrwy9Qtg)

This project was completed as part of a Cornerstone of Engineering project at Northeastern University.
Participating members were Matthew Swenson, Oscar Chen, and myself.

We were tasked with creating a robotic device that met a need. To this we crafted an automatic pill dispenser.
The pill dispenser hosts a webpage that the doctor or caretaker can access and input three different pills, how many need to be dispensed, and when they will be dispensed. This data is then displayed on a small screen on the device so the patient can view when their pills are. An added feature is the dispensing of water with the pills to remove all excuses of not taking pills. The compartment containg the pills is also locked to prevent the abuse of pills.

Additionally, an Alexa Skill was created where the user can ask when the pills will be dispensed and Alexa will respond accordingly. 

Physical Components used were:
  3 Continuous rotation Servos,
  1 180 degree Servo,
  A Neopixel Light Strip,
  Sparkfun Redboard,
  Protoboard,
  Arduino Micro,
  Raspberry Pi 3,
  2.8" GPIO Controlled Touch Scrren for the Raspberry Pi,
  Water Balloon Valve,
  Wood,
  Hotglue,
  Stain (Dark Chestnut),
  Velcro,
  Acrylic Strips,
  Wire,
  
In terms of Software...
  All the above code was used and implemented onto the Raspberry Pi. A tunneling service known as pagekite was used to host both the doctor   end of the dispenserServer.py and the AlexaSkill.py. Additional libraries include datetime, time, serial, flask, flask-ask, requests, and   Beautiful Soup.
  
  The actual code behind the device is a little more complex.  The foundation/main file was called dispenserServer.py. This is what the doctor/care-taker would access to put in the name of the pill and when it will dispense. In this file there is also a counting/gravity sort algorithm so if the times were entered in a different order it would automatically fix itself. This was run on localhost port 80. 

The next program is arduinoController.py. The issue we ran into was figuring out how to communicate between different python files that were using Flask to run continuously. Our solution was to scrape the website that the doctor used to enter the pills. So using BeautifulSoup the website was scraped and the data was put into separate lists. This file also used the datetime library to compare the current time of the machine to the time entered. Once the current time reached the proper time the Raspberry Pi sent a string of what motors to turn on and how many pills would need to be dispensed using the Serial library. This data was then sent to an Arduino Uno over the USB. 

Ah but what does the client see? On the touchscreen (which ended up not working due to it being a non genuine piTFT), another html page was displayed in kiosk mode on the pi. This was run through clientview.py which also scraped the doctor page and hosted using Flask on localhost port 5555.

Yet another file, AlexaSkill.py, scraped the main page and creates a speech file using Flask-Ask which gets sent to Amazon and hosted on a custom skill.

One of the biggest problems faced was due to Northeastern's private network. Essentially, this made it impossible to access the doctor page as one would do in a local home setting. In practice, one could just type in the IP address and the port (192.168.X.X:80 or whatever it may be). But security? So this could not be done over the schools wifi. Now is where tunneling comes in handy. The service pagekite allowed us to tunnel behind some firewalls and host the localhost onto a public domain. We used this service for both the Alexa Skill and for the doctor access page. This meant that when the device was plugged in, we could go to http://display.combros.pagekite.me and be brought to the desired page. However, Northeastern blocked this too! (Thanks NU) The solution was to grab a VPN chrome extension and bypass some restrictions. (Shhh)
