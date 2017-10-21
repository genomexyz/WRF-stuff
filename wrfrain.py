#!/usr/bin/python

import numpy as np
import pandas as pd
from netCDF4 import Dataset
from datetime import datetime
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
#import wrf
#from wrf import getvar, interplevel
import Image
import matplotlib.patches as mpatches

#setting
fileWRF = 'wrfout_d03_2016-09-23_12:00:00'
#timestep = 

def plotdata(llon,dlat,rlon,ulat,delat,delon,ringan,sedang,lebat,ekstrim,time,fimage):
    print 'Plot Image : ',time.strftime('Time  %d-%m-%Y : %H.%M UTC')
    af = plt.figure(1)
    ax = plt.subplot(211)
    baseMap = Basemap(resolution='i',llcrnrlon=llon, llcrnrlat=dlat, urcrnrlon=rlon,urcrnrlat=ulat)
    #baseMap.readshapefile(fshpProv,'Propinsi',color='#FFFFFF',linewidth=0.1)
    baseMap.drawparallels(np.arange(-90,90,delat/2.),labels=[1,0,0,0],fontsize=3,linewidth=0.3,color='#999999')#,zorder=15
    #baseMap.drawmeridians(np.arange(-180,190,delon/2.),labels=[0,0,0,1],fontsize=3,linewidth=0.3,color='#999999')#,zorder=14
    #baseMap.drawcoastlines(linewidth=0.5,color='#FFFFFF')#,zorder=13
    #baseMap.drawcountries(linewidth=0.5,color='#FFFFFF')#,zorder=12
    baseMap.drawmeridians(np.arange(-180,190,delon/2.),labels=[0,0,0,1],fontsize=3,linewidth=0.3,color='#999999')#,zorder=14
    baseMap.drawcoastlines(linewidth=0.5,color='black')#,zorder=13
    baseMap.drawcountries(linewidth=0.5,color='black')#,zorder=12
    lev = [.99,2]
    col = ['red']
    colringan = ['lightgreen']
    colsedang = ['green']
    collebat = ['yellow']
    colext = ['red']
    #tick = [str(i) for i in lev]
    x,y = np.meshgrid(np.linspace(llon,rlon,len(ringan[0])),np.linspace(dlat,ulat,len(ringan)))
    hujringan = baseMap.contourf(x,y,ringan,levels=lev,colors=colringan,labels='hujan ringan')
    hujsedang = baseMap.contourf(x,y,sedang,levels=lev,colors=colsedang,labels='hujan sedang')
    hujlebat = baseMap.contourf(x,y,lebat,levels=lev,colors=collebat,labels='hujan lebat')
    hujextrim = baseMap.contourf(x,y,ekstrim,levels=lev,colors=colext,labels='hujan ekstrem')
    
    #cb = plt.colorbar(cax,ticks=lev,pad=0.01,orientation='vertical')
    #cb.ax.set_yticklabels(tick,fontsize=4.)
    #cb.ax.set_title('Temperature\n(C)',fontsize=4.) #judul colorbar
    x,y = baseMap(llon,ulat+(ulat-dlat)/20.)
    plt.text(x,y,'Prediksi hujan',fontsize=5,weight='bold') #judul gambar
    x,y = baseMap(llon,ulat+(ulat-dlat)/50.)
    #plt.text(x,y,time.strftime('Time  %A,%d-%m-%Y : %H.%M UTC'),fontsize=4) #ket waktu
    x,y = baseMap(rlon,ulat+(ulat-dlat)/50.)
    #x,y = baseMap(llon,dlat-(ulat-dlat)/15.)
    plt.text(x,y,r'$\copyright$ STMKG, '+time.strftime('%Y')+'          ',fontsize=3,color='gray',horizontalalignment='right')
    x,y = baseMap(rlon,ulat+(ulat-dlat)/20.)
    #x,y = baseMap(rlon,dlat-(ulat-dlat)/15.)
    plt.text(x,y,r'Data Source by BMKG          ',fontsize=3,color='gray',horizontalalignment='right')

    im = Image.open('stmkg50.png')
    im = np.array(im).astype(float) / 255

    af.figimage(im, 820, 900)
    ringanlegend = mpatches.Patch(color='lightgreen', label='hujan ringan')
    sedanglegend = mpatches.Patch(color='green', label='hujan sedang')
    lebatlegend = mpatches.Patch(color='yellow', label='hujan lebat')
    extlegend = mpatches.Patch(color='red', label='hujan extrim')
    plt.legend(handles=[ringanlegend,sedanglegend,lebatlegend,extlegend], loc=4, fontsize = '4')
    
    af.savefig(fimage,dpi=500,bbox_inches='tight',pad_inches=0.05)
    plt.close()
    print 'Save Image : ',fimage

#######################
#read raw data session#
#######################

wrfdata = Dataset(fileWRF, mode = 'r')

#get lat and lon
lat = wrfdata.variables['XLAT'][0,:,0]
lon = wrfdata.variables['XLONG'][0,0,:]

#get rain
rainc = wrfdata.variables['RAINC'][:]
rainnc = wrfdata.variables['RAINNC'][:]
#hujan = rainc + rainnc
print np.shape(rainc)
print rainnc
Y, X = np.shape(rainc[0])
#for i in xrange(len(wrfdata.variables['Times'][:])):
#	print wrfdata.variables['Times'][i]
#	print np.sum(hujan[i])

#print ((len(rainc)-1) / 6)
for i in xrange (1):
	#if (i < 11):
	#	continue
	#matrix of classification
	ringanmat = np.zeros((Y,X))
	sedangmat = np.zeros((Y,X))
	lebatmat = np.zeros((Y,X))
	ekstremmat = np.zeros((Y,X))

	#time step domain 3 ternyata per 10 menit
	#untuk mencari hujan perjam, 10 menit dikalikan 6 =  1 jam
	#dari dapat hint untuk mengatur ingin extract hujan per berapa waktu
	
	#cara kerja matrix rainc dan rainnc adalah jumlah curah hujan di time
	#period sebelumnya ditambah terus menerus
	#akhirnya pada array[-1] adalah total curah hujan
	#it means total precip adalah rainc[-1] + rainnc[-1]
	print (i+1)*6
	hujan = rainc[(i+1)*6] + rainnc[(i+1)*6] - rainc[i*6] - rainnc[i*6]
	print np.sum(hujan)
	for j in xrange(Y):
		for k in xrange(X):
			if hujan[j,k] < 5:
				if hujan[j,k] > 1:
					ringanmat[j,k] = 1
			elif hujan[j,k] < 10:
				sedangmat[j,k] = 1
			elif hujan[j,k] < 15:
				lebatmat[j,k] = 1
			else:
				ekstremmat[j,k] = 1
	##################
	#plotting session#
	##################

	llon = lon[0]
	rlon = lon[-1]
	dlat = lat[0]
	ulat = lat[-1]
	delat,delon = 10,10
	time = datetime(2016,9,24,0,0)
	print i
	fimage = 'time step ke-'+str(i)
	plotdata(llon,dlat,rlon,ulat,delat,delon,ringanmat,sedangmat,lebatmat,ekstremmat,time,fimage)
