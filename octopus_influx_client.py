#
# Class for reading and writing Influxdb data
#
# Copyright (C) 2020 Steve Upton
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the license, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS TO A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this progeam; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

from datetime import datetime
from datetime import timezone
from influxdb import InfluxDBClient
#from influxdb.client.write_api import SYNCHRONOUS


class OctopusInfluxClient(object):
	INFLUX_URL='http://blaise:8086'
#	class DataUnavailable(Exception):

	# 
	def __init__(self, host, port, token, org_name, bucket_name):
		#self.token = token
		username = 'admin'
		password = 'admin'
		token = f'{username}:{password}'
		self.org_name = org_name
		self.bucket_name = bucket_name
#		client = InfluxDBClient(url=self.INFLUX_URL, token=token, org=org_name, debug=False)
#		client = InfluxDBClient(url=self.INFLUX_URL, token=f'{username}:{password}', org='-')
		self.client = InfluxDBClient(host=host, port=port) 

#		self.write_client = client.write_api(write_options=SYNCHRONOUS)
#		self.query_client = client.query_api()
		
		self.client.create_database("devdb")
		self.client.switch_database("devdb")
	
	#
	# Write a Point to the database
	#
	def write_electricity_usage_point(self, p):
		self.write_client.write(self.bucket_name, record=p)

	#
	# Write a record to the influx database
	#
	def write_record(self, octopus_record):
		self.client.write_points(octopus_record)

	#
	# Get the last record, so that any later data can be requested from Octopus
	#
	def get_last_electricity_usage_record(self):	# Get the last record that was written
		#record = self.query_client.query("SELECT consumption from electricity_usage")
		
##		query='from(bucket:"devdb") |> range(start: 0, stop: now()) |> filter(fn: (r) => r._measurement == "electricity_usage") |> last()'
##		result = self.query_client.query(query=query)
		query = 'SELECT "consumption" FROM "electricity_usage"'
		result = self.client.query(query)

		#for table in result:
			#print(table)
			#for record in table.records:
				#print(record.get_measurement(),record.get_time(),record.get_field(), record.get_value())
		#print(table.get_group_key())
		return result
	
	#
	# Get the time for the alst usage record	
	def get_last_electricity_usage_time(self):	# Get the last record timestamp that was written
		result = self.get_last_electricity_usage_record()
		last_time = "1970-01-01T00:00:00"
		for table in result:
			for record in table.records:
				last_time = record.get_time()
		#print(table.get_group_key())
		
		return last_time

# write_electricity_cost_data():