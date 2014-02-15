NMEA0183
========

NMEA0183 is a python script that enables connection to serial NMEA0183 devices and interpretation of incoming data.

There are other python NMEA0183 scripts available, but this one is aiming to provide a more wholistic approach to the task. Most of the scripts do not provide a means of connecting to actual NMEA device. This one does. 

Usually, a knowledge of the incoming sentences is also required. With this script, incoming data is stored in variable 'clusters' that group similar bits of data into easily understood sets.


Requirements
------------

- pyserial is required for serial connections - http://pyserial.sourceforge.net/
- Requires a serial NMEA0183 device.


How to Use
------------

 
 ```python
import NMEA0183
 ```
