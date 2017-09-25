#!/bin/bash

#setting
savedir="/home/genomexyz/WRF/Build_WRF/DATA/XXX"
forecasttot=4
forecasttimestep=3
year=2016
month=1
startday=2
endday=30
starthour=0


for ((i=$(($startday)); i<=$endday; i++)); do
	for ((j=0; j<2; j++)); do
		if (( $month < 10 )); then
			bulan=0$month
		else
			bulan=$month
		fi
		if (( $i < 10 )); then
			hari=0$i
		else
			hari=$i
		fi
		if (( $j == 0 )); then
			mode="_0000_"
		else
			mode="_1200_"
		fi
		wget --directory-prefix="$savedir" "https://nomads.ncdc.noaa.gov/data/gfs4/""$year$bulan"/"$year$bulan$hari"/gfs_4_"$year$bulan$hari$mode"000.grb2
		wget --directory-prefix="$savedir" "https://nomads.ncdc.noaa.gov/data/gfs4/""$year$bulan"/"$year$bulan$hari"/gfs_4_"$year$bulan$hari$mode"003.grb2
		wget --directory-prefix="$savedir" "https://nomads.ncdc.noaa.gov/data/gfs4/""$year$bulan"/"$year$bulan$hari"/gfs_4_"$year$bulan$hari$mode"006.grb2
		wget --directory-prefix="$savedir" "https://nomads.ncdc.noaa.gov/data/gfs4/""$year$bulan"/"$year$bulan$hari"/gfs_4_"$year$bulan$hari$mode"009.grb2
		wget --directory-prefix="$savedir" "https://nomads.ncdc.noaa.gov/data/gfs4/""$year$bulan"/"$year$bulan$hari"/gfs_4_"$year$bulan$hari$mode"012.grb2
	done
done
