#/usr/bin/python

from mpl_toolkits.basemap import Basemap, cm
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl

def get_data(infile,var_name,lat_name='Latitude',lon_name='Longitude'):
    nc = Dataset(infile,'r')
    lat = nc.variables[lat_name][:]
    lon = nc.variables[lon_name][:]
    var = nc.variables[var_name][:]
    nc.close()
    if var_name == 'SWE':
#        return (np.log10(var[0]),lat,lon)
	return (var[0],lat,lon)
    else:
        return (var[0],lat,lon)


def plot_basemap(source_dir,var_name,border,cmap,vmin,vmax):
    var,lat,lon = get_data(source_dir,var_name)
    latmi   = min(lat)-border
    latmx   = max(lat)+border
    latmean = (latmi+latmx)/2.
    lonmi   = min(lon)-border
    lonmx   = max(lon)+border
    lonmean = (lonmi+lonmx)/2.
    m = Basemap(projection = 'merc',lat_0=latmean, lon_0=lonmean, llcrnrlat=latmi,
            urcrnrlat=latmx, llcrnrlon=lonmi, urcrnrlon=lonmx, resolution='i')
    m.drawcoastlines(linewidth=0.25)
    xi,yi = m(*np.meshgrid(lon,lat))
    norm = mpl.colors.Normalize(vmin,vmax)
    m.pcolormesh(xi,yi,var,cmap=cmap,norm=norm)


def plot_colorbar(var,vmin,vmax,cax,cmap,tick_size,label_size,unit,orientation,extend):
    norm = mpl.colors.Normalize(vmin,vmax)
    cax = plt.axes(cax)
    cbar = mpl.colorbar.ColorbarBase(cax,cmap=cmap,norm=norm,orientation=orientation,extend=extend)
    cbar.ax.tick_params(labelsize=tick_size)
    cbar.set_label(var + unit, fontsize = label_size)


def cbar_extend(cbar_range,data_range):
    extend = None
    if cbar_range[0] == None:
        cbar_range[0] = data_range[0]
    if cbar_range[1] == None:
        cbar_range[1] == data_range[1]
    if data_range[0] < cbar_range[0]:
        extend = 'min'
    if data_range[1] > cbar_range[1]:
        if extend:
            extend = 'both'
        else:
            extend = 'max'
    if not extend:
        extend = 'neither'
    
    return extend


def cbar_unit(var):
    if var == 'SOIL_MOIST' or var == 'SWE':
        unit = ' (mm)'
    elif var == 'TMAX' or var == 'TMIN' or var == 'TAVG':
        unit = ' ($^\circ$C)'
    else:
        unit = ' (mm/day)'
    return unit


def get_vmin_vmax_seasonal(parent_dir,var,var_names,scenario,seasons):             
    var_name = var_names[var]
    cbar_min = []
    cbar_max = []
    for idx,season in enumerate(seasons):
        source_dir = parent_dir.format(scenario,var,season)
        nc = Dataset(source_dir,'r')
        data = nc.variables[var_name][0][:]
        cbar_min.append(np.min(data))
        cbar_max.append(np.max(data))
        nc.close()
    vmin = np.min(cbar_min)
    vmax = np.max(cbar_max)
    return (vmin,vmax)


def plot_figure_seasonal(parent_dir,store_dir,scenarios,variables,var_names,seasons,fig_size,nrow,ncol,height_ratio,width_ratio,\
                wspace,hspace,border,vmin,vmax,cbar_cax,cbar_tick_size,cbar_label_size,text_size,cmap,orientation):

    for scenario in scenarios:
        for var in variables:              
            store_dir0 = store_dir.format(var,scenario)
            fig = plt.figure(figsize=fig_size)
            grid = gridspec.GridSpec(nrow,ncol,height_ratios=height_ratio,width_ratios=width_ratio,\
                                     wspace=wspace,hspace=hspace)
            var_name = var_names[var]
            for idx,season in enumerate(seasons):
                ax = fig.add_subplot(grid[idx])
                source_dir = parent_dir.format(scenario,var,season)
                plot_basemap(source_dir,var_name,border,cmap,vmin,vmax)
                ax.text(0.97, 0.97, season, verticalalignment='top', horizontalalignment='right',
                    transform=ax.transAxes, color='black', fontsize=text_size)
            var_min,var_max = get_vmin_vmax_seasonal(parent_dir,var,var_names,scenario,seasons)
            print var_min,var_max
            extend = cbar_extend((vmin,vmax),(var_min,var_max))
            unit = cbar_unit(var)
            plot_colorbar(var,vmin,vmax,cbar_cax,cmap,cbar_tick_size,cbar_label_size,unit,orientation,extend)
            fig.savefig(store_dir0,dpi=300)


if __name__=="__main_":
	print "Only functions"
