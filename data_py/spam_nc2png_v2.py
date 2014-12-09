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

logos = Image.open('/home/mcomanescu/logos/SPAM_logos_v4.png')
#logos = Image.open('/Users/maria/Projects/tests/results/SPAM_logos_v4.png')

outputFolder = '/home/tmp/png/'
#outputFolder = '/Users/maria/Downloads/'

baseShpLoc = '/home/mcomanescu/'
#baseShpLoc = '/Users/maria/Projects/tests/'

############ re-use spam2000 colors
cdict_harvested = {'red': ((0., 1, 1), (0.17, 0.91, 0.91), 
				 (0.34, 0.82, 0.82), (0.51, 0.729, 0.729),
                 (0.68, 0.631, 0.631), (0.75, 0.541, 0.541), (1, 0.451, 0.451)),
         'green':((0., 0.894, 0.894), (0.17, 0.769, 0.769), 
         	     (0.34, 0.624, 0.624), (0.51, 0.494, 0.494),
                 (0.68, 0.361, 0.361), (0.75, 0.251, 0.251), (1, 0.149, 0.149)),
         'blue': ((0., 0.631, 0.631), (0.17, 0.529, 0.529), 
         	     (0.34,  0.4, 0.4), (0.51, 0.286, 0.286),
                 (0.68, 0.184, 0.184), (0.75, 0.098, 0.098), (1, 0, 0))}
harvested_colormap = matplotlib.colors.LinearSegmentedColormap('harvested_colormap', cdict_harvested,256)

cdict_area = {'red': ((0., 0.922, 0.922), (0.17, 0.757, 0.757), 
				 (0.34, 0.616, 0.616), (0.51, 0.482, 0.482),
                 (0.68, 0.357, 0.357), (0.75, 0.255, 0.255), (1, 0.149, 0.149)),
         'green':((0., 1, 1), (0.17, 0.859, 0.859), 
         	     (0.34, 0.729, 0.729), (0.51, 0.612, 0.612),
                 (0.68, 0.49, 0.49), (0.75, 0.388, 0.388), (1, 0.29, 0.29)),
         'blue': ((0., 0.631, 0.631), (0.17, 0.592, 0.592), 
         	     (0.34,  0.451, 0.451), (0.51, 0.329, 0.329),
                 (0.68, 0.216, 0.216), (0.75, 0.118, 0.118), (1, 0, 0))}
area_colormap = matplotlib.colors.LinearSegmentedColormap('area_colormap', cdict_area,256)

cdict_yield = {'red': ((0., 1, 1), (0.14, 0.686, 0.686), 
				 (0.28, 0.353, 0.353), (0.42, 0.243, 0.243),
                 (0.56, 0.204, 0.204), (0.7, 0.122, 0.122), (0.84, 0.122, 0.122), (1, 0.047, 0.047)),
         'green':((0., 1, 1), (0.14, 0.961, 0.961), 
         	     (0.28, 0.902, 0.902), (0.42, 0.788, 0.788),
                 (0.56, 0.659, 0.659), (0.7, 0.494, 0.494), (0.84, 0.263, 0.263), (1, 0.063, 0.063)),
         'blue': ((0., 0.502, 0.502), (0.14, 0.325, 0.325), 
         	     (0.28,  0.133, 0.133), (0.42, 0.282, 0.282),
                 (0.56, 0.518, 0.518), (0.7, 0.639, 0.639), (0.84, 0.561, 0.561), (1, 0.471, 0.471))}
yield_colormap = matplotlib.colors.LinearSegmentedColormap('yield_colormap', cdict_yield,256)

cdict_prod = {'red': ((0., 0.808, 0.808), (0.14, 0.714, 0.714), 
				 (0.28, 0.592, 0.592), (0.42, 0.475, 0.475),
                 (0.56, 0.369, 0.369), (0.7, 0.275, 0.275), (0.84, 0.18, 0.18), (1, 0.082, 0.082)),
         'green':((0., 0.949, 0.949), (0.14, 0.839, 0.839), 
         	     (0.28, 0.741, 0.741), (0.42, 0.639, 0.639),
                 (0.56, 0.549, 0.549), (0.7, 0.471, 0.471), (0.84, 0.388, 0.388), (1, 0.259, 0.259)),
         'blue': ((0., 0.929, 0.929), (0.14, 0.82, 0.82), 
         	     (0.28,  0.718, 0.718), (0.42, 0.62, 0.62),
                 (0.56, 0.525, 0.525), (0.7, 0.447, 0.447), (0.84, 0.369, 0.369), (1, 0.29, 0.29))}
prod_colormap = matplotlib.colors.LinearSegmentedColormap('prod_colormap', cdict_prod,256)
###########

def read_data(variableFolder, crop):
	print crop
	filename = crop + '.tiff.nc'
	print variablePath + variableFolder + '/' + filename
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

def get_bins(d2, k):

	df = pd.DataFrame(d2)
	s = df.unstack()
	s_one = s[~np.isnan(s)]
	if len(s_one) == 0 : return []

	jc = br.Jenks_Caspall(s_one, k)

	for i in range(0,len(jc.bins)):
		if len(str(int(jc.bins[i]))) >= 3: 
			jc.bins[i] = np.round(jc.bins[i] / 100.0 ,0) * 100

	return jc.bins

def plot_map(res, bins, cmap, cropName, technologyName, variableName, unitLabel, parentFolder):
	
	figTitle = cropName + ' ' + technologyName + ' ' + variableName + ' (' + unitLabel + ')' 

	plt.close()
	plt.figtext(0.025,0.92, figTitle, clip_on = 'True', size = 'large', weight = 'semibold'); 
	plt.figtext(0.025,0.86, 'Spatially disaggregated production statistics of circa 2005 using the Spatial Production Allocation Model (SPAM).', clip_on = 'True', size = 'x-small', stretch = 'semi-condensed', weight = 'medium');
	plt.figtext(0.025,0.835,'Values are for 5 arc-minute grid cells.', clip_on = 'True', size = 'x-small', stretch = 'semi-condensed', weight = 'medium');

	plt.figtext(0.025,0.072, 'You, L., U. Wood-Sichra, S. Fritz, Z. Guo, L. See, and J. Koo. 2014', clip_on = 'True', size = 'xx-small', stretch = 'semi-condensed', weight = 'medium')
	plt.figtext(0.025,0.051, 'Spatial Production Allocation Model (SPAM) 2005 Beta Version.', clip_on = 'True', size = 'xx-small', stretch = 'semi-condensed', weight = 'medium')
	plt.figtext(0.025,0.030, '08.15.2014. Available from http://mapspam.info', clip_on = 'True', size = 'xx-small', stretch = 'semi-condensed', weight = 'medium');

	plt.figimage(logos, 4100, 200)

	map = Basemap(projection='merc',resolution='i', epsg=4326, lat_0 = 0, lon_0 = 20, llcrnrlon=-160, llcrnrlat=-70, urcrnrlon=200, urcrnrlat=90)
	map.drawlsmask(land_color='#fffff0', lakes = False, zorder = 1)
	shp_coast = map.readshapefile(baseShpLoc + 'ne_50m_coastline/ne_50m_coastline', 'scalerank', drawbounds=True, linewidth=0.1, color = '#828282', zorder = 7)
	shp_rivers = map.readshapefile(baseShpLoc + 'ne_110m_rivers_lake_centerlines/ne_110m_rivers_lake_centerlines', 'scalerank', drawbounds=True, color='#e8f8ff', linewidth=0.1, zorder = 5)
	shp_lakes = map.readshapefile(baseShpLoc + 'ne_110m_lakes/ne_110m_lakes', 'scalerank', drawbounds=True, linewidth=0.1, color='#e8f8ff', zorder=4)

	paths = []
	for line in shp_lakes[4]._paths:
		paths.append(matplotlib.path.Path(line.vertices, codes=line.codes))
	coll_lakes = matplotlib.collections.PathCollection(paths, linewidths=0, facecolors='#e8f8ff', zorder=3)

	cs = map.pcolormesh(res.lons, res.lats, res.d2, cmap=cmap, norm=BoundaryNorm(bins, 256, clip=True), zorder = 6)

	map.drawcountries(linewidth=0.1, color='#828282', zorder = 8)

	ax = plt.gca()
	ax.add_collection(coll_lakes)

	cbar = map.colorbar(cs,location='bottom', pad='3%')

	if (variableName == 'Production' or variableName == 'Yield'):
		labelSize = 8
	else :
		labelSize = 7
	labels = [item.get_text() for item in cbar.ax.get_xticklabels()]
	labels[0] = '1'; labels[labelSize - 1] = labels[labelSize - 1] + ' <'; labels[labelSize] = ''
	cbar.ax.set_xticklabels(labels)

	plt.tight_layout(h_pad=0.9, w_pad = 0.9)
	
	outputFile = 'spam2005v1r0_' + variableName.replace(' ', '-') + '_' + cropName + '_' + technologyName
	outputFile = outputFile.lower()
	plt.savefig(outputFolder + parentFolder + '/' + outputFile + '.png', format='png', dpi=1000)

'''
for crop in ('whea', 'rice', 'maiz', 'barl', 'pmil', 'smil', 'sorg', 'ocer', 'pota', 'swpo', 'yams', 'cass', 'orts', 'bean', 'chic', 'cowp', 'pige', 'lent', 'opul', 'soyb', 'grou', 'cnut', 'oilp', 'sunf', 'rape', 'sesa', 'ooil', 'sugc', 'sugb', 'cott', 'ofib', 'acof', 'rcof', 'coco', 'teas', 'toba', 'bana', 'plnt', 'trof', 'temf', 'vege', 'rest'):

	result = read_data('quickstart_harvested', crop)
	bins = get_bins(result.d2, 8)
	if (len(bins) != 0):
		cropName = cropList[cropList['varCode'] == crop].varName.values[0]
 		plot_map(result, bins, harvested_colormap, cropName, 'Total', 'Harvested Area', 'ha', 'quickstart_harvested')
 		
 		result_i = read_data('quickstart_harvested', crop + '_i')
 		plot_map(result_i, bins, harvested_colormap, cropName, 'Irrigated', 'Harvested Area', 'ha', 'quickstart_harvested')
 		
 		result_r = read_data('quickstart_harvested', crop + '_r')
 		plot_map(result_r, bins, harvested_colormap, cropName, 'Rainfed', 'Harvested Area', 'ha', 'quickstart_harvested')
'''
for crop in ('whea', 'rice', 'maiz', 'barl', 'pmil', 'smil', 'sorg', 'ocer', 'pota', 'swpo', 'yams', 'cass', 'orts', 'bean', 'chic', 'cowp', 'pige', 'lent', 'opul', 'soyb', 'grou', 'cnut', 'oilp', 'sunf', 'rape', 'sesa', 'ooil', 'sugc', 'sugb', 'cott', 'ofib', 'acof', 'rcof', 'coco', 'teas', 'toba', 'bana', 'plnt', 'trof', 'temf', 'vege', 'rest'):
	result = read_data('quickstart_area', crop)
	bins = get_bins(result.d2, 8)
	if (len(bins) != 0):
		cropName = cropList[cropList['varCode'] == crop].varName.values[0]
 		plot_map(result, bins, area_colormap, cropName, 'Total', 'Physical Area', 'ha', 'quickstart_area')
 		
 		result_i = read_data('quickstart_area', crop + '_i')
 		plot_map(result_i, bins, area_colormap, cropName, 'Irrigated', 'Physical Area', 'ha', 'quickstart_area')
 		
 		result_r = read_data('quickstart_area', crop + '_r')
 		plot_map(result_r, bins, area_colormap, cropName, 'Rainfed', 'Physical Area', 'ha', 'quickstart_area')

for crop in ('whea', 'rice', 'maiz', 'barl', 'pmil', 'smil', 'sorg', 'ocer', 'pota', 'swpo', 'yams', 'cass', 'orts', 'bean', 'chic', 'cowp', 'pige', 'lent', 'opul', 'soyb', 'grou', 'cnut', 'oilp', 'sunf', 'rape', 'sesa', 'ooil', 'sugc', 'sugb', 'cott', 'ofib', 'acof', 'rcof', 'coco', 'teas', 'toba', 'bana', 'plnt', 'trof', 'temf', 'vege', 'rest'):
	result = read_data('quickstart_yield', crop)
	bins = get_bins(result.d2, 9)
	if (len(bins) != 0):
		cropName = cropList[cropList['varCode'] == crop].varName.values[0]
 		plot_map(result, bins, yield_colormap, cropName, 'Total', 'Yield', 'kg/ha', 'quickstart_yield')
 		
 		result_i = read_data('quickstart_yield', crop + '_i')
 		plot_map(result_i, bins, yield_colormap, cropName, 'Irrigated', 'Yield', 'kg/ha', 'quickstart_yield')
 		
 		result_r = read_data('quickstart_yield', crop + '_r')
 		plot_map(result_r, bins, yield_colormap, cropName, 'Rainfed', 'Yield', 'kg/ha', 'quickstart_yield')

for crop in ('whea', 'rice', 'maiz', 'barl', 'pmil', 'smil', 'sorg', 'ocer', 'pota', 'swpo', 'yams', 'cass', 'orts', 'bean', 'chic', 'cowp', 'pige', 'lent', 'opul', 'soyb', 'grou', 'cnut', 'oilp', 'sunf', 'rape', 'sesa', 'ooil', 'sugc', 'sugb', 'cott', 'ofib', 'acof', 'rcof', 'coco', 'teas', 'toba', 'bana', 'plnt', 'trof', 'temf', 'vege', 'rest'):
	result = read_data('quickstart_prod', crop)
	bins = get_bins(result.d2, 9)
	if (len(bins) != 0):
		cropName = cropList[cropList['varCode'] == crop].varName.values[0]
 		plot_map(result, bins, prod_colormap, cropName, 'Total', 'Production', 'mt', 'quickstart_prod')
 		
 		result_i = read_data('quickstart_prod', crop + '_i')
 		plot_map(result_i, bins, prod_colormap, cropName, 'Irrigated', 'Production', 'mt', 'quickstart_prod')
 		
 		result_r = read_data('quickstart_prod', crop + '_r')
 		plot_map(result_r, bins, prod_colormap, cropName, 'Rainfed', 'Production', 'mt', 'quickstart_prod')
 		
######## to test single prints
'''
cropName = cropList[cropList['varCode'] == 'whea'].varName.values[0]

result = read_data('quickstart_harvested', 'whea')
bins = get_bins(result.d2, 8)
plot_map(result, bins, harvested_colormap, cropName, 'Total', 'Harvested Area', 'ha', 'quickstart_harvested')

result = read_data('quickstart_area', 'whea')
bins = get_bins(result.d2, 8)
plot_map(result, bins, area_colormap, cropName, 'Total', 'Physical Area', 'ha', 'quickstart_area')

result = read_data('quickstart_yield', 'whea')
bins = get_bins(result.d2, 9)
plot_map(result, bins, yield_colormap, cropName, 'Total', 'Yield', 'kg/ha', 'quickstart_yield')

result = read_data('quickstart_prod', 'whea')
bins = get_bins(result.d2, 9)
plot_map(result, bins, prod_colormap, cropName, 'Total', 'Production', 'mt', 'quickstart_prod')
'''

