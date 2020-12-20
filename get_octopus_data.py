#
# Script to manage the extraction of data from Octopus Energy and handling the data returned
#
# TODO:
# - Allow and manage command line parameters
# - Pull data for Agile rate from Octopus and send to Influxdb
#
# Derived from: https://gist.github.com/codeinthehole/5f274f46b5798f435e6984397f1abb64
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
 
import requests
import config
from requests.exceptions import HTTPError
import json
from datetime import datetime
from datetime import timezone
from influxdb import InfluxDBClient

from octopus_client import OctopusAPIClient
from octopus_influx_client import OctopusInfluxClient

octoclient = OctopusAPIClient(config.API_KEY)
influxclient = OctopusInfluxClient(config.INFLUX_HOST, config.INFLUX_PORT, config.token, config.org_name, config.bucket_name)

#
# Get the latest usage data from Octopus
#
def pull_latest_usage_data():
	p = {
		"period_from":"2020-09-25T21:31:00+01:00",
		"period_to":"2020-09-25T21:59:00+01:00"
	}

	# Get the last entry
	last_time = influxclient.get_last_electricity_usage_time()

	print(last_time)
	# Get the data since the last entry
	#o_data = octoclient.electricity_meter_consumption(config.MPAN, config.SERIAL, period_from="2020-09-25T21:31:00+01:00",period_to="2020-09-25T21:59:00+01:00");


	o_data = octoclient.electricity_meter_consumption(config.MPAN, config.SERIAL, period_from="2020-09-07T00:00:00",period_to="2020-10-13T00:00:00")
	
	octopus_record = [
		{
			"measurement": config.measurement_name,
			"tags": {
				"interval_start": 0,
				"interval_end": 0
			},
			"time": 0,
			"fields": {}
		}
	]

	for result in o_data["results"]:
#		p = Point(config.measurement_name)
# 			.tag("interval_start",result["interval_start"]).tag("interval_end",result["interval_end"])
# 			.field("consumption",result["consumption"]).time(result["interval_start"])
#		influxclient.write_electricity_usage_point(p)
		print(result)
		tags = octopus_record[0]["tags"]
		tags["interval_start"] = result["interval_start"]
		tags["interval_end"] = result["interval_end"]
		octopus_record[0]["time"] = result["interval_start"]
		fields = octopus_record[0]["fields"]
		fields["consumption"] = result["consumption"]
		print(json.dumps(octopus_record, indent=2, sort_keys=False))

		influxclient.write_record(octopus_record)

	while o_data["next"]:
		print(o_data["next"])	
		o_data = octoclient.get_next(o_data["next"])
		for result in o_data["results"]:
#			p = Point(config.measurement_name).tag("interval_start",result["interval_start"]).tag("interval_end",result["interval_end"]).field("consumption",result["consumption"]).time(result["interval_start"])
#			influxclient.write_electricity_usage_point(p)
			print(result)
			tags = octopus_record[0]["tags"]
			tags["interval_start"] = result["interval_start"]
			tags["interval_end"] = result["interval_end"]
			octopus_record[0]["time"] = result["interval_start"]
			fields = octopus_record[0]["fields"]
			fields["consumption"] = result["consumption"]
			print(json.dumps(octopus_record, indent=2, sort_keys=False))
			
			influxclient.write_record(octopus_record)
	
	print("No more data")


#{
#	"count": 1,
#	"next": null,
#	"previous": null,
#	"results": [
#		{
#			"consumption": 0.474,
#			"interval_start": "2020-09-25T21:30:00+01:00",
#			"interval_last_record = end": "time9025T22:00:00+01:00"()
#		}

	#ts =	Get the last timestamp
	
	#last_read_time = datetime.fromtimestamp(ts)
	
##	for result in o_data["results"]:



	#	print(result["consumption"])
	#	print(result["interval_start"])
	#	print(result["interval_end"])

#		interval_start = datetime.fromisoformat(result["interval_start"])
#		data_read_time = interval_start.replace(tzinfo=timezone.utc).timestamp()
#		print(int(data_read_time))	# Time in seconds	
##		p = Point(config.measurement_name).tag("interval_start",result["interval_start"]).tag("interval_end",result["interval_end"]).field("consumption",result["consumption"]).time(result["interval_start"])
##		influxclient.write_electricity_usage_point(p)


#print(data_read_time)
#	data = response.json()
#	for result in data["results"]:
#		print(f'{result["consumption"]},{result["interval_start"]}')
#		print(f'{result["consumption"]},{result["interval_end"]}')


pull_latest_usage_data() 
			