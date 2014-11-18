#!/bin/bash

#This scripts aims to compare PRISM dataset with Livneh dataset; PRISM spans from 1971 to 2000 with 1/120 degree, while Livneh spans from 1911 to 2011 with 1/8 degrees.
#The script does several things: 1. extract part of Livneh to match time period of PRISM  2. convert the units of Livneh's precipitation to mm/year, which is the unit of PRISM  3. remove the time dimension of Livneh  4. convert the grids of Livneh to match PRISM's  5. calculate the difference between three variables, PRISM minus Livneh   6. change the units to mm/day

input=/raid2/homefc/conus/data.sets/Livneh_PRISM
output=/raid3/jiawei/homero/data/prism/1971.2000/L13
input1=/raid3/jiawei/homero/data/prism/1971.2000/data/ppt
input2=/raid3/jiawei/homero/data/prism/1971.2000/data/tmax
input3=/raid3/jiawei/homero/data/prism/1971.2000/data/tmin

livneh_1915_2011=`printf "data.191501_201112.nc"` #Livneh original dataset
livneh_1971_2000=`printf "data.197101_200012.nc"` #Livneh dataset from 1971 to 2000
livneh_1971_2000_new_units=`printf "data.1971.2000.nc"` #Livneh dataset after changing units

#Livneh dataset after removing time dimension
livneh_prec_no_time=`printf "data.Prec.nc"`
livneh_tmax_no_time=`printf "data.Tmax.nc"`
livneh_tmin_no_time=`printf "data.Tmin.nc"`

#remap Livneh dataset to math the grids of PRISM dataset
prism_prec_remap=`printf "data.Prec.remap.nc"`
prism_tmax_remap=`printf "data.Tmax.remap.nc"`
prism_tmin_remap=`printf "data.Tmin.remap.nc"`

#PRSIM original dataset
prism_prec_1971_2000=`printf "Prec_1971_2000.nc"`
prism_tmax_1971_2000=`printf "Tmax_1971_2000.nc"`
prism_tmin_1971_2000=`printf "Tmin_1971_2000.nc"`

# the difference between PRISM and Livneh ( PRISM - Livneh )
prec_temp_diff=`printf "data.Prec.temp.diff.nc"` 
tmax_diff=`printf "data.Tmax.diff.nc"`
tmin_diff=`printf "data.Tmin.diff.nc"`

#daily precipitation for the difference
prec_diff=`printf "data.Prec.diff.nc"`

#extract parts of the Livneh data to match the time periods of PRSIM 
ncea -F -d time,673,1032 $input/$livneh_1915_2011 $output/$livneh_1971_2000

#convert the units of precipitation of Livneh data, 30 means 30 days in a month,12 means 12 months in a year; so the final unit will be mm/year.
ncap2 -s "Prec=Prec*30*12" $output/$livneh_1971_2000 $output/$livneh_1971_2000_new_units

#remove the time dimension of Livneh dataset by averaging the file over the time dimension as an axis
ncwa -O -v Prec -a time $output/$livneh_1971_2000_new_units $output/$livneh_prec_no_time
ncwa -O -v Tmax -a time $output/$livneh_1971_2000_new_units $output/$livneh_tmax_no_time
ncwa -O -v Tmin -a time $output/$livneh_1971_2000_new_units $output/$livneh_tmin_no_time

#convert grid of PRISM to that of Livneh
cdo remapcon,$output/$livneh_prec_no_time $input1/$prism_prec_1971_2000 $output/$prism_prec_remap
cdo remapcon,$output/$livneh_tmax_no_time $input2/$prism_tmax_1971_2000 $output/$prism_tmax_remap
cdo remapcon,$output/$livneh_tmin_no_time $input3/$prism_tmin_1971_2000 $output/$prism_tmin_remap

#calculate the differences of three variables, PRISM minus Livneh
ncdiff -v Prec $output/$prism_prec_remap $output/$livneh_prec_no_time $output/$prec_temp_diff
ncdiff -v Tmax $output/$prism_tmax_remap $output/$livneh_tmax_no_time $output/$tmax_diff
ncdiff -v Tmin $output/$prism_tmin_remap $output/$livneh_tmin_no_time $output/$tmin_diff

#change units to mm/day
ncap2 -s "Prec=Prec/365" $output/$prec_temp_diff $output/$prec_diff
