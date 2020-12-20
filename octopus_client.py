#
# Script to pull data from Octopus Energy
#
# Derived from: https://gist.github.com/codeinthehole/5f274f46b5798f435e6984397f1abb64
# By David Winterbottom (codeinthehole)
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

# Requires:
# 	requests library (install with 'pip install requests')
#	
# Notes:
# - Results returned from queries contain:
#     count: The number of records included in this partial dataset
#     next: URL for the next partial dataset in the set
#     prev: URL for the previous partial dataset in the set
#     results: Array of data records returned
#
import requests


class OctopusAPIClient(object):
	BASE_URL = "https://api.octopus.energy/v1"

	class DataUnavailable(Exception):
		"""
		Catch-all exception indicating we can't get data back from the API
		"""

	def __init__(self, api_key):
		self.api_key = api_key
		self.session = requests.Session()

	def _get(self, path, params=None):
		"""
		Make a GET HTTP request
		"""
		if params is None:
			params = {}
		url = self.BASE_URL + path
		try:
			response = self.session.request(method="GET", url=url, auth=(self.api_key, ""), params=params)
		except requests.RequestException as e:
			raise self.DataUnavailable("Network exception") from e

		if response.status_code != 200:
			raise self.DataUnavailable("Unexpected response status (%s)" % response.status_code)

		return response.json()

	# Get the data for the next page if one exists
	def get_next(self, fullpath):
		params = {}
		try:
			response = self.session.request(method="GET", url=fullpath, auth=(self.api_key, ""), params=params)
		except requests.RequestException as e:
			raise self.DataUnavailable("Network exception") from e

		if response.status_code != 200:
			raise self.DataUnavailable("Unexpected response status (%s)" % response.status_code)

		return response.json()

	##################################################################
	# Get the list of product details, limited by the defined criteria
	#
	# https://developer.octopus.energy/docs/api/#energy-products
	#
	# Example data values:
	#	'code': 'AFFECT-FIX-12M-20-09-22', 
	#	'direction': 'IMPORT',
	#	'full_name': 'Affect 12M Fixed September 2020 v2',
	# 	'display_name': 'Affect 12M Fixed',
	# 	'description': "This tariff features 100% renewable electricity and fixes your unit rates and standing charge for 12 months. There are no exit fees, so if you change your mind, you're in control.",
	# 	'is_variable': False,
	# 	'is_green': False,
	# 	'is_tracker': False,
	# 	'is_prepay': False,
	# 	'is_business': False,
	# 	'is_restricted': False,
	# 	'term': 12,
	# 	'available_from': '2020-09-22T00:00:00+01:00',
	# 	'available_to': None,
	# 	'links': [
	# 		{	
	# 			'href': 'https://api.octopus.energy/v1/products/AFFECT-FIX-12M-20-09-22/',
	# 			'method': 'GET',
	# 			'rel': 'self'
	# 		}
	# 	],
	# 	'brand': 'AFFECT_ENERGY'
	#
	def products(self, is_variable=None, is_green=None, is_tracker=None, is_prepay=None, is_business=False, available_at=None):
		params = {}
		
		if is_variable:
			params['is_variable']=is_variable
			
		if is_green:
			params['is_green']=is_green
		
		if is_tracker:
			params['is_tracker']=is_tracker
		
		if is_prepay:
			params['is_prepay']=is_prepay
			
		if is_business:
			params['is_business']=is_business
	
		if available_at:
			params['available_at'] = available_at.isoformat()
			
		return self._get("/products/", params=params)
	
	##################################################################
	# Get a single products details
	#
	# Params:
	#		tariffs_active_at - The datetime for active tariffs. REST API defaults to now if not defined.
	# 
	# https://developer.octopus.energy/docs/api/#energy-products
	#
	def product(self, product_code, tariffs_active_at=None):
		params = {}
		
		if tariffs_active_at:
			params['tariffs_active_at'] = tariffs_active_at.isoformat()

		return self._get("/products/%s/" % product_code, params=params)

	##################################################################
	# Get a list of tariff charges
	#
	# https://developer.octopus.energy/docs/api/#list-tariff-charges
	#
	# TODO:
	#		period_from
	#		period_to
	#		page_size
	#			
	def elec_standing_charges(self, product_code, tariff_code, period_from=None, period_to=None, page_size=None):
		params = {}
		
		if period_from:
			params['period_from'] = period_from.isoformat()
			if period_to:
				params['period_to'] = period_to.isoformat()
				
		if page_size:
			params['page_size'] = page_size
			
		return self._get("/products/%s/electricity-tariffs/%s/standing-charges/" % (product_code, tariff_code), params)
	#############################
	def elec_standard_unit_rates(self, product_code, tariff_code, period_from=None, period_to=None, page_size=None):
		params = {}
		
		if period_from:
			params['period_from'] = period_from.isoformat()
			if period_to:
				params['period_to'] = period_to.isoformat()

		if page_size:
			params['page_size'] = page_size
					
		return self._get("/products/%s/electricity-tariffs/%s/standard-unit-rates/" % (product_code, tariff_code), params)
	#############################
	def elec_day_unit_rates(self, product_code, tariff_code):
		return self._get("/products/%s/electricity-tariffs/%s/day-unit-rates/" % (product_code, tariff_code))
	#############################
	def elec_night_unit_rates(self, product_code, tariff_code):
		return self._get("/products/%s/electricity-tariffs/%s/night-unit-rates/" % (product_code, tariff_code))
	#############################
	def gas_standing_charges(self, product_code, tariff_code):
		return self._get("/products/%s/gas-tariffs/%s/standing-charges/" % (product_code, tariff_code))
	#############################
	def gas_standard_unit_rates(self, product_code, tariff_code):
		return self._get("/products/%s/gas-tariffs/%s/standard-unit-rates/" % (product_code, tariff_code))

	##################################################################
	def electricity_meter_point(self, mpan):
		# See https://developer.octopus.energy/docs/api/#electricity-meter-points
		return self._get("/electricity-meter-points/%s/" % mpan)

	def electricity_tariff_unit_rates(self, product_code, tariff_code, period_from=None, period_to=None):
		# See https://developer.octopus.energy/docs/api/#list-tariff-charges
		params = {}
		if period_from:
			params['period_from'] = period_from.isoformat()
			if period_to:
				params['period_to'] = period_to.isoformat()
                
		return self._get("/products/%s/electricity-tariffs/%s/standard-unit-rates/" % (
			product_code, tariff_code), params=params)

	def electricity_tariff_standing_charges(self, product_code, tariff_code, period_from=None, period_to=None):
		# See https://developer.octopus.energy/docs/api/#list-tariff-charges
		params = {}
		if period_from:
			params['period_from'] = period_from.isoformat()
			if period_to:
				params['period_to'] = period_to.isoformat()
		return self._get("/products/%s/electricity-tariffs/%s/standing-charges/" % (
				product_code, tariff_code), params=params)

	def agile_tariff_unit_rates(self, gsp, period_from=None, period_to=None):
		"""
		Helper method to easily look-up the electricity unit rates for given GSP
		"""
		# Handle GSPs passed with leading underscore
		if len(gsp) == 2:
			gsp = gsp[1]
		assert gsp in ("A", "B", "C", "D", "E", "F", "G", "P", "N", "J", "H", "K", "L", "M")

		return self.electricity_tariff_unit_rates(
			product_code="AGILE-18-02-21",
			tariff_code="E-1R-AGILE-18-02-21-%s" % gsp,
			period_from=period_from,
			period_to=period_to)

	def electricity_meter_consumption(self, mpan, serial_number, **params):
		# See https://developer.octopus.energy/docs/api/#list-consumption-for-a-meter
		return self._get("/electricity-meter-points/%s/meters/%s/consumption/" % (
			mpan, serial_number), params=params)

	def gas_meter_consumption(self, mprn, serial_number, **params):
		# See https://developer.octopus.energy/docs/api/#list-consumption-for-a-meter
		return self._get("/gas-meter-points/%s/meters/%s/consumption/" % (
			mprn, serial_number), params=params)
     