
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>
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
import os

def plot_monthly_mean(ifile,start,end,store_dir,fig_size,fmt_mean,fmt_smoothing,fig_txt_mean,fig_txt_smoothing,smoothing_step,linewidth,\
                      legend_loc,legend_size,xlabel,ylabel,y_unit,ymin_limit,ymax_limit,label_size,tick_size,pos_name):
    df = get_data(ifile,start,end)
    df.plot(style=fmt_mean,label=fig_txt_mean)
    pds.rolling_mean(df,smoothing_step,center=True).plot(style=fmt_smoothing,label=fig_txt_smoothing,linewidth=2.5)
    ax.legend(loc=legend_loc,prop={'size':legend_size})
    ax.set_xlabel(xlabel,fontsize=label_size)
    ax.set_ylabel(ylabel+y_unit,fontsize=label_size)
    ax.set_ylim([ymin_limit,ymax_limit])
    ax.tick_params(axis='both',which='major',labelsize=tick_size)

# <codecell>

def plot_annual_mean(ifile,start,end,store_dir,fig_size,fmt_mean,fmt_smoothing,fig_txt_mean,fig_txt_smoothing,smoothing_step,\
                     linewidth,legend_loc,legend_size,xlabel,ylabel,y_unit,ymin_limit,ymax_limit,label_size,tick_size,pos_name):
    df = get_data(ifile,start,end)
    df.resample('A',how='mean').plot(style=fmt_mean,label=fig_txt_mean)
    df_mean = df.resample('A',how='mean')
    pds.rolling_mean(df_mean,smoothing_step,center=True).plot(style=fmt_smoothing,label=fig_txt_smoothing,linewidth=2.5)
    ax.legend(loc=legend_loc,prop={'size':legend_size})
    ax.set_xlabel(xlabel,fontsize=label_size)
    ax.set_ylabel(ylabel+y_unit,fontsize=label_size)
    ax.set_ylim([ymin_limit,ymax_limit])
    ax.tick_params(axis='both',which='major',labelsize=tick_size)
    fig.savefig(store_dir,dpi=300)

# <codecell>

def plot_mean_monthly(ifile,start,end,store_dir,fig_size,fmt,fig_txt,linewidth,\
                      legend_loc,legend_size,xlabel,ylabel,y_unit,ymin_limit,ymax_limit,label_size,tick_size,pos_name):
    monthes=['Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep']
    df = get_data(ifile,start,end)
    df.groupby(lambda x: water_month(x.month)).mean().plot(style=fmt,label=fig_txt)  
    ax.legend(loc=legend_loc,prop={'size':legend_size})
    ax.set_xlabel(xlabel,fontsize=label_size)
    ax.set_ylabel(ylabel+y_unit,fontsize=label_size)
    ax.set_ylim([ymin_limit,ymax_limit])
    ax.set_xticks(np.arange(12))
    ax.set_xlim([-0.5,11.5])
    ax.set_xticklabels(monthes)
    ax.tick_params(axis='both',which='major',labelsize=tick_size) 

# <codecell>

def plot_monthly_mean_together(outdir_fldmean_month_series,start,end,variables,scenarios,store_dir_monthly_mean0,fig_size,\
                               smoothing_step,linewidth,legend_loc,legend_size,xlabel,ylabel,ymin_limit,\
                          ymax_limit,label_size,tick_size):
    for var in variables:
        if var == 'SOIL_MOIST' or var == 'SWE':
            y_unit = '(mm)'
        elif var == 'TMAX' or var == 'TMIN' or var == 'TAVG':
            y_unit = ' ($^\circ$C)'
        else:
            y_unit = ' (mm/day)'      
        for scenario in scenarios:         
            fig = plt.figure(figsize=(fig_size))
            store_dir_monthly_mean = store_dir_monthly_mean0.format(scenario,var)
            ax = fig.add_subplot(111)
            for idx,pos in enumerate(positions):
                pos_name = pos_names[idx]
                fig_txt_mean = pos_name + ' Monthly Mean ' + '(' + scenario + ')'   
                fig_txt_smoothing = '{} Months Moving Average'.format(smoothing_step)     
                ifile = outdir_fldmean_month_series.format(scenario,var,pos_name)
                df = get_data(ifile,start,end)
                fmt = fmts[idx]
                fig_txt= pos_name
                pds.rolling_mean(df,smoothing_step,center=True).plot(style=fmt,label=fig_txt,linewidth=linewidth)                          
            ax.legend(loc=legend_loc,prop={'size':legend_size})
            ax.set_xlabel(xlabel,fontsize=label_size)
            ax.set_ylabel(ylabel+y_unit,fontsize=label_size)
            ax.set_ylim([ymin_limit,ymax_limit])
            ax.tick_params(axis='both',which='major',labelsize=tick_size)
            fig.savefig(store_dir_monthly_mean,dpi=300)

# <codecell>

def plot_annual_mean_together(outdir_fldmean_month_series,start,end,variables,scenarios,store_dir_annual_mean0,fig_size,\
                               smoothing_step,linewidth,legend_loc,legend_size,xlabel,ylabel,ymin_limit,\
                          ymax_limit,label_size,tick_size):
    for var in variables:
        if var == 'SOIL_MOIST' or var == 'SWE':
            y_unit = '(mm)'
        elif var == 'TMAX' or var == 'TMIN' or var == 'TAVG':
            y_unit = ' ($^\circ$C)'
        else:
            y_unit = ' (mm/day)'      
        for scenario in scenarios:         
            fig = plt.figure(figsize=(fig_size))
            store_dir_annual_mean = store_dir_annual_mean0.format(scenario,var)
            ax = fig.add_subplot(111)
            for idx,pos in enumerate(positions):
                pos_name = pos_names[idx]
                fig_txt_mean = pos_name + ' Monthly Mean ' + '(' + scenario + ')'   
                fig_txt_smoothing = '{} Months Moving Average'.format(smoothing_step)  
                fmt = fmts[idx]
                fig_txt= pos_name 
                ifile = outdir_fldmean_month_series.format(scenario,var,pos_name)          
                df = get_data(ifile,start,end)
                df_mean = df.resample('A',how='mean')
                pds.rolling_mean(df_mean,smoothing_step,center=True).plot(style=fmt,label=fig_txt,linewidth=linewidth)                          
            ax.legend(loc=legend_loc,prop={'size':legend_size})
            ax.set_xlabel(xlabel,fontsize=label_size)
            ax.set_ylabel(ylabel+y_unit,fontsize=label_size)
            ax.set_ylim([ymin_limit,ymax_limit])
            ax.tick_params(axis='both',which='major',labelsize=tick_size)
            fig.savefig(store_dir_annual_mean,dpi=300)

# <codecell>

def plot_mean_monthly_together(outdir_fldmean_month_series,start,end,variables,scenarios,store_dir_annual_mean0,fig_size,\
                               smoothing_step,linewidth,legend_loc,legend_size,xlabel,ylabel,ymin_limit,\
                          ymax_limit,label_size,tick_size):
    monthes=['Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep']
    for var in variables:
        if var == 'SOIL_MOIST' or var == 'SWE':
            y_unit = '(mm)'
        elif var == 'TMAX' or var == 'TMIN' or var == 'TAVG':
            y_unit = ' ($^\circ$C)'
        else:
            y_unit = ' (mm/day)'      
        for scenario in scenarios:         
            fig = plt.figure(figsize=(fig_size))
            store_dir_annual_mean = store_dir_annual_mean0.format(scenario,var)
            ax = fig.add_subplot(111)
            for idx,pos in enumerate(positions):
                pos_name = pos_names[idx]
                fig_txt_mean = pos_name + ' Monthly Mean ' + '(' + scenario + ')'   
                fig_txt_smoothing = '{} Months Moving Average'.format(smoothing_step)  
                fmt = fmts[idx]
                fig_txt= pos_name 
                ifile = outdir_fldmean_month_series.format(scenario,var,pos_name)          
                df = get_data(ifile,start,end)
                df.groupby(lambda x: water_month(x.month)).mean().plot(style=fmt,label=fig_txt,linewidth=linewidth)                          
            ax.legend(loc=legend_loc,prop={'size':legend_size})
            ax.set_xlabel(xlabel,fontsize=label_size)
            ax.set_ylabel(ylabel+y_unit,fontsize=label_size)
            ax.set_ylim([ymin_limit,ymax_limit])
            ax.set_xticks(np.arange(12))
            ax.set_xlim([-0.5,11.5])
            ax.set_xticklabels(monthes)
            ax.tick_params(axis='both',which='major',labelsize=tick_size)
            fig.savefig(store_dir_annual_mean,dpi=300)

# <codecell>

def plot_mean_monthly_scenarios(ifile,start,end,store_dir,fig_size,fmt,fig_txt,linewidth,\
                      legend_loc,legend_size,xlabel,ylabel,y_unit,ymin_limit,ymax_limit,label_size,tick_size,pos_name):
    monthes=['Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep']
    df = get_data(ifile,start,end)
    df.groupby(lambda x: water_month(x.month)).mean().plot(style=fmt,label=fig_txt)  

# <codecell>

def get_data(ifile,start=None,end=None):
    nc = Dataset(ifile,'r')
    for key in nc.variables.keys():
        if key not in nc.dimensions.keys():
            var = key
    time =  num2date(nc.variables['Time'][:],nc.variables['Time'].units,calendar = nc.variables['Time'].calendar)
    df = pd.Series(nc.variables[var][:,0,0],index = time)
    nc.close()
    if start:
        df = df[start:]
    if end:
        df = df[:end]
    return df

# <codecell>

def water_month(indate):
    moy = indate
    if moy >= 10:
        outmonth = moy - 10
    else:
        outmonth = moy + 2
    return outmonth

# <codecell>

def get_fldmean(pos,ifile,ofile_cat,ofile_area,ofile_fldmean):
    if not(os.path.exists(ofile_cat)):
        cdo.cat(input = ifile, output = ofile_cat)
    if not(os.path.exists(ofile_area)):
        cdo.sellonlatbox(pos,input = ofile_cat,output=ofile_area)
    if not(os.path.exists(ofile_fldmean)):
        cdo.fldmean(input = ofile_area, output = ofile_fldmean)

# <codecell>

def process_data(indir,positions,pos_names,variables,scenarios,global_month_series,local_month_series,local_fldmean_month_series):
    #positions = positions
    import os
    for idx,pos in enumerate(positions):
        for var in variables:
            for scenario in scenarios:
                ifile = indir.format(scenario,var)
                file_month_series = global_month_series.format(scenario,var,pos_names[idx])
                file_local = local_month_series.format(scenario,var,pos_names[idx])
                file_fldmean = local_fldmean_month_series.format(scenario,var,pos_names[idx])        
                if not(os.path.exists(file_month_series)):
                    get_fldmean(pos,ifile,file_month_series,file_local,file_fldmean)
                if os.path.exists(ifile):
                    os.remove(ifile)

# <codecell>

def get_vmin_vmax(ifile,start,end):
    df = get_data(ifile)
    vmin = np.floor(df.min())
    vmax = np.ceil(df.max())
    return (vmin,vmax)

# <codecell>

def get_y_unit(var):
    if var == 'SOIL_MOIST' or var == 'SWE':
        y_unit = '(mm)'
    elif var == 'TMAX' or var == 'TMIN':
        y_unit = ' ($^\circ$C)'
    else:
        y_unit = ' (mm/day)'
    return y_unit

# <codecell>

def get_positions():    
    '''return a list of the range of latitudes and longitudes of NW,NE,SW,SE'''
    '''dividing point is 42N,116W'''
    positions = ['-124.594,-116,42,52.8438','-116,-103.031,42,52.8438','-124,-116,29.0312,42','-116,-103.031,29.0312,42']
    return positions

# <codecell>

def get_pos_names():
    '''return a list of names for NW,NE,SW,SE'''
    pos_names = ['PNW','Interior','California','SW']
    return pos_names

# <codecell>

def get_ylabels():
    '''return a list of names for ylabels'''
    ylabels = {'TMAX':'Tmax','TMIN':'Tmin','RUNOFF':'Runoff','PREC':'Precipitation','EVAP':'Evaporation'}
    return ylabels

# <codecell>

def get_var_names():
    '''return the variable names for accessing netCDF file'''
    var_names={'TMAX':'air_temp_tmax','TMIN':'air_temp_tmin'}
    return var_names

