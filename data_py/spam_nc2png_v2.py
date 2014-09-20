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
import sys 

variablePath  = '/home/tmp/nc/'
#variablePath = '/Users/maria/Downloads/'

cropList = pd.read_csv('/home/django/spam2005-global/data_py/spam_crops.csv')
#cropList = pd.read_csv('/Users/maria/Projects/spam2005-global/data_py/spam_crops.csv')

logos = Image.open('/home/mcomanescu/logos/spam_logos2.png')
#logos = Image.open('/Users/maria/Projects/tests/results/spam_logos2.png')

outputFolder = '/home/tmp/png/'
#outputFolder = '/Users/maria/Downloads/'

def read_data(variableFolder, crop):
	print crop
	filename = crop + '.tiff.nc'
	print variablePath + filename
	datafile = Dataset(variablePath + variableFolder + '/' + filename)
	#datafile = Dataset(variablePath + filename)

	data = datafile.variables['Band1'][:]
	lats = datafile.variables['lat'][:]
	lons = datafile.variables['lon'][:]

	d2 = ma.masked_where(data <= 1, data)
	df = pd.DataFrame(d2)

	res = pd.DataFrame()
	res.lats = lats
	res.lons = lons
	res.d2 = d2
	return res

def get_bins(d2):

	df = pd.DataFrame(d2)
	s = df.unstack()
	s_one = s[~np.isnan(s)]
	if len(s_one) == 0 : return []

	jc = br.Jenks_Caspall(s_one, k = 8)

	for i in range(0,len(jc.bins)):
		if len(str(int(jc.bins[i]))) >= 3: 
			jc.bins[i] = np.round(jc.bins[i] / 100.0 ,0) * 100

	return jc.bins

def plot_map(res, bins, bmap, cropName, technologyName, variableName, unitLabel, parentFolder, outputFile):
	
	cmap = bmap.get_mpl_colormap(N=256)

	figTitle = cropName + ' ' + technologyName + ' ' + variableName + ' (' + unitLabel + ')' 

	plt.close()
	plt.figtext(0.025,0.92, figTitle, clip_on = 'True', size = 'large', weight = 'semibold'); 
	plt.figtext(0.025,0.86, 'Spatially disaggregated production statistics of circa 2005 using the Spatial Production Allocation Model (SPAM).', clip_on = 'True', size = 'x-small', stretch = 'semi-condensed', weight = 'medium');
	plt.figtext(0.025,0.835,'Values are for 5 arc-minute grid cells.', clip_on = 'True', size = 'x-small', stretch = 'semi-condensed', weight = 'medium');

	plt.figtext(0.025,0.072, 'You, L., U. Wood-Sichra, S. Fritz, Z. Guo, L. See, and J. Koo. 2014', clip_on = 'True', size = 'xx-small', stretch = 'semi-condensed', weight = 'medium')
	plt.figtext(0.025,0.051, 'Spatial Production Allocation Model (SPAM) 2005 Beta Version.', clip_on = 'True', size = 'xx-small', stretch = 'semi-condensed', weight = 'medium')
	plt.figtext(0.025,0.030, '08.15.2014. Available from http://mapspam.info', clip_on = 'True', size = 'xx-small', stretch = 'semi-condensed', weight = 'medium');

	plt.figimage(logos,1830, 100)

	map = Basemap(projection='merc',resolution='i', epsg=4326, lat_0 = 0, lon_0 = 20, llcrnrlon=-160, llcrnrlat=-70, urcrnrlon=200, urcrnrlat=90)
	map.drawlsmask(land_color='#fafafa', lakes = False, zorder = 1)
	shp_coast = map.readshapefile('/home/mcomanescu/ne_50m_coastline/ne_50m_coastline', 'scalerank', drawbounds=True, linewidth=0.1, color = '#e0e0e0')
	shp_rivers = map.readshapefile('/home/mcomanescu/ne_110m_rivers_lake_centerlines/ne_110m_rivers_lake_centerlines', 'scalerank', drawbounds=True, color='#c6dbef', linewidth=0.1, zorder = 5)
	shp_lakes = map.readshapefile('/home/mcomanescu/ne_110m_lakes/ne_110m_lakes', 'scalerank', drawbounds=True, linewidth=0.1, color='#c6dbef', zorder=4)

	paths = []
	for line in shp_lakes[4]._paths:
		paths.append(matplotlib.path.Path(line.vertices, codes=line.codes))
	coll_lakes = matplotlib.collections.PathCollection(paths, linewidths=0, facecolors='#c6dbef', zorder=3)

	cs = map.pcolormesh(res.lons, res.lats, res.d2, cmap=cmap, norm=BoundaryNorm(bins, 256, clip=True), zorder = 6)

	map.drawcountries(linewidth=0.05, color='#e0e0e0', zorder = 7)

	ax = plt.gca()
	ax.add_collection(coll_lakes)

	cbar = map.colorbar(cs,location='bottom', pad='3%')

	labels = [item.get_text() for item in cbar.ax.get_xticklabels()]
	labels[0] = '1'; labels[6] = labels[6] + ' <'; labels[7] = ''
	cbar.ax.set_xticklabels(labels)

	plt.tight_layout(h_pad=0.9, w_pad = 0.9)
	plt.savefig(outputFolder + parentFolder + '/' + outputFile + '.png', format='png', dpi=400)

for crop in ('whea', 'rice', 'maiz', 'barl', 'pmil', 'smil', 'sorg', 'ocer', 'pota', 'swpo', 'yams', 'cass', 'orts', 'bean', 'chic', 'cowp', 'pige', 'lent', 'opul', 'soyb', 'grou', 'cnut', 'oilp', 'sunf', 'rape', 'sesa', 'ooil', 'sugc', 'sugb', 'cott', 'ofib', 'acof', 'rcof', 'coco', 'teas', 'toba', 'bana', 'plnt', 'trof', 'temf', 'vege', 'rest'):
#for crop in ('whea', 'smil'):
	result = read_data('quickstart_harvested', crop)
	bins = get_bins(result.d2)
	if (len(bins) != 0):
		cropName = cropList[cropList['varCode'] == crop].varName.values[0]
 		plot_map(result, bins, sequential.Oranges[7], cropName, 'Total', 'Harvested Area', 'ha', 'quickstart_harvested', crop)
 		
 		result_i = read_data('quickstart_harvested', crop + '_i')
 		plot_map(result_i, bins, sequential.Oranges[7], cropName, 'Irrigated', 'Harvested Area', 'ha', 'quickstart_harvested', crop + '_i')
 		
 		result_r = read_data('quickstart_harvested', crop + '_r')
 		plot_map(result_r, bins, sequential.Oranges[7], cropName, 'Rainfed', 'Harvested Area', 'ha', 'quickstart_harvested', crop + '_r')

for crop in ('whea', 'rice', 'maiz', 'barl', 'pmil', 'smil', 'sorg', 'ocer', 'pota', 'swpo', 'yams', 'cass', 'orts', 'bean', 'chic', 'cowp', 'pige', 'lent', 'opul', 'soyb', 'grou', 'cnut', 'oilp', 'sunf', 'rape', 'sesa', 'ooil', 'sugc', 'sugb', 'cott', 'ofib', 'acof', 'rcof', 'coco', 'teas', 'toba', 'bana', 'plnt', 'trof', 'temf', 'vege', 'rest'):
	result = read_data('quickstart_area', crop)
	bins = get_bins(result.d2)
	if (len(bins) != 0):
		cropName = cropList[cropList['varCode'] == crop].varName.values[0]
 		plot_map(result, bins, sequential.Oranges[7], cropName, 'Total', 'Physical Area', 'ha', 'quickstart_area', crop)
 		
 		result_i = read_data('quickstart_area', crop + '_i')
 		plot_map(result_i, bins, sequential.Oranges[7], cropName, 'Irrigated', 'Physical Area', 'ha', 'quickstart_area', crop + '_i')
 		
 		result_r = read_data('quickstart_area', crop + '_r')
 		plot_map(result_r, bins, sequential.Oranges[7], cropName, 'Rainfed', 'Physical Area', 'ha', 'quickstart_area', crop + '_r')

for crop in ('whea', 'rice', 'maiz', 'barl', 'pmil', 'smil', 'sorg', 'ocer', 'pota', 'swpo', 'yams', 'cass', 'orts', 'bean', 'chic', 'cowp', 'pige', 'lent', 'opul', 'soyb', 'grou', 'cnut', 'oilp', 'sunf', 'rape', 'sesa', 'ooil', 'sugc', 'sugb', 'cott', 'ofib', 'acof', 'rcof', 'coco', 'teas', 'toba', 'bana', 'plnt', 'trof', 'temf', 'vege', 'rest'):
	result = read_data('quickstart_yield', crop)
	bins = get_bins(result.d2)
	if (len(bins) != 0):
		cropName = cropList[cropList['varCode'] == crop].varName.values[0]
 		plot_map(result, bins, sequential.YlGnBu[7], cropName, 'Total', 'Yield', 'kg/ha', 'quickstart_yield', crop)
 		
 		result_i = read_data('quickstart_yield', crop + '_i')
 		plot_map(result_i, bins, sequential.YlGnBu[7], cropName, 'Irrigated', 'Yield', 'kg/ha', 'quickstart_yield', crop + '_i')
 		
 		result_r = read_data('quickstart_yield', crop + '_r')
 		plot_map(result_r, bins, sequential.YlGnBu[7], cropName, 'Rainfed', 'Yield', 'kg/ha', 'quickstart_yield', crop + '_r')

for crop in ('whea', 'rice', 'maiz', 'barl', 'pmil', 'smil', 'sorg', 'ocer', 'pota', 'swpo', 'yams', 'cass', 'orts', 'bean', 'chic', 'cowp', 'pige', 'lent', 'opul', 'soyb', 'grou', 'cnut', 'oilp', 'sunf', 'rape', 'sesa', 'ooil', 'sugc', 'sugb', 'cott', 'ofib', 'acof', 'rcof', 'coco', 'teas', 'toba', 'bana', 'plnt', 'trof', 'temf', 'vege', 'rest'):
	result = read_data('quickstart_prod', crop)
	bins = get_bins(result.d2)
	if (len(bins) != 0):
		cropName = cropList[cropList['varCode'] == crop].varName.values[0]
 		plot_map(result, bins, sequential.Greens[7], cropName, 'Total', 'Production', 'mt', 'quickstart_prod', crop)
 		
 		result_i = read_data('quickstart_prod', crop + '_i')
 		plot_map(result_i, bins, sequential.Greens[7], cropName, 'Irrigated', 'Production', 'mt', 'quickstart_prod', crop + '_i')
 		
 		result_r = read_data('quickstart_prod', crop + '_r')
 		plot_map(result_r, bins, sequential.Greens[7], cropName, 'Rainfed', 'Production', 'mt', 'quickstart_prod', crop + '_r')
 		
