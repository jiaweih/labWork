
import numpy as np

ftemplate = '/usr1/jiawei/courses/computingWorkshop/shell/data/fluxes_{:.4f}_{:.4f}'
infile='/usr1/jiawei/courses/computingWorkshop/shell/data/lat_lon.txt'
outtemplate = '/usr1/jiawei/courses/computingWorkshop/shell/data/PythonResult/monthly_precipitation_{:.4f}_{:.4f}'

#get latitude and longitude of every dataset
lat_lon = np.genfromtxt(infile,unpack=True)
lat_lon=lat_lon.transpose()

#calculate length of years
len = lat_lon.shape
len = len[0]

LenYear = 23 #length of years
Prcp = np.zeros(12)
for i in np.arange(len):
    data = np.genfromtxt(ftemplate.format(lat_lon[i,0],lat_lon[i,1]))  
    s = data.shape
    s = s[0]  #length of all the data
    
    #calculate the sum of precipitation in the same month
    for j in np.arange(s):
        k = data[j,1].astype(int)
        Prcp[k-1] += data[j,3]
    
    #calculate monthly precipitation, there are 23 years of data
    for k in np.arange(12):
        Prcp[k]=Prcp[k]/LenYear

    f = open(outtemplate.format(lat_lon[i,0],lat_lon[i,1]),"w")
    for k in np.arange(1,13):
        f.write('%d   %f\n' %(k,Prcp[k-1]))
    f.close()
