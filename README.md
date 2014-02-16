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
	
	#Rudder data
	print nmea.data_rudder['stbd_angle']
	
	#Quit the NMEA connection
	nmea.quit()

else:
	print 'No connection!'

 ```

Current NMEA Sentences
----------------------

##### GPS Data
- Latitude in decimal format = data_gps['lat']
- Longitude in decimal format = data_gps['lon']
- Speed in knots = data_gps['speed']
- Course track in degrees = data_gps['track']
- UTC in standard format, ie. 1994-11-05T13:15:30Z = data_gps['utc']
- Status, A is Valid, V is Invalid = data_gps['status']

##### Depth Data
You must understand the source of the depth data, as it could be coming from a waterline reading, or below waterline reading. 

- Depth in feet = data_depth['feet']
- Depth in meters = data_depth['meters']
- Depth in fathoms = data_depth['fathoms']
- Depth offset, positive is transducer to waterline, negative is transducer to keel = data_depth['offset']

##### Weather Data

- Wind angle = data_weather['wind_angle']
- Wind reference, R is relative, T is true = data_weather['wind_ref']
- Wind speed = data_weather['wind_speed']
- Wind unit, K/M/N = data_weather['wind_unit']
- Water temp = data_weather['water_temp']
- Water unit, C/F = data_weather['water_unit']
- Air temp = data_weather['air_temp']
- Air unit, C/F = data_weather['air_unit']

##### Rudder Data

- Starboard (or single) rudder angle = data_rudder['stdb_angle']
- Starboard (or single) status, A is valid, V is invalid = data_rudder['stdb_status']
- Port rudder angle = data_rudder['port_angle']
- Port status, A is valid, V is invalid = data_rudder['port_status']

