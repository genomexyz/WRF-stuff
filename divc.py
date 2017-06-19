#!/usr/bin/python

from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt

def plotingtime(judul, plotvar):
	m = Basemap(resolution='l', projection='merc', \
	llcrnrlon=lon[0,0], llcrnrlat=lat[0,0], urcrnrlon=lon[0,-1], urcrnrlat=lat[-1,0])

	cs = m.pcolormesh(lon, lat, np.squeeze(plotvar), cmap='Set3', latlon=True)

	#draw map coastline, etc
	m.drawcoastlines(linewidth=0.75)
	m.drawcountries(linewidth=0.75)

	plt.title(judul)
	cbar = m.colorbar(cs, location='bottom', pad="10%") #add color bar
	plt.show()



#setting
findpres = 70000 #in Pa
dx = 10000.0
dy = 10000.0

#file
wrfoutfile = 'wrfout_d01_2017-06-01_00:00:00'


#######################
#read raw data session#
#######################

dsetwrf = Dataset(wrfoutfile, mode = 'r')

lat = dsetwrf.variables['XLAT'][0]
lon = dsetwrf.variables['XLONG'][0]

pres = dsetwrf.variables['P'][0]
presbase = dsetwrf.variables['PB'][0]
ucomp = dsetwrf.variables['U'][0]
vcomp = dsetwrf.variables['V'][0]


#####################
#calculating session#
#####################

print len(ucomp[0,0,:])
print len(vcomp[0,:,0])

div = np.zeros((len(vcomp), len(vcomp[0,:,0])-1, len(ucomp[0,0,:])-1))
print np.shape(div)
for i in xrange(len(vcomp[0,:,0])-1):
	for j in xrange(len(ucomp[0,0,:])-1):
		#print i,j
		#print ucomp[:,i,j], vcomp[:,i,j]
		#div[:,i,j] = 9
		div[:,i,j] = (ucomp[:,i,j+1] - ucomp[:,i,j]) / dx + (vcomp[:,i+1,j] - vcomp[:,i,j]) / dy

print div

#seek level with interpolation
realpres = pres + presbase

Y, X = np.shape(realpres[0])
paramfind = np.zeros((Y, X))
for i in xrange(Y):
	for j in xrange(X):
		#find 'in between' value of our findpres
		for k in xrange(len(realpres)):
			if (realpres[k,i,j] < findpres):
				banding = (div[k-1,i,j] - div[k,i,j]) / (realpres[k-1,i,j] - realpres[k,i,j])
				paramfind[i,j] = div[k,i,j] + (findpres - realpres[k,i,j]) * banding
				break

print paramfind

###############
#plotting time#
###############

plotingtime('divergence at 700 mb', paramfind)
