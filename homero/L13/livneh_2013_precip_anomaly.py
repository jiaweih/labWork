# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# import modules
from netCDF4 import Dataset
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import matplotlib.gridspec as gridspec

# <codecell>

# set default font size
mpl.rcParams.update({'font.size': 16})
regions = ['west', 'north', 'south', 'east']
# define the template for the filename - update for your directories
fntemplate = './{}_data.191501_201112.mean.nc'
# define time index: You could calculate this from the netcdf files, 
# but it is easier this way. Because the last record is (2011, 12), you 
# need to have the end beyond that (2012, 1, 1)
tdx = pd.date_range(start=dt.datetime(1915,1,1), end=dt.datetime(2012,1,1), freq='M')
# Variable to look at
var = 'Prec'
sdx = 0
seasons = ['DJF', 'MAM', 'JJA', 'SON']
# define months in each season
months = [[12,1,2], [3,4,5], [6,7,8], [9,10,11]]
for season in seasons:
    idx = 0
    # Create figure
    fig = plt.figure(figsize=(20,20))
    # Layout panels in figure
    grid = gridspec.GridSpec(2, 2, height_ratios=[1,1,1,1,0.05], wspace=0.05, hspace=0.05)
    for region in regions:
        # open panel
        ax = fig.add_subplot(grid[idx])
        # read netcdf file
        nc = Dataset(fntemplate.format(region), 'r')
        data = nc.variables[var][:].flatten()
        nc.close()
        # convert data to time series object with defined time index. Again, 
        # this can be calculated from the netcdf file, but that is more work
        df = pd.Series(data, tdx)
        # subset the time series by finding the months in the time series 
        # that are in the current season
        df = df[np.in1d(df.index.month, months[sdx])]
        # resample to annual by taking the mean of the months within the year
        ann = df.resample('A', how='mean')
        # calculate a 10 year rolling mean anomaly
        y = pd.rolling_mean(ann-ann.mean(), 10, center=True)
        # plot the 10 year rolling mean anomaly (line)
        y.plot(color='black')
        # color the positive anomalies blue
        plt.fill_between(y.index, 0, y, where=y>0, interpolate=True, facecolor='blue')
        # color the negative anomalies red
        plt.fill_between(y.index, 0, y, where=y<0, interpolate=True, facecolor='red')
        # plot the annual anomalies as a black line
        (ann-ann.mean()).plot(color='black')
        # set the y-axis label
        ax.set_ylabel('Precipitation anomaly (mm/day)')
        # no y-axis on the right hand column
        if idx%2 == 1:
            ax.set_yticklabels([]) # turn off the tick labels on the y-axis
            ax.set_ylabel('')
        # no x-axis labels on the top row
        if idx < 2:
            ax.set_xticklabels([]) # turn off the tick labels on the x-axis
        # add text
        ax.text(0.10, 0.97, seasons[sdx], verticalalignment='top', horizontalalignment='left',
                transform=ax.transAxes, color='black', fontsize=16)
        ax.text(0.97, 0.97, region, verticalalignment='top', horizontalalignment='right',
                transform=ax.transAxes, color='black', fontsize=16)
        ax.text(0.5, 0.97, "1915-2011", verticalalignment='top', horizontalalignment='center',
                transform=ax.transAxes, color='black', fontsize=16) 
        ax.text(0.5, 0.91, "UNSCALED", verticalalignment='top', horizontalalignment='center',
                transform=ax.transAxes, color='black', fontsize=16)
        # make the y-axis limits symmetric
        ax.set_ylim([-1.5,1.5])
        # plot a horizontal line at y=0
        plt.axhline(0, linewidth=2, color='black')
        idx += 1
    # write the plot to file
    plt.savefig('livneh_2013_anomaly_prcp_{}.png'.format(season))
    sdx += 1

# <codecell>

# Same for Maximum temperature

# set default font size
mpl.rcParams.update({'font.size': 16})
regions = ['west', 'north', 'south', 'east']
# define the template for the filename - update for your directories
fntemplate = './{}_data.191501_201112.mean.nc'
# define time index: You could calculate this from the netcdf files, 
# but it is easier this way. Because the last record is (2011, 12), you 
# need to have the end beyond that (2012, 1, 1)
tdx = pd.date_range(start=dt.datetime(1915,1,1), end=dt.datetime(2012,1,1), freq='M')
# Variable to look at
var = 'Tmax'
sdx = 0
seasons = ['DJF', 'MAM', 'JJA', 'SON']
# define months in each season
months = [[12,1,2], [3,4,5], [6,7,8], [9,10,11]]
for season in seasons:
    idx = 0
    # Create figure
    fig = plt.figure(figsize=(20,20))
    # Layout panels in figure
    grid = gridspec.GridSpec(2, 2, height_ratios=[1,1,1,1,0.05], wspace=0.05, hspace=0.05)
    for region in regions:
        # open panel
        ax = fig.add_subplot(grid[idx])
        # read netcdf file
        nc = Dataset(fntemplate.format(region), 'r')
        data = nc.variables[var][:].flatten()
        nc.close()
        # convert data to time series object with defined time index. Again, 
        # this can be calculated from the netcdf file, but that is more work
        df = pd.Series(data, tdx)
        # subset the time series by finding the months in the time series 
        # that are in the current season
        df = df[np.in1d(df.index.month, months[sdx])]
        # resample to annual by taking the mean of the months within the year
        ann = df.resample('A', how='mean')
        # calculate a 10 year rolling mean anomaly
        y = pd.rolling_mean(ann-ann.mean(), 10, center=True)
        # plot the 10 year rolling mean anomaly (line)
        y.plot(color='black')
        # color the positive anomalies blue
        plt.fill_between(y.index, 0, y, where=y>0, interpolate=True, facecolor='blue')
        # color the negative anomalies red
        plt.fill_between(y.index, 0, y, where=y<0, interpolate=True, facecolor='red')
        # plot the annual anomalies as a black line
        (ann-ann.mean()).plot(color='black')
        # set the y-axis label
        ax.set_ylabel('Tmax anomaly ($^o$C)')
        # no y-axis on the right hand column
        if idx%2 == 1:
            ax.set_yticklabels([]) # turn off the tick labels on the y-axis
            ax.set_ylabel('')
        # no x-axis labels on the top row
        if idx < 2:
            ax.set_xticklabels([]) # turn off the tick labels on the x-axis
        # add text
        ax.text(0.10, 0.97, seasons[sdx], verticalalignment='top', horizontalalignment='left',
                transform=ax.transAxes, color='black', fontsize=16)
        ax.text(0.97, 0.97, region, verticalalignment='top', horizontalalignment='right',
                transform=ax.transAxes, color='black', fontsize=16)
        ax.text(0.5, 0.97, "1915-2011", verticalalignment='top', horizontalalignment='center',
                transform=ax.transAxes, color='black', fontsize=16)
        # make the y-axis limits symmetric
        ax.set_ylim([-3.5,3.5])
        # plot a horizontal line at y=0
        plt.axhline(0, linewidth=2, color='black')
        idx += 1
    # write the plot to file
    plt.savefig('livneh_2013_anomaly_tmax_{}.png'.format(season))
    sdx += 1

# <codecell>

# Same for minimum temperature

# set default font size
mpl.rcParams.update({'font.size': 16})
regions = ['west', 'north', 'south', 'east']
# define the template for the filename - update for your directories
fntemplate = './{}_data.191501_201112.mean.nc'
# define time index: You could calculate this from the netcdf files, 
# but it is easier this way. Because the last record is (2011, 12), you 
# need to have the end beyond that (2012, 1, 1)
tdx = pd.date_range(start=dt.datetime(1915,1,1), end=dt.datetime(2012,1,1), freq='M')
# Variable to look at
var = 'Tmin'
sdx = 0
seasons = ['DJF', 'MAM', 'JJA', 'SON']
# define months in each season
months = [[12,1,2], [3,4,5], [6,7,8], [9,10,11]]
for season in seasons:
    idx = 0
    # Create figure
    fig = plt.figure(figsize=(20,20))
    # Layout panels in figure
    grid = gridspec.GridSpec(2, 2, height_ratios=[1,1,1,1,0.05], wspace=0.05, hspace=0.05)
    for region in regions:
        # open panel
        ax = fig.add_subplot(grid[idx])
        # read netcdf file
        nc = Dataset(fntemplate.format(region), 'r')
        data = nc.variables[var][:].flatten()
        nc.close()
        # convert data to time series object with defined time index. Again, 
        # this can be calculated from the netcdf file, but that is more work
        df = pd.Series(data, tdx)
        # subset the time series by finding the months in the time series 
        # that are in the current season
        df = df[np.in1d(df.index.month, months[sdx])]
        # resample to annual by taking the mean of the months within the year
        ann = df.resample('A', how='mean')
        # calculate a 10 year rolling mean anomaly
        y = pd.rolling_mean(ann-ann.mean(), 10, center=True)
        # plot the 10 year rolling mean anomaly (line)
        y.plot(color='black')
        # color the positive anomalies blue
        plt.fill_between(y.index, 0, y, where=y>0, interpolate=True, facecolor='blue')
        # color the negative anomalies red
        plt.fill_between(y.index, 0, y, where=y<0, interpolate=True, facecolor='red')
        # plot the annual anomalies as a black line
        (ann-ann.mean()).plot(color='black')
        # set the y-axis label
        ax.set_ylabel('Tmin anomaly ($^o$C)')
        # no y-axis on the right hand column
        if idx%2 == 1:
            ax.set_yticklabels([]) # turn off the tick labels on the y-axis
            ax.set_ylabel('')
        # no x-axis labels on the top row
        if idx < 2:
            ax.set_xticklabels([]) # turn off the tick labels on the x-axis
        # add text
        ax.text(0.10, 0.97, seasons[sdx], verticalalignment='top', horizontalalignment='left',
                transform=ax.transAxes, color='black', fontsize=16)
        ax.text(0.97, 0.97, region, verticalalignment='top', horizontalalignment='right',
                transform=ax.transAxes, color='black', fontsize=16)
        ax.text(0.5, 0.97, "1915-2011", verticalalignment='top', horizontalalignment='center',
                transform=ax.transAxes, color='black', fontsize=16)
        # make the y-axis limits symmetric
        ax.set_ylim([-3.5,3.5])
        # plot a horizontal line at y=0
        plt.axhline(0, linewidth=2, color='black')
        idx += 1
    # write the plot to file
    plt.savefig('livneh_2013_anomaly_tmin_{}.png'.format(season))
    sdx += 1

# <codecell>

# Same for wind

# set default font size
mpl.rcParams.update({'font.size': 16})
regions = ['west', 'north', 'south', 'east']
# define the template for the filename - update for your directories
fntemplate = './{}_data.191501_201112.mean.nc'
# define time index: You could calculate this from the netcdf files, 
# but it is easier this way. Because the last record is (2011, 12), you 
# need to have the end beyond that (2012, 1, 1)
tdx = pd.date_range(start=dt.datetime(1915,1,1), end=dt.datetime(2012,1,1), freq='M')
# Variable to look at
var = 'Wind'
sdx = 0
seasons = ['DJF', 'MAM', 'JJA', 'SON']
# define months in each season
months = [[12,1,2], [3,4,5], [6,7,8], [9,10,11]]
for season in seasons:
    idx = 0
    # Create figure
    fig = plt.figure(figsize=(20,20))
    # Layout panels in figure
    grid = gridspec.GridSpec(2, 2, height_ratios=[1,1,1,1,0.05], wspace=0.05, hspace=0.05)
    for region in regions:
        # open panel
        ax = fig.add_subplot(grid[idx])
        # read netcdf file
        nc = Dataset(fntemplate.format(region), 'r')
        data = nc.variables[var][:].flatten()
        nc.close()
        # convert data to time series object with defined time index. Again, 
        # this can be calculated from the netcdf file, but that is more work
        df = pd.Series(data, tdx)
        # subset the time series by finding the months in the time series 
        # that are in the current season
        df = df[np.in1d(df.index.month, months[sdx])]
        # resample to annual by taking the mean of the months within the year
        ann = df.resample('A', how='mean')
        # calculate a 10 year rolling mean anomaly
        y = pd.rolling_mean(ann-ann.mean(), 10, center=True)
        # plot the 10 year rolling mean anomaly (line)
        y.plot(color='black')
        # color the positive anomalies blue
        plt.fill_between(y.index, 0, y, where=y>0, interpolate=True, facecolor='blue')
        # color the negative anomalies red
        plt.fill_between(y.index, 0, y, where=y<0, interpolate=True, facecolor='red')
        # plot the annual anomalies as a black line
        (ann-ann.mean()).plot(color='black')
        # set the y-axis label
        ax.set_ylabel('Wind speed anomaly (m/s)')
        # no y-axis on the right hand column
        if idx%2 == 1:
            ax.set_yticklabels([]) # turn off the tick labels on the y-axis
            ax.set_ylabel('')
        # no x-axis labels on the top row
        if idx < 2:
            ax.set_xticklabels([]) # turn off the tick labels on the x-axis
        # add text
        ax.text(0.10, 0.97, seasons[sdx], verticalalignment='top', horizontalalignment='left',
                transform=ax.transAxes, color='black', fontsize=16)
        ax.text(0.97, 0.97, region, verticalalignment='top', horizontalalignment='right',
                transform=ax.transAxes, color='black', fontsize=16)
        ax.text(0.5, 0.97, "1915-2011", verticalalignment='top', horizontalalignment='center',
                transform=ax.transAxes, color='black', fontsize=16)
        # make the y-axis limits symmetric
        ax.set_ylim([-0.5,0.5])
        # plot a horizontal line at y=0
        plt.axhline(0, linewidth=2, color='black')
        idx += 1
    # write the plot to file
    plt.savefig('livneh_2013_anomaly_wind_{}.png'.format(season))
    sdx += 1

# <codecell>


