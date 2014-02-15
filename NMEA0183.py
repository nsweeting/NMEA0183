#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import serial
import binascii
from threading import Thread


class NMEA0183():


	def __init__(self, location, baud_rate, timeout):
		'''
		Initiates variables.
		
		Keyword arguments:
		location -- the location of the serial connection
		baud_rate -- the baud rate of the connection
		timeout -- the timeout of the connection
		
		'''
		self.exit = False
		self.location = location
		self.baud_rate = baud_rate
		self.timeout = timeout
		self.serial_dev = None
		self.serial_data = None

		#Ready the GPS variables
		self.data_gps = {'lat': float(0.0), 'lon': float(0.0), 'speed': float(0.0), 'track': float(0.0), 'utc': '0.0', 'status': 'A'}
		#Ready the depth variables
		self.data_depth = {'feet': float(0.0), 'meters': float(0.0), 'fathoms': float(0.0), 'offset': float(0.0)}
		#Ready the weather variables
		self.data_weather = {'wind_angle': float(0.0), 'wind_ref': 'R', 'wind_speed': float(0.0), 'wind_unit': 'K', 'water_temp': float(0.0), 'water_unit': 'C', 'air_temp': float(0.0), 'air_unit': 'C'}
		#Ready the rudder variables
		self.data_rudder = {'stdb_angle': float(0.0), 'stdb_status': 'A', 'port_angle': float(0.0), 'port_status': 'A'}
		#Ready the turn variables
		self.data_turn = {'rate': float(0.0), 'status': 'A'}

	def start(self):
		'''
		Creates a thread to read serial connection data.
		'''
		self.serial_dev = serial.Serial(self.location, self.baud_rate, self.timeout)
		serial_thread = Thread(None,self.read_thread,None,())
		serial_thread.start()

	def read_thread(self):
		'''
		The thread used to read incoming serial data.
		'''
		dat_new = ''
		dat_old = ''
		#Loops until the connection is broken, or is instructed to quit
		try:
			while self.is_open():
				#Instructed to quit
				if self.exit: 
					break
				if dat_new: 
					dat_old = dat_new
					dat_new = ''
				dat_old = dat_old + self.buffer()
				if re.search("\r\n", dat_old):
					try:
						self.serial_data, dat_new = dat_old.split("\r\n")
					except:
						pass
					#The checksum is correct, so the data will be deconstructed
					if self.checksum(self.serial_data):
						self.check_type()
					dat_old = ''
		except:
			self.quit()

	def is_open(self):
		'''
		Checks whether the serial connection is still open.
		'''
		return self.serial_dev.isOpen()

	def buffer(self):
		'''
		Creates a buffer for serial data reading. Avoids reading lines for better performance.
		'''
		dat_cur = self.serial_dev.read(1)
		x = self.serial_dev.inWaiting()
		if x: dat_cur = dat_cur + self.serial_dev.read(x)
		return dat_cur

	def make_checksum(self,data):
		'''
		Calculates a checksum from a NMEA sentence.
		
		Keyword arguments:
		data -- the NMEA sentence to create
		
		'''
		csum = 0
		i = 0
		# Remove ! or $ and *xx in the sentence
		data = data[1:data.rfind('*')]
		while (i < len(data)):
			input = binascii.b2a_hex(data[i])
			input = int(input,16)
			#xor
			csum = csum ^ input
			i += 1
		return csum

	def checksum(self,data):
		'''
		Reads the checksum of an NMEA sentence.
		
		Keyword arguments:
		data -- the NMEA sentence to check
		
		'''
		try:
			# Create an integer of the two characters after the *, to the right
			supplied_csum = int(data[data.rfind('*')+1:data.rfind('*')+3], 16)
		except:
			return ''
		# Create the checksum
		csum = self.make_checksum(data)
		# Compare and return
		if csum == supplied_csum:
			return True
		else:
			return False

	def check_type(self):
		'''
		Reads the sentence type, and directs the data to its respective function.
		'''
		self.serial_data = self.serial_data.split('*')
		#Splits up the NMEA data by comma
		self.serial_data = self.serial_data[0].split(',')
		#Incoming serial data is GPS related
		if self.serial_data[0][3:6] == 'RMC':
			self.nmea_rmc()
		#Incoming serial data is depth related
		elif self.serial_data[0][3:6] in ('DBS','DBT', 'DBK'):
			self.nmea_dbs()
		#Incoming serial data is depth related
		elif self.serial_data[0][3:6] == 'DPT':
			self.nmea_dpt()
		#Incoming serial data is weather related
		elif self.serial_data[0][3:6] == 'MWV':
			self.nmea_mwv()
		#Incoming serial data is weather related
		elif self.serial_data[0][3:6] == 'MTW':
			self.nmea_mtw()
		#Incoming serial data is weather related
		elif self.serial_data[0][3:6] == 'MTA':
			self.nmea_mta()
		#Incoming serial data is rudder related
		elif self.serial_data[0][3:6] == 'RSA':
			self.nmea_rsa()
		#Incoming serial data is turn related
		elif self.serial_data[0][3:6] == 'ROT':
			self.nmea_rot()
		elif self.serial_data[0][3:6] == 'XDR':
			self.nmea_rot()

	def nmea_rmc(self):
		'''
		Deconstructs NMEA gps readings.
		'''
		self.data_gps['utc'] = self.gps_nmea2utc()
		self.data_gps['status'] = self.serial_data[2]
		self.data_gps['lat'] = self.gps_nmea2dec(0)
		self.data_gps['lon'] = self.gps_nmea2dec(1)
		self.data_gps['speed'] = float(self.serial_data[7])
		self.data_gps['track'] = float(self.serial_data[8])

	def nmea_dbs(self):
		'''
		Deconstructs NMEA depth readings.
		'''
		self.data_depth['feet'] = self.serial_data[1]
		self.data_depth['meters'] = self.serial_data[3]
		self.data_depth['fathoms'] = self.serial_data[5]
		self.data_depth['offset'] = 0

	def nmea_dpt(self):
		'''
		Deconstructs NMEA depth readings.
		'''
		self.data_depth['meters'] = self.serial_data[1]
		self.data_depth['offset'] = self.serial_data[2]

	def nmea_mwv(self):
		'''
		Deconstructs NMEA weather readings.
		'''
		self.data_weather['wind_angle'] = self.serial_data[1]
		self.data_weather['wind_ref'] = self.serial_data[2]
		self.data_weather['wind_speed'] = self.serial_data[3]
		self.data_weather['wind_unit'] = self.serial_data[4]

	def nmea_mtw(self):
		'''
		Deconstructs NMEA water readings.
		'''
		self.data_weather['water_temp'] = self.serial_data[1]
		self.data_weather['water_unit'] = self.serial_data[2]

	def nmea_mta(self):
		'''
		Deconstructs NMEA air temp readings.
		'''
		self.data_weather['air_temp'] = self.serial_data[1]
		self.data_weather['air_unit'] = self.serial_data[2]

	def nmea_rsa(self):
		'''
		Deconstructs NMEA rudder angle readings.
		'''
		self.data_rudder['stbd_angle'] = self.serial_data[1]
		self.data_rudder['stdb_status'] = self.serial_data[2]
		self.data_rudder['port_angle'] = self.serial_data[3]
		self.data_rudder['port_status'] = self.serial_data[4]

	def nmea_rot(self):
		'''
		Deconstructs NMEA rudder angle readings.
		'''
		self.data_turn['rate'] = self.serial_data[1]
		self.data_turn['status'] = self.serial_data[2]

	def nmea_xdr(self):
		'''
		Deconstructs NMEA weather readings.
		'''
		if self.serial_data[0][0:2] == '$WI':
			self.data_weather['wind_angle'] = self.serial_data[1]
			self.data_weather['wind_ref'] = self.serial_data[2]
			self.data_weather['wind_speed'] = self.serial_data[3]
			self.data_weather['wind_unit'] = self.serial_data[4]

	def gps_nmea2dec(self,type):
		'''
		Converts NMEA lat/long format to decimal format.
		
		Keyword arguments:
		type -- tells whether it is a lat or long. 0=lat,1=long
		
		'''
		#Represents the difference in list position between lat/long
		x = type*2
		#Converts NMEA format to decimal format
		data = float(self.serial_data[3+x][0:2+type]) + float(self.serial_data[3+x][2+type:9+type])/60
		#Adds negative value based on N/S, W/E
		if self.serial_data[4+x] == 'S': data = data*(-1)
		elif self.serial_data[4+x] == 'W': data = data*(-1)
		return data

	def gps_nmea2utc(self):
		'''
		Converts NMEA utc format to more standardized format.
		'''
		time = self.serial_data[1][0:2] + ':' + self.serial_data[1][2:4] + ':' + self.serial_data[1][4:6]
		date = '20' + self.serial_data[9][4:6] + '-' + self.serial_data[9][2:4] + '-' + self.serial_data[9][0:2]
		return date + 'T' + time + 'Z'

	def quit(self):
		'''
		Enables quiting the serial connection.
		'''
		self.exit = True
