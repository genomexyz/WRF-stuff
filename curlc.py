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
findpres = 85000 #in Pa
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


#unstag all staggering grid
X = len(ucomp[0,0,:]) - 1
Y = len(vcomp[0,:,0]) - 1

#unstag ucomp
unstagu = np.zeros((len(ucomp), Y, X))
for i in xrange(X):
	unstagu[:,:,i] = (ucomp[:,:,i] + ucomp[:,:,i+1]) / 2.0
	
#unstag vcomp
unstagv = np.zeros((len(vcomp), Y, X))
for i in xrange(Y):
	unstagv[:,i,:] = (vcomp[:,i,:] + vcomp[:,i+1,:]) / 2.0


#cdiff to get curl
curl = np.zeros((len(ucomp), Y, X))
for i in xrange(Y-2):
	for j in xrange(X-2):
		dudy = (unstagu[:,i+2,j] - unstagu[:,i,j]) / (2*dy)
		dvdx = (unstagv[:,i,j+2] - unstagu[:,i,j]) / (2*dx)
		curl[:,i+1,j+1] = dudy - dvdx
		




#seek level with interpolation
realpres = pres + presbase
Y, X = np.shape(realpres[0])
paramfind = np.zeros((Y, X))
for i in xrange(Y):
	for j in xrange(X):
		#find 'in between' value of our findpres
		for k in xrange(len(realpres)):
			if (realpres[k,i,j] < findpres):
				banding = (curl[k-1,i,j] - curl[k,i,j]) / (realpres[k-1,i,j] - realpres[k,i,j])
				paramfind[i,j] = curl[k,i,j] + (findpres - realpres[k,i,j]) * banding
				break

#masking missing data
paramfind[0,:] = np.nan
paramfind[:,0] = np.nan
paramfind[-1,:] = np.nan
paramfind[:,-1] = np.nan
paramfind = np.ma.masked_where(np.isnan(paramfind), paramfind)


###############
#plotting time#
###############

plotingtime('curl at 850 mb', paramfind)
