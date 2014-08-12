
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
from matplotlib.colors import BoundaryNorm, Normalize
import matplotlib.pyplot as plt
import numpy as np
import gc, brewer2mpl
from brewer2mpl import sequential
import pandas as pd
import Image

datafile = Dataset('/Users/maria/Projects/tests/maiz8.nc')
data = datafile.variables['Band1'][:]
lats = datafile.variables['lat'][:]
lons = datafile.variables['lon'][:]

df = pd.DataFrame(data[data>0])
cat = pd.qcut(df, 10, retbins=True, precision = 1)
for i in range(0,11):
	cat[1][i] = np.round(cat[1][i] * 0.01,0) / 0.01

bmap = sequential.YlGnBu[7]
cmap = bmap.get_mpl_colormap(N=256)

plt.close()
map = Basemap(projection='merc',lat_0=0,lon_0=0,resolution='l', epsg=4326)

# cs = map.pcolormesh(lons, lats, data, cmap=cmap, norm=Normalize(vmin=data.min(), vmax=data.max(), clip=True))
cs = map.pcolormesh(lons, lats, data, cmap=cmap, norm=BoundaryNorm(cat[1], 256, clip=True))

map.drawcoastlines(linewidth=0.05)
map.drawcountries(linewidth=0.05)

cbar = map.colorbar(cs,location='bottom', pad='5%')
cbar.ax.set_xlabel('kg/ha');

plt.title('Maize Yield [kg/ha]', loc = 'left'); 
plt.figtext(12,12,'Source: You, Wood-Sichra, and Wood. 2014. SPAM 2014');
img = Image.open('/Users/maria/Projects/tests/hc_white_small2.png')
plt.figimage(img,1200,12)
plt.savefig('/Users/maria/Projects/tests/maiz_y.png', format='png', dpi=200)
