#
# Script to test the tariff commands in the Agile API
#
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
 
import config
import json
from pprint import pprint
from dateutil import tz
from datetime import datetime
from datetime import timezone

from octopus_client import OctopusAPIClient

London_tz = tz.gettz("Europe/London")
octoclient = OctopusAPIClient(config.API_KEY)

product_code = 'AGILE-18-02-21'
tariff_code = 'E-1R-AGILE-18-02-21-A'

#product_code = 'VAR-17-01-11'
#tariff_code = 'E-1R-VAR-17-01-11-A'

#for result in data["results"]:
#	print("{} - {}".format(result["code"], result["display_name"]))

e_standing_charges = octoclient.elec_standing_charges(product_code, tariff_code)
print("\nElectricity - Standing Charges - {} - {}".format(product_code, tariff_code))
print("============================")
#pprint(e_standing_charges)	

period_from = datetime.fromisoformat("2020-10-01T00:00+00:00")
period_to = datetime.fromisoformat("2020-10-02T00:00+00:00")
e_standard_rates = octoclient.elec_standard_unit_rates(product_code, tariff_code, period_from=period_from, period_to=period_to, page_size=48)

#pprint(e_standard_rates)
for result in e_standard_rates["results"]:
	print("{} {} {}p {}p".format(result["valid_from"], result["valid_to"], result["value_exc_vat"], result["value_inc_vat"]))
#e_day_rates = octoclient.elec_day_unit_rates(product_code, tariff_code)

#e_night_rates = octoclient.elec_night_unit_rates(product_code, tariff_code)

gas_product_code = 'FGQ-0114-DD'
gas_tariff_code = 'FGQ-0114-DD-22'
#g_standing_charges = octoclient.gas_standing_charges(gas_product_code, gas_tariff_code)

#g_unit_rates = octoclient.gas_standard_unit_rates(gas_product_code, gas_tariff_code)
	
#pprint(product)