#!/bin/bash
#Western U.S. is divided into four parts. The field mean is calculated for each part. 
#discharge is calculated by adding runoff and baseflow
#directory of data: 

#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q default.q@compute-0-*

scenarios="historical rcp45 rcp85"
variables="PREC EVAP RUNOFF BASEFLOW"
positions="PNW Interior California SW"


for scenario in $scenarios
do
	for var in $variables
	do
		inpath=/raid3/stumbaugh/IS/CONUS/v2.2/simulator/$scenario/IPSL-CM5A-MR/wus_full.1/ncLL/*mean
		outpath=/raid3/jiawei/integrated_scenarios/IPSL-CM5A-MR/simulator/$scenario/timeseries/division/$var
		if [ ! -d $outpath ]
		then
			mkdir -p $outpath
		fi
		cdo cat $inpath $outpath/cat.nc
		cdo sellonlatbox,-124.594,-116,42,52.8438 $outpath/cat.nc $outpath/month_series_PNW
		cdo sellonlatbox,-116,-103.031,42,52.8438 $outpath/cat.nc $outpath/month_series_Interior
		cdo sellonlatbox,-124,-116,29.0312,42 $outpath/cat.nc $outpath/month_series_California
		cdo sellonlatbox,-116,-103.031,29.0312,42 $outpath/cat.nc $outpath/month_series_SW
		for pos in $positions
		do
			cdo fldmean $outpath/month_series_$pos $outpath/fldmean_month_series_$pos
		done
	done
done

for scenario in $scenarios
do
	dir_runoff=/raid3/jiawei/integrated_scenarios/IPSL-CM5A-MR/simulator/$scenario/timeseries/division/RUNOFF
	dir_baseflow=/raid3/jiawei/integrated_scenarios/IPSL-CM5A-MR/simulator/$scenario/timeseries/division/BASEFLOW
	dir_flow=/raid3/jiawei/integrated_scenarios/IPSL-CM5A-MR/simulator/$scenario/timeseries/division/FLOW
	if [ ! -d $dir_flow ]
	then
		mkdir -p $dir_flow
	fi
	for pos in $positions
	do
		cdo merge $dir_runoff/fldmean_month_series_$pos $dir_baseflow/fldmean_month_series_$pos $dir_flow/fldmean_month_series_tmp_$pos
		cdo expr,"Flow=Runoff+Baseflow" $dir_flow/fldmean_month_series_tmp_$pos $dir_flow/fldmean_month_series_$pos
		rm $dir_flow/fldmean_month_series_tmp_$pos
	done
done
