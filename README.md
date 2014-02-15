NMEA0183
========

NMEA0183 is a python script that enables connection to serial NMEA0183 devices and interpretation of incoming data.

There are other python NMEA0183 scripts available, but this one is aiming to provide a more wholistic approach to the task. Most of the scripts do not provide a means of connecting to actual NMEA device. This one does. 

Usually, a knowledge of the incoming sentences is also required. With this script, incoming data is stored in variable 'clusters' that group similar bits of data into easily understood sets.

This project is still incomplete. There are various NMEA data types still missing. I've basically included the ones I needed at the moment. More will be coming. It is not difficult to add additional data types if you'de like to do this yourself.

Requirements
------------

- pyserial is required for serial connections - http://pyserial.sourceforge.net/
- Requires a serial NMEA0183 device.


How to Use
----------

Here is an example of its use:
 
 ```python
import NMEA0183

serial_location = '/dev/ttyUSB0'
serial_baudrate = 4800
serial_timeout = 5

#Provides the required serial device info
nmea = NMEA0183(serial_location,serial_baudrate,serial_timeout)

#Starts the serial connection
nmea.start()

#Checks if there is a valid connection
if nmea.exit == False:
	print 'Connection!'
	
	#More info on data names below
	#Different data types require different devices...obviously...
	#Some examples...
	
	#GPS data
	print nmea.data_gps['lat']
	print nmea.data_gps['lon']
	
	#Depth data
	print nmea.data_depth['feet']
	
	#Weather data
	print nmea.data_weather['wind_angle']
	print nmea.data_weather['water_temp']
	
	print nmea.data_rudder['stbd_angle']

else:
	print 'No connection!'

 ```

Current NMEA Sentences
----------------------

- RMC : Provides GPS data. 

Data types: 

Latitude      - data_gps['lat']
Longitude     - data_gps['lon']
Speed         - data_gps['speed']
Track Angle   - data_gps['track']
UTC date/time - data_gps['utc']
Status        - data_gps['status']

