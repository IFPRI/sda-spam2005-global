import pandas as pd
import urllib2 as ul2
import urllib as ul
import csv
import json

# p = pd.read_csv('/media/data/Projects/spam2005-global/spam2005_a_sample.csv')
# headers = { 'Content-Type' : 'application/json' }
p = pd.read_csv('/media/data/Projects/Datasets/spam2005/spam2005_a.csv')
p.columns = map(str.lower, p.columns)
print p['iso3'].unique()
url = 'http://127.0.0.1:8000/area/'

# for cnt in p['iso3'].unique():
for cnt in ['BEN', 'ROU']:
	p_cnt = p[p['iso3'] == str(cnt)].to_json(orient = 'records')
	tt = json.loads(p_cnt)
	for t in tt: 
		data = ul.urlencode(t)
		req = ul2.Request(url, data)
		response = ul2.urlopen(req)
		the_page = response.read();

