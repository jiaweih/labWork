#!/bin/bash -x

#cwd=`pwd`
#inpath=/raid/blivneh/forcings/outputs/CONUS/nc.regen.unscaled.sept.2013
#outpath=/raid9/homefc/conus/data.sets/Livneh 
## Use 'ncra' to create monthly means for each file
#for year in {1915..2011}
#do 
#	for month in {1..12}
#	do 
#		fn=`printf "data.%04d%02d.nc" $year $month`
#		echo $fn
#		ncra $inpath/$fn $outpath/$fn
#	done
#done
#cd $outpath

# Remove all the extraneous stuff and fix the coordinate and time axes
# Use 'cdo setgrid' to change the coordinate axes from (x,y) to (lon, lat)
for file in data.??????.nc
do
	ncks -O -x -vtimestp,nav_lon,nav_lat,land,CellID $file junk.nc
	ncrename -dtstep,time junk.nc
	cdo setgrid,usgrid.txt junk.nc $file
	rm junk.nc
done

# Use 'ncrcat' to concatenate the monthly files into a monthly timeseries
# Note that the time coordinate is messed up after this, because they do 
# not start from a common base. We should fix this as well (but that is 
# not done here, I just do that when I am plotting)
ncrcat data.??????.nc data.191501_201112.nc

# Use 'ncks' to subset the region you are interested in
ncks -dlon,-180.,-110. data.191501_201112.nc west_data.191501_201112.nc
ncks -dlon,-110.,-90. -dlat,0.,38. data.191501_201112.nc south_data.191501_201112.nc
ncks -dlon,-110.,-90. -dlat,38.,90. data.191501_201112.nc north_data.191501_201112.nc
ncks -dlon,-90.,0. data.191501_201112.nc east_data.191501_201112.nc

# Use 'cdo -fldmean' to calculate a time series of the mean over the region
cdo fldmean west_data.191501_201112.nc west_data.191501_201112.mean.nc
cdo fldmean south_data.191501_201112.nc south_data.191501_201112.mean.nc
cdo fldmean north_data.191501_201112.nc north_data.191501_201112.mean.nc
cdo fldmean east_data.191501_201112.nc east_data.191501_201112.mean.nc

cd $cwd
