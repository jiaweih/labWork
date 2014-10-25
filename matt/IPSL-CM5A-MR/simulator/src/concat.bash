#!/bin/bash
#concatenate the monthly files from Stumbaugh directory

#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q@compute-0-*

scenarios="historical rcp45 rcp85"
variables="PREC EVAP RUNOFF BASEFLOW"
#variables="TMAX TMIN"

for scenario in $scenarios
do
	for var in $variables
	do
		inpath=/raid3/stumbaugh/IS/CONUS/v2.2/simulator/$scenario/IPSL-CM5A-MR/wus_full.1/ncLL/*mean
		#inpath=/raid2/stumbaugh/IS/CONUS/v2.2/vicfrcnc/$scenario/IPSL-CM5A-MR/ncLL/$var/*mean
		outpath=/raid3/jiawei/integrated_scenarios/IPSL-CM5A-MR/simulator/$scenario/cat/$var
		if [ ! -d $outpath ]
		then
			mkdir -p $outpath
		fi

		cdo cat $inpath $outpath/concat.nc
	done
done
