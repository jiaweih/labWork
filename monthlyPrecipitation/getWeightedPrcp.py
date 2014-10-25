import numpy as np
import math

#function to get the area of each dataset covering 0.5*0.5 degrees
def get_area(lat,lon):
    radians = (90.0 - (lat + 0.25))*3.141593/180.0
    cosines = math.cos(radians) - math.cos((radians + (0.5*3.141593)/180.0))
    area = (6371221.3*6371221.3*3.141593*cosines/360.0)*0.000001
    return area

infile='/usr1/jiawei/courses/computingWorkshop/shell/data/lat_lon.txt'
ftemplate = '/usr1/jiawei/courses/computingWorkshop/shell/data/PythonResult/monthly_precipitation_{:.4f}_{:.4f}'
outtemplate ='/usr1/jiawei/courses/computingWorkshop/shell/data/PythonResult/weighedPrecipitation.txt'

#get the latitude and longitude of each dataset
lat_lon = np.genfromtxt(infile,unpack=True)
lat_lon=lat_lon.transpose()
len = lat_lon.shape
len = len[0]

num = 49 #number of files
areaprcp = np.zeros((12,num))
weightedprcp = np.zeros((12,2))
sumarea = 0


for i in np.arange(len):
    data = np.genfromtxt(ftemplate.format(lat_lon[i,0],lat_lon[i,1]))   #get monthly precipitation
    area = get_area(lat_lon[i,0],lat_lon[i,1])
    areaprcp[:,i] = area*data[:,1]  #monthly precipitation multiplied by area
    sumarea += area  #sum of areas

for i in np.arange(12):
    weightedprcp[i,0] = i + 1
    weightedprcp[i,1] = np.sum(areaprcp[i,:])/sumarea  #weighted monthly precipitation 

f = open(outtemplate,"w")
for i in np.arange(12):
    f.write('%d   %f\n' %(weightedprcp[i,0],weightedprcp[i,1]))
f.close()
