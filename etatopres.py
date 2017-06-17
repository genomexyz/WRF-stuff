#!/usr/bin/python

from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt

#setting
findpres = 85000

#file
wrfoutfile = 'wrfout_d01_2017-06-01_00:00:00'


#######################
#read raw data session#
#######################

dsetwrf = Dataset(wrfoutfile, mode = 'r')

lat = dsetwrf.variables['XLAT'][0]
lon = dsetwrf.variables['XLONG'][0]
stagz = dsetwrf.variables['ZNU'][0]

pres = dsetwrf.variables['P'][0]
presbase = dsetwrf.variables['PB'][0]
ptop = dsetwrf.variables['P_TOP'][0]

mixrat = dsetwrf.variables['QVAPOR'][0]

print np.shape(presbase)
print np.shape(pres)

realpres = pres + presbase

print realpres
print mixrat

Y, X = np.shape(realpres[0])
paramfind = np.zeros((Y, X))
for i in xrange(Y):
	for j in xrange(X):
		#find 'in between' value of our findpres
		for k in xrange(len(stagz)):
			if (realpres[k,i,j] < findpres):
				banding = (mixrat[k-1,i,j] - mixrat[k,i,j]) / (realpres[k-1,i,j] - realpres[k,i,j])
				paramfind[i,j] = mixrat[k,i,j] + (findpres - realpres[k,i,j]) * banding
				print k, k-1
				break

print paramfind

###############
#plotting time#
###############

m = Basemap(resolution='l', projection='merc', \
llcrnrlon=lon[0,0], llcrnrlat=lat[0,0], urcrnrlon=lon[0,-1], urcrnrlat=lat[-1,0])

cs = m.pcolormesh(lon, lat, np.squeeze(paramfind), cmap='Set3', latlon=True)

#draw map coastline, etc
m.drawcoastlines(linewidth=0.75)
m.drawcountries(linewidth=0.75)

plt.title('mixing ratio at 850 mb')
cbar = m.colorbar(cs, location='bottom', pad="10%") #add color bar
plt.show()
