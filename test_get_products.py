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
#//#odify it under the terms of the GNU General Public License
# aprint(datas published by the Free Software Foundation; either version 2
#of the license, or (at your option) any later version.
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
from pprint import pprint
from datetime import datetime
from datetime import timezone


from octopus_client import OctopusAPIClient

octoclient = OctopusAPIClient(config.API_KEY)

#
## Example response data
#
#
# {
# 	'count': 100,
# 	'next': None,
# 	'previous': None, 
# 	'results': [
# 		{	'code': 'AFFECT-FIX-12M-20-09-22',
# 			'direction': 'IMPORT',
# 			'full_name': 'Affect 12M Fixed September 2020 v2',
# 			'display_name': 'Affect 12M Fixed',
# 			'description': "This tariff features 100% renewable electricity and fixes your unit rates and standing charge for 12 months. There are no exit fees, so if you change your mind, you're in control.",
# 			'is_variable': False,
# 			'is_green': False,
# 			'is_tracker': False,
# 			'is_prepay': False,
# 			'is_business': False,
# 			'is_restricted': False,
# 			'term': 12,
# 			'available_from': '2020-09-22T00:00:00+01:00',
# 			'available_to': None,
# 			'links': [
# 				{	
# 					'href': 'https://api.octopus.energy/v1/products/AFFECT-FIX-12M-20-09-22/',
# 					'method': 'GET',
# 					'rel': 'self'
# 				}
# 			],
# 			'brand': 'AFFECT_ENERGY'
# 		}
#
# ...
#
#		]
# }

# Get all of the data
data = octoclient.products()

print("\nAll Products")
print("=================")

for result in data["results"]:
	print("{} - {}".format(result["code"], result["display_name"]))

#
# Get a single product
#
product = octoclient.product("AGILE-18-02-21")

print("\nSingle Product")
print("=================")

pprint(product)