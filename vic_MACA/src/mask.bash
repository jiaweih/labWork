#!/bin/bash
#This script aims to clip the domain of Columbia River Basin from ifile based on hist.sh.SWE.nc file.

ifile=SWE.nc

idir=/raid3/jiawei/vic_MACA/data/netCDF/ipynb
odir=/raid3/jiawei/vic_MACA/data/netCDF/data/means

cdo gtc,0.0 $odir/hist.sh.SWE.nc $odir/test.nc

ncwa -O -v SWE -a time $odir/test.nc $idir/date.nc

cdo ifthen $idir/date.nc $idir/$ifile $odir/days.nc
