import pandas as pd
import urllib2 as ul2
import urllib as ul
import csv
import json

# p = pd.read_csv('/media/data/Projects/spam2005-global/spam2005_a_sample.csv')
# headers = { 'Content-Type' : 'application/json' }
# p = pd.read_csv('/media/data/Projects/Datasets/spam2005/spam2005_a.csv') # local
p = pd.read_csv('/home/djuser/spam2005_data/spam2005_a.csv') # server
p.columns = map(str.lower, p.columns)
print p['iso3'].unique()
url = 'http://127.0.0.1:8000/area/'
# ['CHN', 'AFG', 'IND', 'BTN', 'BGD', 'KHM', 'IDN', 'BRN', 'MNG', 'JPN', 'PRK', 'KOR'
# , 'PAK', 'NPL', 'MMR', 'VNM', 'LAO', 'PHL', 'THA', 'LKA', 'MYS', 'MDV', 'SGP', 'TLS'
# , 'CAN', 'NOR', 'FIN', 'SWE', 'GBR', 'EST', 'LVA', 'DNK', 'LTU', 'BLR', 'KAZ', 'IRL'
# , 'DEU', 'POL', 'NLD', 'UKR', 'BEL', 'FRA', 'CZE', 'LUX', 'SVK', 'AUT', 'HUN', 'MDA'
# , 'ROU', 'CHE', 'ITA', 'SVN', 'HRV', 'SRB', 'BIH', 'UZB', 'BGR', 'ESP', 'MNE', 'GEO'

# , 'KGZ', 'TKM', 'ALB', 'MKD', 'PRT', 'TUR', 'AZE', 'GRC', 'ARM', 'TJK', 'CYP', 'MEX'
# , 'CUB', 'HTI', 'DOM', 'JAM', 'PRI', 'BLZ', 'GLP', 'GTM', 'VIR', 'ATG', 'KNA', 'MSR'
# , 'HND', 'DMA', 'NIC', 'MTQ', 'SLV', 'LCA', 'VCT', 'BRB', 'COL', 'GRD', 'VEN', 'TTO'
# , 'CRI', 'PAN', 'GUY', 'SUR', 'GUF', 'BRA', 'ECU', 'PER', 'BOL', 'CHL', 'PRY', 'ARG'
# , 'URY', 'IRN', 'IRQ', 'SYR', 'MLT', 'LBN', 'JOR', 'ISR', 'SAU', 'KWT', 'OMN', 'BHR'
# , 'QAT', 'ARE', 'YEM', 'TUN', 'DZA', 'MAR', 'LBY', 'EGY', 'KIR', 'PNG', 'SLB', 'AUS'
# , 'VUT', 'FJI', 'NCL', 'NZL', 'RUS', 'MLI', 'NER', 'TCD', 'SDN', 'MRT', 'ERI', 'SEN'
# , 'BFA', 'ETH', 'GMB', 'NGA', 'CMR', 'DJI', 'GNB', 'GIN', 'BEN', 'SOM', 'GHA', 'TGO'
# , 'CAF', 'CIV', 'SLE', 'LBR', 'COD', 'KEN', 'GNQ', 'UGA', 'COG', 'GAB', 'STP', 'TZA'
# , 'RWA', 'BDI', 'SYC', 'AGO', 'ZMB', 'MWI', 'MUS', 'MOZ', 'MDG', 'ZWE', 'NAM', 'BWA'
# , 'ZAF', 'SWZ', 'LSO', 'USA']
# for cnt in p['iso3'].unique():
for cnt in ['BTN', 'BGD', 'KHM', 'IDN', 'BRN', 'MNG', 'JPN', 'PRK', 'KOR', 'PAK', 'NPL', 'MMR', 'VNM', 'LAO', 'PHL', 'THA', 'LKA', 'MYS', 'MDV', 'SGP', 'TLS', 'CAN', 'NOR', 'FIN', 'SWE', 'GBR', 'EST', 'LVA', 'DNK', 'LTU', 'BLR', 'KAZ', 'IRL', 'DEU', 'POL', 'NLD', 'UKR', 'BEL', 'FRA', 'CZE', 'LUX', 'SVK', 'AUT', 'HUN', 'MDA', 'ROU', 'CHE', 'ITA', 'SVN', 'HRV', 'SRB', 'BIH', 'UZB', 'BGR', 'ESP', 'MNE', 'GEO']:
	print cnt
	p_cnt = p[p['iso3'] == str(cnt)].to_json(orient = 'records')
	tt = json.loads(p_cnt)
	for t in tt: 
		data = ul.urlencode(t)
		req = ul2.Request(url, data)
		response = ul2.urlopen(req)
		the_page = response.read();


# single tests
# p_cnt = p[p['iso3'] == 'AFG'].to_json(orient = 'records')
# tt = json.loads(p_cnt)
# print tt[0]
# url = 'http://127.0.0.1:8000/area/'
# data = ul.urlencode(tt[0])
# req = ul2.Request(url, data)
# response = ul2.urlopen(req)
# the_page = response.read();
# print data