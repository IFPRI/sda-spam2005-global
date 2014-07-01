import pandas as pd
import urllib2 as ul2
import urllib as ul
import csv
import json

p = pd.read_csv('/media/data/Projects/spam2005-global/spam2005_a_sample.csv')
t = p.to_json(orient = 'records')
print t
tt = json.load(t)
print tt[0]
print values

data = ul.urlencode(tt[0])
data = ul.urlencode(values)
print data 
values = { 'iso3': 'sd', 'prod_level': 'sd', 'alloc_key': 'sd', 'cell5m': 0.0, 'rec_type': 's', 'unit': 'd',  'whea': 0,  'rice': 0,  'maiz': 0,  'barl': 0,  'pmil': 0,  'smil': 0,  'sorg': 0,  'ocer': 0,  'pota': 0,  'swpo': 0,  'yams': 0,  'cass': 0,  'orts': 0,  'bean': 0,  'chic': 0,  'cowp': 0,  'pige': 0,  'lent': 0,  'opul': 0,  'soyb': 0,  'grou': 0,  'cnut': 0,  'oilp': 0,  'sunf': 0,  'rape': 0,  'sesa': 0,  'ooil': 0,  'sugc': 0,  'sugb': 0,  'cott': 0,  'ofib': 0,  'acof': 0,  'rcof': 0,  'coco': 0,  'teas': 0,  'toba': 0,  'bana': 0,  'plnt': 0,  'trof': 0,  'temf': 0,  'vege': 0,  'rest': 0,  'whea_i': 0,  'rice_i': 0,  'maiz_i': 0,  'barl_i': 0,  'pmil_i': 0,  'smil_i': 0,  'sorg_i': 0,  'ocer_i': 0,  'pota_i': 0,  'swpo_i': 0,  'yams_i': 0,  'cass_i': 0,  'orts_i': 0,  'bean_i': 0,  'chic_i': 0,  'cowp_i': 0,  'pige_i': 0,  'lent_i': 0,  'opul_i': 0,  'soyb_i': 0,  'grou_i': 0,  'cnut_i': 0,  'oilp_i': 0,  'sunf_i': 0,  'rape_i': 0,  'sesa_i': 0,  'ooil_i': 0,  'sugc_i': 0,  'sugb_i': 0,  'cott_i': 0,  'ofib_i': 0,  'acof_i': 0,  'rcof_i': 0,  'coco_i': 0,  'teas_i': 0,  'toba_i': 0,  'bana_i': 0,  'plnt_i': 0,  'trof_i': 0,  'temf_i': 0,  'vege_i': 0,  'rest_i': 0,  'crea_date': '',  'year_data': '',  'source': '',  'scale_year': 0,  'name_cntr': '',  'name_adm1': '',  'whea_h': 0,  'whea_l': 0,  'whea_s': 0,  'rice_h': 0,  'rice_l': 0,  'rice_s': 0,  'maiz_h': 0,  'maiz_l': 0,  'maiz_s': 0,  'barl_h': 0,  'barl_l': 0,  'barl_s': 0,  'pmil_h': 0,  'pmil_l': 0,  'pmil_s': 0,  'smil_h': 0,  'smil_l': 0,  'smil_s': 0,  'sorg_h': 0,  'sorg_l': 0,  'sorg_s': 0,  'ocer_h': 0,  'ocer_l': 0,  'ocer_s': 0,  'pota_h': 0,  'pota_l': 0,  'pota_s': 0,  'swpo_h': 0,  'swpo_l': 0,  'swpo_s': 0,  'yams_h': 0,  'yams_l': 0,  'yams_s': 0,  'cass_h': 0,  'cass_l': 0,  'cass_s': 0,  'orts_h': 0,  'orts_l': 0,  'orts_s': 0,  'bean_h': 0,  'bean_l': 0,  'bean_s': 0,  'chic_h': 0,  'chic_l': 0,  'chic_s': 0,  'cowp_h': 0,  'cowp_l': 0,  'cowp_s': 0,  'pige_h': 0,  'pige_l': 0,  'pige_s': 0,  'lent_h': 0,  'lent_l': 0,  'lent_s': 0,  'opul_h': 0,  'opul_l': 0,  'opul_s': 0,  'soyb_h': 0,  'soyb_l': 0,  'soyb_s': 0,  'grou_h': 0,  'grou_l': 0,  'grou_s': 0,  'cnut_h': 0,  'cnut_l': 0,  'cnut_s': 0,  'oilp_h': 0,  'oilp_l': 0,  'oilp_s': 0,  'sunf_h': 0,  'sunf_l': 0,  'sunf_s': 0,  'rape_h': 0,  'rape_l': 0,  'rape_s': 0,  'sesa_h': 0,  'sesa_l': 0,  'sesa_s': 0,  'ooil_h': 0,  'ooil_l': 0,  'ooil_s': 0,  'sugc_h': 0,  'sugc_l': 0,  'sugc_s': 0,  'sugb_h': 0,  'sugb_l': 0,  'sugb_s': 0,  'cott_h': 0,  'cott_l': 0,  'cott_s': 0,  'ofib_h': 0,  'ofib_l': 0,  'ofib_s': 0,  'acof_h': 0,  'acof_l': 0,  'acof_s': 0,  'rcof_h': 0,  'rcof_l': 0,  'rcof_s': 0,  'coco_h': 0,  'coco_l': 0,  'coco_s': 0,  'teas_h': 0,  'teas_l': 0,  'teas_s': 0,  'toba_h': 0,  'toba_l': 0,  'toba_s': 0,  'bana_h': 0,  'bana_l': 0,  'bana_s': 0,  'plnt_h': 0,  'plnt_l': 0,  'plnt_s': 0,  'trof_h': 0,  'trof_l': 0,  'trof_s': 0,  'temf_h': 0,  'temf_l': 0,  'temf_s': 0,  'vege_h': 0,  'vege_l': 0,  'vege_s': 0,  'rest_h': 0,  'rest_l': 0,  'rest_s': 0,  'x': 0,  'y': 0,  'hc_seq5m': 0}
print type(values)
data = ul.urlencode(values)

# headers = { 'Content-Type' : 'application/json' }
url = 'http://127.0.0.1:8000/area/'
req = ul2.Request(url, data)
response = ul2.urlopen(req)
the_page = response.read();

