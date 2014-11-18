#!/bin/bash

#This scripts aims to compare PRISM dataset with Livneh dataset; PRISM spans from 1971 to 2000 with 1/120 degree, while Livneh spans from 1911 to 2011 with 1/8 degrees.
#The script does several things: 1. extract part of Livneh to match time period of PRISM  2. convert the units of Livneh's precipitation to mm/year, which is the unit of PRISM  3. remove the time dimension of Livneh  4. convert the grids of Livneh to match PRISM's  5. calculate the difference between three variables, PRISM minus Livneh   6. change the units to mm/day

input=/raid2/homefc/conus/data.sets/Livneh_PRISM
output=/raid3/jiawei/homero/data/prism/1971.2000/L13
input1=/raid3/jiawei/homero/data/prism/1971.2000/data/ppt
input2=/raid3/jiawei/homero/data/prism/1971.2000/data/tmax
input3=/raid3/jiawei/homero/data/prism/1971.2000/data/tmin

fn1=`printf "data.191501_201112.nc"`
fn2=`printf "data.197101_200012.nc"`
fn3=`printf "data.1971.2000.nc"`
fn4=`printf "data.Prec.nc"`
fn5=`printf "data.Tmax.nc"`
fn6=`printf "data.Tmin.nc"`
fn7=`printf "data.Prec.remap.nc"`
fn8=`printf "data.Tmax.remap.nc"`
fn9=`printf "data.Tmin.remap.nc"`
fn10=`printf "Prec_1971_2000.nc"`
fn11=`printf "Tmax_1971_2000.nc"`
fn12=`printf "Tmin_1971_2000.nc"`
pre_temp_diff=`printf "data.Prec.temp.diff.nc"`
tmax_diff=`printf "data.Tmax.diff.nc"`
tmin_diff=`printf "data.Tmin.diff.nc"`
pre_diff=`printf "data.Prec.diff.nc"` #final dataset desired

ncea -F -d time,673,1032 $input/$fn1 $output/$fn2

ncap2 -s "Prec=Prec*30*12" $output/$fn2 $output/$fn3

ncwa -O -v Prec -a time $output/$fn3 $output/$fn4
ncwa -O -v Tmax -a time $output/$fn3 $output/$fn5
ncwa -O -v Tmin -a time $output/$fn3 $output/$fn6

#cdo remapcon,$input1/$fn10 $output/$fn4 $output/$fn7
#cdo remapcon,$input2/$fn11 $output/$fn5 $output/$fn8
#cdo remapcon,$input3/$fn12 $output/$fn6 $output/$fn9

cdo remapcon,$output/$fn4 $input1/$fn10 $output/$fn7
cdo remapcon,$output/$fn5 $input2/$fn11 $output/$fn8
cdo remapcon,$output/$fn6 $input3/$fn12 $output/$fn9

ncdiff -v Prec $input1/$fn10 $output/$fn7 $output/$pre_temp_diff
ncdiff -v Tmax $input2/$fn11 $output/$fn8 $output/$tmax_diff
ncdiff -v Tmin $input3/$fn12 $output/$fn9 $output/$tmin_diff

#ncdiff -v Prec $output/$fn4 $output/$fn7 $output/$pre_temp_diff
#ncdiff -v Tmax $output/$fn5 $output/$fn8 $output/$tmax_diff
#ncdiff -v Tmin $output/$fn6 $output/$fn9 $output/$tmin_diff

ncap2 -s "Prec=Prec/365" $output/$pre_temp_diff $output/$pre_diff
