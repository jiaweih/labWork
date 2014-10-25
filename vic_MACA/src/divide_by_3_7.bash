#!/bin/bash
#The scripts aims to divide 3-day and 7-day maximum values by 3 and 7, respectively to convert their units to daily units.

idir=/raid3/jiawei/vic_MACA/data/netCDF/max
odir=/raid3/jiawei/vic_MACA/data/netCDF/max/processed

vars1="SWE Qs SoilMst1 SoilMst2 SoilMst3 SoilMst"
vars2="max3 max7"

for var1 in $vars1
do	
	for var2 in $vars2
	do
		filename=$var2.$var1.nc
		if [ "$var2" == "max3" ]
		then
			ncap2 -s $var1=$var1/3 $idir/$filename $odir/$filename
		else
			ncap2 -s $var1=$var1/7 $idir/$filename $odir/$filename
		fi
	done
done

