#! /usr/bin/env python
'''The western U.S. is divided into four areas. The mean monthly timeseries of historical, rcp45, rcp85 are plotted for each area.'''

from cdo import *
from mpl_toolkits.basemap import Basemap, cm
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import datetime as dt
from netCDF4 import date2num, num2date
import pandas as pd
import pandas.stats.moments as pds
import os as os
from timeseries_function import *
#%matplotlib inline
cdo = Cdo()

indir='/raid2/stumbaugh/IS/CONUS/v2.2/vicfrcnc/{}/IPSL-CM5A-MR/ncLL/{}/*_mean' 
out_parent_dir = '/raid3/jiawei/stumbaugh/simulator/{}/timeseries/division/{}/'

outdir_month_series = out_parent_dir + 'month_series_{}' 
outdir_fldmean_month_series = out_parent_dir + 'fldmean_month_series_{}'
outdir_month_series = out_parent_dir + 'series_{}'

store_dir_monthly_mean0 = '/raid3/jiawei/stumbaugh/figures/IPSL-CM5A-MR/timeseries/monthly_series_division_{}_{}.png'  
store_dir_annual_mean0 = '/raid3/jiawei/stumbaugh/figures/IPSL-CM5A-MR/timeseries/annual_series_division_all_{}.png' 
store_dir_mean_average0 = '/raid3/jiawei/stumbaugh/figures/IPSL-CM5A-MR/timeseries/mean_monthly_division_all_{}.png' 
variables=['TMAX']
var_names=get_var_names()
#scenarios = ['historical']
scenarios = ['historical','rcp45','rcp85']


positions = get_positions()
#positions = ['-124.594,-116,42,52.8438','-116,-103.031,42,52.8438','-124,-116,29.0312,42','-116,-103.031,29.0312,42']
pos_names = get_pos_names()
fig_size = (22,18)
fmt = 'b-'
fmts = ['b-','g-','r-']
fmt_mean = 'b-'
fmt_smoothing = 'r'
linewidth = 1.5
legend_loc = 'best'
legend_size = 16
height_ratio = [1,1]
width_ratio = [1,1]
wspace = 0.15
hspace = 0.15
xlabel = 'Month'
ylabels = get_ylabels()
label_size = 19
tick_size = 18
nrow = 2
ncol = 2
start = None
end = None
dpi = 300

process_data(indir,positions,pos_names,variables,scenarios,outdir_month_series,outdir_month_series,outdir_fldmean_month_series)   

for var in variables:
    ylabel = ylabels[var]  
    y_unit = get_y_unit(var)
    grid = gridspec.GridSpec(nrow,ncol,height_ratios=height_ratio,width_ratios=width_ratio,wspace=wspace,hspace=hspace)
    fig = plt.figure(figsize=(fig_size))
    store_dir = store_dir_mean_average0.format(var)
    monthes=['Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep']
    for idx,pos in enumerate(positions):
        ax = fig.add_subplot(grid[idx])
        pos_name = pos_names[idx]
        for idy,scenario in enumerate(scenarios):                
            ymax_limit = 46
            ymin_limit = -5              
            file_fldmean = outdir_fldmean_month_series.format(scenario,var,pos_name) 
            fmt = fmts[idy]
            fig_txt = scenario
            plot_mean_monthly_scenarios(file_fldmean,start,end,store_dir,fig_size,fmt,fig_txt,\
                              linewidth,legend_loc,legend_size,xlabel,ylabel,y_unit,ymin_limit,ymax_limit,label_size,tick_size,pos_name)
        ax.legend(loc=legend_loc,prop={'size':legend_size})
        ax.set_xlabel(xlabel,fontsize=label_size)
        ax.set_ylabel(ylabel+y_unit,fontsize=label_size)
        ax.set_ylim([ymin_limit,ymax_limit])
        ax.set_xticks(np.arange(12))
        ax.set_xlim([-0.5,11.5])
        ax.set_xticklabels(monthes)
        ax.tick_params(axis='both',which='major',labelsize=tick_size)
    fig.savefig(store_dir,dpi=dpi)
            
