#!/bin/bash 

dir="fluxes*"
resultDir="/usr1/jiawei/courses/computingWorkshop/shell/data/bashResult"
#loop for accessing each file under desired directory
for file in $dir
do
 filename=$file
 newfile=${filename:7} #extract part of filename

#calculate the monthly precipitation, sum[$2]is the sum of precipitation in a single month in every year, n[$2]is the number of days in every month in all years. The monthly mean precipitation is redirected to files
 awk '{ sum[$2]+=$4;n[$2]+=1 } END{for(month in sum) printf("%4d %16.12f\n",\
 month, sum[month]/23.0)}' $file | sort -n > $resultDir/monthly_precipitation_$newfile
done

dir2="/usr1/jiawei/courses/computingWorkshop/shell/data/bashResult/monthly_precipitation_*"


sumArea=0.0
for((k=0;k<12;k++))
do
 sumPreci[$k]=0.0
done

i=0
for file in $dir2
do
 lat=$(echo $file | cut -d '_' -f 3)
 lon=$(echo $file | cut -d '_' -f 4)
 lat=`echo $lat | bc`
 lon=`echo $lon | bc`
 radians=`echo "((90.0-($lat+0.25))*3.141593/180.0)" | bc -l`
 cosines=`echo "c($radians)-c($radians+(0.5*3.141593)/180.0)" | bc -l`
 area[$i]=`echo "(6371221.3*6371221.3*3.141593*$cosines/360.0)*0.000001" | bc -l` #calculate the area of each gridded cell with latitude and longitude in center
 sumArea=`echo "${area[$i]}+$sumArea" | bc`  #The sum of all areas

 j=0 
 while read -a line
 do
  preci[$j]=`echo "${line[1]}"`
  sumPreci[$j]=`echo "${sumPreci[$j]}+${preci[$j]}*${area[$i]}" | bc -l` # mean precipitation in each gridded cell in every month multiplied by its area
  j=`echo "$j+1" | bc`
 done < "$file"
 
 i=`echo "$i+1" | bc`
done
 
for((i=0;i<12;i++))
do
 averPreci[$i]=`echo "${sumPreci[$i]}/$sumArea" | bc -l` #average precipitation in all gridded cells for each month

done

echo "Month" " " "AveragePrecipitation"
for((i=0;i<12;i++))
do
 month=`echo "$i+1" | bc`
 echo " " $month "  " ${averPreci[$i]}
done
exit

