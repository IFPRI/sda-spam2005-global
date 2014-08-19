import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import BoundaryNorm, Normalize
import matplotlib.pyplot as plt
import numpy as np
import gc, brewer2mpl
from brewer2mpl import sequential
import pandas as pd
from PIL import Image
from netCDF4 import Dataset
import numpy.ma as ma
import pysal.esda.mapclassify as br

variablePath  = '/home/tmp/nc/'

#cropList = pd.read_csv('/Users/maria/Projects/spam2005-global/data_py/spam_crops.csv')
cropList = pd.read_csv('/home/django/spam2005-global/data_py/spam_crops.csv')

def plotCrop(variableFolder, crop):
	print crop
	filename = crop + '.tiff.nc'
	datafile = Dataset(variablePath + variableFolder + filename)

	data = datafile.variables['Band1'][:]
	lats = datafile.variables['lat'][:]
	lons = datafile.variables['lon'][:]

	d2 = ma.masked_where(data <= 1, data)
	df = pd.DataFrame(d2)

	s = pd.Series()
	for col in df.columns:
    	s = s.append(pd.Series(df[col]))

	s_one = s[~np.isnan(s)]
	
	jc = br.Jenks_Caspall(s_one, k = 8)

	bins = []
	for i in range(0,len(jc.bins)):
		if len(str(int(jc.bins[i]))) >= 3: 
			bins[i] = np.round(jc.bins[i] / 50.0 ,0) * 50

	if 'harvested' in variableFolder: 
		bmap = sequential.YlOrBr[bins]; unitLabel = 'ha';
		parentFolder = 'quickstart_harvested'; variableName = 'Harvested Area';
	if 'area' in variableFolder: 
		bmap = sequential.YlOrBr[bins]; unitLabel = 'ha';
		parentFolder = 'quickstart_area'; variableName = 'Physical Area';
	if 'yield' in variableFolder: 
		bmap = sequential.YlGnBu[bins]; unitLabel = 'kg/ha';
		parentFolder = 'quickstart_yield'; variableName = 'Yield';
	if 'prod' in variableFolder: 
		bmap = sequential.YlGn[bins]; unitLabel = 'mt';
		parentFolder = 'quickstart_prod'; variableName = 'Production';

	cropArr = crop.split('_');
	if len(cropArr) == 1:
		technologyName = 'Total'
	else:
		if cropArr[1] == 'r': technologyName = 'Rainfed'
		else: technologyName = 'Irrigated'

	cropName = cropList[cropList['varCode'] == cropArr[0]].varName.values[0]

	cmap = bmap.get_mpl_colormap(N=256)

	figTitle = cropName + ' ' + technologyName + ' ' + variableName + ' (' + unitLabel + ')' 

	plt.close()
	plt.figtext(0.035,0.92, str(figTitle), clip_on = 'True', size = 'large', weight = 'semibold'); 
	plt.figtext(0.035,0.87, 'Spatially disaggregated production statistics of circa 2005 using the Spatial Production Allocation Model (SPAM).', clip_on = 'True', size = 'x-small', stretch = 'semi-condensed', weight = 'medium');
	plt.figtext(0.035,0.845,'Values are for 5 arc-minute grid cells.', clip_on = 'True', size = 'x-small', stretch = 'semi-condensed', weight = 'medium');

	plt.figtext(0.035,0.072, 'You, L., U. Wood-Sichra, S. Fritz, Z. Guo, L. See, and J. Koo. 2014', clip_on = 'True', size = 'xx-small', stretch = 'semi-condensed', weight = 'medium')
	plt.figtext(0.035,0.051, 'Spatial Production Allocation Model (SPAM) 2005 Beta Version.', clip_on = 'True', size = 'xx-small', stretch = 'semi-condensed', weight = 'medium')
	plt.figtext(0.035,0.030, '08.18.2014. Available from http://mapspam.info', clip_on = 'True', size = 'xx-small', stretch = 'semi-condensed', weight = 'medium');

	logos = Image.open('/home/mcomanescu/logos/spam_logos2.png')
	plt.figimage(logos,1770, 100)

	map = Basemap(projection='merc',resolution='l', epsg=4326, lat_0 = 0, lon_0 = 20)
	#map = Basemap(projection='merc',resolution='i', epsg=4326, llcrnrlon=-130, llcrnrlat=-75, urcrnrlon=185, urcrnrlat=80)
	cs = map.pcolormesh(lons, lats, d2, cmap=cmap, norm=BoundaryNorm(bins, 256, clip=True))
	map.drawlsmask(land_color='#f4f4f4')
	# cs = map.pcolormesh(lons, lats, data, cmap=cmap, norm=Normalize(vmin=data.min(), vmax=data.max(), clip=True))

	map.drawcountries(linewidth=0.05)
	map.drawcoastlines(linewidth=0.05)

	cbar = map.colorbar(cs,location='bottom', pad='3%')


	cbar.ax.set_xlabel(unitLabel, fontsize = 'x-small');

	labels = [item.get_text() for item in cbar.ax.get_xticklabels()]
	labels[0] = '>0'; labels[bins] = '>' + labels[bins - 1]
	cbar.ax.set_xticklabels(labels)

	plt.tight_layout(h_pad=0.9, w_pad = 0.9)
	plt.savefig('/home/tmp/png/' + parentFolder + '/' + crop + '.png', format='png', dpi=400)

for variableFolder in ('quickstart_harvested/', 'quickstart_area/', 'quickstart_yield/', 'quickstart_prod/'):
	#for crop in ('whea', 'rice', 'maiz', 'barl', 'pmil', 'smil', 'sorg', 'ocer', 'pota', 'swpo', 'yams', 'cass', 'orts', 'bean', 'chic', 'cowp', 'pige', 'lent', 'opul', 'soyb', 'grou', 'cnut', 'oilp', 'sunf', 'rape', 'sesa', 'ooil', 'sugc', 'sugb', 'cott', 'ofib', 'acof', 'rcof', 'coco', 'teas', 'toba', 'bana', 'plnt', 'trof', 'temf', 'vege', 'rest', 'whea_i', 'rice_i', 'maiz_i', 'barl_i', 'pmil_i', 'smil_i', 'sorg_i', 'ocer_i', 'pota_i', 'swpo_i', 'yams_i', 'cass_i', 'orts_i', 'bean_i', 'chic_i', 'cowp_i', 'pige_i', 'lent_i', 'opul_i', 'soyb_i', 'grou_i', 'cnut_i', 'oilp_i', 'sunf_i', 'rape_i', 'sesa_i', 'ooil_i', 'sugc_i', 'sugb_i', 'cott_i', 'ofib_i', 'acof_i', 'rcof_i', 'coco_i', 'teas_i', 'toba_i', 'bana_i', 'plnt_i', 'trof_i', 'temf_i', 'vege_i', 'rest_i', 'whea_r', 'rice_r', 'maiz_r', 'barl_r', 'pmil_r', 'smil_r', 'sorg_r', 'ocer_r', 'pota_r', 'swpo_r', 'yams_r', 'cass_r', 'orts_r', 'bean_r', 'chic_r', 'cowp_r', 'pige_r', 'lent_r', 'opul_r', 'soyb_r', 'grou_r', 'cnut_r', 'oilp_r', 'sunf_r', 'rape_r', 'sesa_r', 'ooil_r', 'sugc_r', 'sugb_r', 'cott_r', 'ofib_r', 'acof_r', 'rcof_r', 'coco_r', 'teas_r', 'toba_r', 'bana_r', 'plnt_r', 'trof_r', 'temf_r', 'vege_r', 'rest_r'):
	for crop in ('whea', 'rice', 'maiz', 'whea_i', 'rice_i', 'maiz_i', 'whea_r', 'rice_r', 'maiz_r'):
		plotCrop(variableFolder, crop)
