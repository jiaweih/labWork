#!/bin/bash

for year in {1915..2011}
do

 	ncrcat data.$year??.nc data.$year.nc

done


