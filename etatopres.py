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
stagz = dsetwrf.variables['ZNW'][0]


ptop = dsetwrf.variables['P_TOP'][0]
psfc = dsetwrf.variables['PSFC'][0]
wcomp = dsetwrf.variables['W'][0]
#potentemp = dsetwrf.variables['T'][0]
#basetemp = dsetwrf.variables['T00'][0]

#print psfc
#print
print stagz
print

#####################
#calculating session#
#####################

#
#poten temp = perturb poten temp + base state temp
#

Y, X = np.shape(psfc)

etatoprs = np.zeros((len(stagz), Y, X))


#convert eta to pressure
for i in xrange(Y):
	for j in xrange(X):
		etatoprs[:,i,j] = stagz * (psfc[i,j] - ptop) + ptop

#print etatoprs


paramfind = np.zeros((Y, X))
for i in xrange(Y):
	for j in xrange(X):
		#find 'in between' value of our findpres
		for k in xrange(len(stagz)):
			if (etatoprs[k,i,j] < findpres):
				paramfind[i,j] = wcomp[k-1,i,j] - (etatoprs[k-1,i,j] - findpres) \
				* ((wcomp[k-1,i,j] - wcomp[k,i,j]) / (etatoprs[k-1,i,j] - etatoprs[k,i,j]))
				print wcomp[k,i,j], wcomp[k-1,i,j]
				break


###############
#plotting time#
###############

m = Basemap(resolution='l', projection='merc', \
llcrnrlon=lon[0,0], llcrnrlat=lat[0,0], urcrnrlon=lon[0,-1], urcrnrlat=lat[-1,0])

cs = m.pcolormesh(lon, lat, np.squeeze(paramfind), cmap='Set3', latlon=True)

#draw map coastline, etc
m.drawcoastlines(linewidth=0.75)
m.drawcountries(linewidth=0.75)

plt.title('vertical velocity at 850 mb')
cbar = m.colorbar(cs, location='bottom', pad="10%") #add color bar
plt.show()
