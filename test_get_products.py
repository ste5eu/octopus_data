#
# Script to manage the extraction of data from Octopus Energy and handling the data returned
#
# TODO:
# - Allow and manage command line parameters
# - Pull data for Agile rate from Octopus and send to Influxdb
#
# Copyright 2020 Steve Upton
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to 
# deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
# IN THE SOFTWARE.
 
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