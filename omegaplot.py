#!/usr/bin/python

import numpy as np
import pandas as pd
from netCDF4 import Dataset
from datetime import datetime
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
import wrf
from wrf import getvar, interplevel
import Image
import matplotlib.patches as mpatches

#setting
wrfoutname = '/home/genomexyz/banding/wrfout_d03_2016-06-17_12_00_00'
lattarget = -7.53
lontarget = 109.4


dsetwrf = Dataset(wrfoutname, mode = 'r')

#horizontal grid
latawal = dsetwrf.variables['XLAT'][0]
lonawal = dsetwrf.variables['XLONG'][0]
height = dsetwrf.variables['ZNU'][0]
waktu = np.asarray(range(12,31))

for i in xrange(len(latawal[:,0])):
	if lattarget > latawal[i,0]:
		y2 = latawal[i,0]
		y1 = latawal[i-1,0]
		titiky2 = i
		titiky1 = i-1

if abs(y2-lattarget) < abs(lattarget-y1):
	titiky = titiky2
else:
	titiky = titiky1

for i in xrange(len(lonawal[0,:])):
	if lontarget > lonawal[0,i]:
		x2 = lonawal[0,i]
		x1 = lonawal[0,i-1]
		titikx2 = i
		titikx1 = i-1

if abs(x2-lontarget) < abs(lontarget-x1):
	titikx = titikx2
else:
	titikx = titikx1

omegacnt = []
for i in xrange(12,31):
	omegavar = getvar(dsetwrf, "omg", timeidx = i)
	omegacnt.append(omegavar[:,titiky,titikx])
	#omegacnt = np.append(omegacnt, 
omegacnt = np.asarray(omegacnt)
omegacnt = np.transpose(omegacnt)

#
omegacnt = np.flipud(omegacnt)
height = np.flip(height, 0)

print omegacnt
print np.shape(omegacnt)
plt.contourf(waktu, height, omegacnt, 100)
plt.colorbar()
plt.show()
