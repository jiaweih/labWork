#!/bin/bash
#cdo timmax command can obtain the largest value on a single day by comparing values on the same day in different years, the result will be one value for each day in a year.
#cdo runsum,n command can sum the value in n consecutive days.

input=/raid3/jiawei/vic_MACA/data/netCDF
output=/raid3/jiawei/vic_MACA/data/netCDF/max
vars="SWE Qs SoilMst1 SoilMst2 SoilMst3 SoilMst"
#vars="SoilMst1 SoilMst2 SoilMst3 SoilMst"

for var in $vars
do 
	filename=hist.sh.${var}.nc
	max1=max1.${var}.nc
	max3=max3.${var}.nc
	max7=max7.${var}.nc
	sum3=sum3.hist.sh.${var}.nc
	sum7=sum7.hist.sh.${var}.nc
	cdo timmax $input/$filename $output/$max1
	cdo runsum,3 $input/$filename $output/$sum3
	cdo runsum,7 $input/$filename $output/$sum7
	cdo timmax $output/$sum3 $output/$max3
	cdo timmax $output/$sum7 $output/$max7
done

