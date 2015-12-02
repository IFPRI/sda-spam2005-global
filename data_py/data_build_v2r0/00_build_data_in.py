import pandas as pd
import os
os.chdir('/Users/maria/Projects/spam2005-global/data_build_v2r0/')


def read_region(region, technology) :
	path = 'data_raw/'+ region + '/spam2005V2r0_'+ str.upper(region) + '_' + technology + '/spam2005V2r0_' + str.upper(region) + '_'+ technology + '.csv'
	return pd.read_csv(path, low_memory=False)

# if __name__ == '__main__':

yield_data = pd.DataFrame()
for region in 'Asia', 'Canada', 'Europe', 'LAC', 'MEast', 'NAfrica', 'Oceania', 'Russia', 'SSA', 'USA' :
	yield_data = yield_data.append(read_region(region, 'Y'))
	print  region + ' ' + str(len(yield_data)) 
print len(yield_data) # 772367

harvested_data = pd.DataFrame()
for region in 'Asia', 'Canada', 'Europe', 'LAC', 'MEast', 'NAfrica', 'Oceania', 'Russia', 'SSA', 'USA'  :
	harvested_data = harvested_data.append(read_region(region, 'H'))
	print  region + ' ' + str(len(harvested_data)) #

production_data = pd.DataFrame()
for region in 'Asia', 'Canada', 'Europe', 'LAC', 'MEast', 'NAfrica', 'Oceania', 'Russia', 'SSA', 'USA' :
	production_data = production_data.append(read_region(region, 'P'))
	print  region + ' ' + str(len(production_data)) 
print len(production_data) # 772367

physical_data = pd.DataFrame()
for region in 'Asia', 'Canada', 'Europe', 'LAC', 'MEast', 'NAfrica', 'Oceania', 'Russia', 'SSA', 'USA'  :
	physical_data = physical_data.append(read_region(region, 'A'))
	print  region + ' ' + str(len(physical_data)) #

vop_data = pd.DataFrame()
for region in 'Asia', 'Canada', 'Europe', 'LAC', 'MEast', 'NAfrica', 'Oceania', 'Russia', 'SSA', 'USA'  :
	vop_data = vop_data.append(read_region(region, 'V'))
	print  region + ' ' + str(len(vop_data)) #
	
print vop_data.describe()
import numpy as np
print vop_data[str(vop_data.maiz_i) == str('')].head()
h = production_data.head(10)
h.to_csv('data_in/spam2005v2r0_harvested.csv', index = False);
print h
print h.dtypes
print vop_data.columns

for crop in 'whea','rice','maiz','barl','pmil','smil','sorg','ocer','pota','swpo','yams','cass','orts','bean','chic','cowp','pige','lent','opul','soyb','grou','cnut','oilp','sunf','rape','sesa','ooil','sugc','sugb','cott','ofib','acof','rcof','coco','teas','toba','bana','plnt','trof','temf','vege','rest':
	vop_data[crop + '_r'] = vop_data[crop + '_h'] + vop_data[crop + '_l'] + vop_data[crop + '_s']
	harvested_data[crop + '_r'] = harvested_data[crop + '_h'] + harvested_data[crop + '_l'] + harvested_data[crop + '_s']
	physical_data[crop + '_r'] = physical_data[crop + '_h'] + physical_data[crop + '_l'] + physical_data[crop + '_s']
	production_data[crop + '_r'] = production_data[crop + '_h'] + production_data[crop + '_l'] + production_data[crop + '_s']
	yield_data[crop + '_r'] = 0

yield_tmp = yield_data.merge(production_data, on='cell5m', suffixes=('', '_prod'))
yield_tmp = yield_tmp.merge(harvested_data, on='cell5m', suffixes=('', '_harvested'))

#print len(yield_tmp)
#yield_tmp.head(10).to_csv('data_in/spam2005v2r0_yield_2.csv', index=False)

for crop in 'whea','rice','maiz','barl','pmil','smil','sorg','ocer','pota','swpo','yams','cass','orts','bean','chic','cowp','pige','lent','opul','soyb','grou','cnut','oilp','sunf','rape','sesa','ooil','sugc','sugb','cott','ofib','acof','rcof','coco','teas','toba','bana','plnt','trof','temf','vege','rest':
	yield_tmp[crop + '_r'] = (yield_tmp[crop + '_r_prod'] / yield_tmp[crop + '_r_harvested'] * 1000).round(1)
	yield_tmp[crop + '_r'].fillna(0, inplace=True)

#print pd.DataFrame(yield_tmp, columns = ['whea', 'whea_i', 'whea_r', 'whea_h', 'whea_l', 'whea_s'])

yield_out = pd.DataFrame(yield_tmp, columns = ['iso3','prod_level','alloc_key','cell5m','rec_type','unit','whea','rice','maiz','barl','pmil','smil','sorg','ocer','pota','swpo','yams','cass','orts','bean','chic','cowp','pige','lent','opul','soyb','grou','cnut','oilp','sunf','rape','sesa','ooil','sugc','sugb','cott','ofib','acof','rcof','coco','teas','toba','bana','plnt','trof','temf','vege','rest','whea_i','rice_i','maiz_i','barl_i','pmil_i','smil_i','sorg_i','ocer_i','pota_i','swpo_i','yams_i','cass_i','orts_i','bean_i','chic_i','cowp_i','pige_i','lent_i','opul_i','soyb_i','grou_i','cnut_i','oilp_i','sunf_i','rape_i','sesa_i','ooil_i','sugc_i','sugb_i','cott_i','ofib_i','acof_i','rcof_i','coco_i','teas_i','toba_i','bana_i','plnt_i','trof_i','temf_i','vege_i','rest_i','whea_r','rice_r','maiz_r','barl_r','pmil_r','smil_r','sorg_r','ocer_r','pota_r','swpo_r','yams_r','cass_r','orts_r','bean_r','chic_r','cowp_r','pige_r','lent_r','opul_r','soyb_r','grou_r','cnut_r','oilp_r','sunf_r','rape_r','sesa_r','ooil_r','sugc_r','sugb_r','cott_r','ofib_r','acof_r','rcof_r','coco_r','teas_r','toba_r','bana_r','plnt_r','trof_r','temf_r','vege_r','rest_r','crea_date','year_data','source','scale_year','name_cntr','name_adm1','name_adm2'])
harvested_out = pd.DataFrame(harvested_data, columns = ['iso3','prod_level','alloc_key','cell5m','rec_type','unit','whea','rice','maiz','barl','pmil','smil','sorg','ocer','pota','swpo','yams','cass','orts','bean','chic','cowp','pige','lent','opul','soyb','grou','cnut','oilp','sunf','rape','sesa','ooil','sugc','sugb','cott','ofib','acof','rcof','coco','teas','toba','bana','plnt','trof','temf','vege','rest','whea_i','rice_i','maiz_i','barl_i','pmil_i','smil_i','sorg_i','ocer_i','pota_i','swpo_i','yams_i','cass_i','orts_i','bean_i','chic_i','cowp_i','pige_i','lent_i','opul_i','soyb_i','grou_i','cnut_i','oilp_i','sunf_i','rape_i','sesa_i','ooil_i','sugc_i','sugb_i','cott_i','ofib_i','acof_i','rcof_i','coco_i','teas_i','toba_i','bana_i','plnt_i','trof_i','temf_i','vege_i','rest_i','whea_r','rice_r','maiz_r','barl_r','pmil_r','smil_r','sorg_r','ocer_r','pota_r','swpo_r','yams_r','cass_r','orts_r','bean_r','chic_r','cowp_r','pige_r','lent_r','opul_r','soyb_r','grou_r','cnut_r','oilp_r','sunf_r','rape_r','sesa_r','ooil_r','sugc_r','sugb_r','cott_r','ofib_r','acof_r','rcof_r','coco_r','teas_r','toba_r','bana_r','plnt_r','trof_r','temf_r','vege_r','rest_r','crea_date','year_data','source','scale_year','name_cntr','name_adm1','name_adm2'])
physical_out = pd.DataFrame(physical_data, columns = ['iso3','prod_level','alloc_key','cell5m','rec_type','unit','whea','rice','maiz','barl','pmil','smil','sorg','ocer','pota','swpo','yams','cass','orts','bean','chic','cowp','pige','lent','opul','soyb','grou','cnut','oilp','sunf','rape','sesa','ooil','sugc','sugb','cott','ofib','acof','rcof','coco','teas','toba','bana','plnt','trof','temf','vege','rest','whea_i','rice_i','maiz_i','barl_i','pmil_i','smil_i','sorg_i','ocer_i','pota_i','swpo_i','yams_i','cass_i','orts_i','bean_i','chic_i','cowp_i','pige_i','lent_i','opul_i','soyb_i','grou_i','cnut_i','oilp_i','sunf_i','rape_i','sesa_i','ooil_i','sugc_i','sugb_i','cott_i','ofib_i','acof_i','rcof_i','coco_i','teas_i','toba_i','bana_i','plnt_i','trof_i','temf_i','vege_i','rest_i','whea_r','rice_r','maiz_r','barl_r','pmil_r','smil_r','sorg_r','ocer_r','pota_r','swpo_r','yams_r','cass_r','orts_r','bean_r','chic_r','cowp_r','pige_r','lent_r','opul_r','soyb_r','grou_r','cnut_r','oilp_r','sunf_r','rape_r','sesa_r','ooil_r','sugc_r','sugb_r','cott_r','ofib_r','acof_r','rcof_r','coco_r','teas_r','toba_r','bana_r','plnt_r','trof_r','temf_r','vege_r','rest_r','crea_date','year_data','source','scale_year','name_cntr','name_adm1','name_adm2'])
production_out = pd.DataFrame(production_data, columns = ['iso3','prod_level','alloc_key','cell5m','rec_type','unit','whea','rice','maiz','barl','pmil','smil','sorg','ocer','pota','swpo','yams','cass','orts','bean','chic','cowp','pige','lent','opul','soyb','grou','cnut','oilp','sunf','rape','sesa','ooil','sugc','sugb','cott','ofib','acof','rcof','coco','teas','toba','bana','plnt','trof','temf','vege','rest','whea_i','rice_i','maiz_i','barl_i','pmil_i','smil_i','sorg_i','ocer_i','pota_i','swpo_i','yams_i','cass_i','orts_i','bean_i','chic_i','cowp_i','pige_i','lent_i','opul_i','soyb_i','grou_i','cnut_i','oilp_i','sunf_i','rape_i','sesa_i','ooil_i','sugc_i','sugb_i','cott_i','ofib_i','acof_i','rcof_i','coco_i','teas_i','toba_i','bana_i','plnt_i','trof_i','temf_i','vege_i','rest_i','whea_r','rice_r','maiz_r','barl_r','pmil_r','smil_r','sorg_r','ocer_r','pota_r','swpo_r','yams_r','cass_r','orts_r','bean_r','chic_r','cowp_r','pige_r','lent_r','opul_r','soyb_r','grou_r','cnut_r','oilp_r','sunf_r','rape_r','sesa_r','ooil_r','sugc_r','sugb_r','cott_r','ofib_r','acof_r','rcof_r','coco_r','teas_r','toba_r','bana_r','plnt_r','trof_r','temf_r','vege_r','rest_r','crea_date','year_data','source','scale_year','name_cntr','name_adm1','name_adm2'])
vop_out = pd.DataFrame(vop_data, columns = ['iso3','prod_level','alloc_key','cell5m','rec_type','unit','whea','rice','maiz','barl','pmil','smil','sorg','ocer','pota','swpo','yams','cass','orts','bean','chic','cowp','pige','lent','opul','soyb','grou','cnut','oilp','sunf','rape','sesa','ooil','sugc','sugb','cott','ofib','acof','rcof','coco','teas','toba','bana','plnt','trof','temf','vege','rest','whea_i','rice_i','maiz_i','barl_i','pmil_i','smil_i','sorg_i','ocer_i','pota_i','swpo_i','yams_i','cass_i','orts_i','bean_i','chic_i','cowp_i','pige_i','lent_i','opul_i','soyb_i','grou_i','cnut_i','oilp_i','sunf_i','rape_i','sesa_i','ooil_i','sugc_i','sugb_i','cott_i','ofib_i','acof_i','rcof_i','coco_i','teas_i','toba_i','bana_i','plnt_i','trof_i','temf_i','vege_i','rest_i','whea_r','rice_r','maiz_r','barl_r','pmil_r','smil_r','sorg_r','ocer_r','pota_r','swpo_r','yams_r','cass_r','orts_r','bean_r','chic_r','cowp_r','pige_r','lent_r','opul_r','soyb_r','grou_r','cnut_r','oilp_r','sunf_r','rape_r','sesa_r','ooil_r','sugc_r','sugb_r','cott_r','ofib_r','acof_r','rcof_r','coco_r','teas_r','toba_r','bana_r','plnt_r','trof_r','temf_r','vege_r','rest_r','crea_date','year_data','source','scale_year','name_cntr','name_adm1','name_adm2'])

yield_out.to_csv('data_in/spam2005v2r0_yield.csv', index = False);
harvested_out.to_csv('data_in/spam2005v2r0_harvested-area.csv', index = False);
production_out.to_csv('data_in/spam2005v2r0_production.csv', index = False);
physical_out.to_csv('data_in/spam2005v2r0_physical-area.csv', index = False);
vop_out.to_csv('data_in/spam2005v2r0_value-production.csv', index = False);
