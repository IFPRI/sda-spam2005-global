
from mpl_toolkits.basemap import Basemap
from netCDF4 import *
from matplotlib.colors import BoundaryNorm, Normalize
import matplotlib.pyplot as plt
import numpy as np
import gc, brewer2mpl
from brewer2mpl import sequential
import pandas as pd
from PIL import Image
from netCDF4 import Dataset
import numpy.ma as ma

matplotlib.use('Agg')

variableFolder = '/home/tmp/nc/quickstart_harvested/'
#variableFolder = '/home/tmp/nc/quickstart_area/'
#variableFolder = '/home/tmp/nc/quickstart_yield/'
#variableFolder = '/home/tmp/nc/quickstart_prod/'

#cropList = pd.read_csv('/Users/maria/Projects/spam2005-global/data_py/spam_crops.csv')
cropList = pd.read_csv('/home/django/spam2005-global/data_py/spam_crops.csv')

def plotCrop(variableFolder, crop, cropList):
	filename = crop + '.tiff.nc'
	datafile = Dataset(variableFolder + filename)

	data = datafile.variables['Band1'][:]
	lats = datafile.variables['lat'][:]
	lons = datafile.variables['lon'][:]

	d2 = ma.masked_where(data <= 0, data)
	df = pd.DataFrame(d2)
	df = np.round(df,0)
	
	bins = 7
	success = False

	while not success:
	    try:
	        cat = pd.qcut(df, bins, retbins=True, precision = 1)
	        success = True
	    except ValueError:
	    	bins = bins - 1
	    	pass

	for i in range(0,len(cat[1])):
		if len(str(int(cat[1][i]))) >= 3: 
			cat[1][i] = np.round(cat[1][i] * 0.01,0) / 0.01

	if 'harvested' in variableFolder: 
		bmap = sequential.YlGnBu[7]; unitLabel = 'ha';
		parentFolder = 'quickstart_harvested'; variableName = 'Harvested Area';
	if 'area' in variableFolder: 
		bmap = sequential.YlGnBu[7]; unitLabel = 'ha';
		parentFolder = 'quickstart_area'; variableName = 'Physical Area';
	if 'yield' in variableFolder: 
		bmap = sequential.YlGnBu[7]; unitLabel = 'kg/ha';
		parentFolder = 'quickstart_yield'; variableName = 'Yield';
	if 'prod' in variableFolder: 
		bmap = sequential.YlGnBu[7]; unitLabel = 'mt';
		parentFolder = 'quickstart_prod'; variableName = 'Production';

	cropArr = crop.split('_');
	if len(cropArr) == 1:
		technologyName = 'Total'
	else:
		if cropArr[1] == 'r': technologyName = 'Rainfed'
		else: technologyName = 'Irrigated'

	cropName = cropList[cropList['varCode'] == cropArr[0]].varName[1]

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
	cs = map.pcolormesh(lons, lats, d2, cmap=cmap, norm=BoundaryNorm(cat[1], 256, clip=True))
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

for crop in ('bana', 'barl'):
	plotCrop(variableFolder, crop, cropList)
