#ncols  4320
#nrows  2160
#xllcorner  -180
#yllcorner  -89.9999999999999
#cellsize 0.0833333333333333

import numpy as np
import pandas as pd
import os
import gc
import urllib
import rpy2.robjects as robjects
import gdal

os.chdir('/Users/maria/Projects/hc-cell5m/py/data_update_042015/data_in')
vi = pd.read_csv('vi.csv')
cell5m = pd.read_csv('cell5m.csv')

cols = 50539
rows = 10000
offset = 1000

ncols = 4320
nrows = 2160
cellsize  = 0.0833333333333333


# http://gis.stackexchange.com/questions/58517/python-gdal-save-array-as-raster-with-projection-from-other-file
# http://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html

dst_filename = 'test.tif'
format = 'GTiff'
driver = gdal.GetDriverByName(format)

dst_ds = driver.Create(dst_filename, ncols, nrows, 1, gdal.GDT_Byte)

for i in range(10):
    # generate random integers from 1 to 10
    a = np.random.random_integers(0, i, size=(offset, cols))
    # write data to band 1
    dst_ds.GetRasterBand(1).WriteArray(a, 0, offset * i)

dst_ds = None

a = np.random.random_integers(1, 10, size=(offset, cols))
print len(a[0])



