#/usr/bin/python

### following are functions used in plotting SWE for three situations 

from mpl_toolkits.basemap import Basemap, cm
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
from functions_common import get_data,plot_basemap,cbar_extend,plot_colorbar,get_var_name,cbar_unit

### calculate vmin and vmax of data
def get_vmin_vmax_SWE(var,scenarios,source_dir):
    cbar_min=[]
    cbar_max=[]
    for i,scenario in enumerate(scenarios):
        nc = Dataset(source_dir.format(scenario,var), 'r')
        var_name = get_var_name(var)
        info = nc.variables[var_name]
        data = info[0]
        cbar_min.append(np.min(data))
        cbar_max.append(np.max(data))
    vmin=np.min(cbar_min)
    vmax=np.max(cbar_max)
    return (vmin,vmax)

### plot SWE of historical, rcp45, rcp85 on one figure
def plot_figure_SWE(source_dir,variables,scenarios,fig_size,border,cmap,orientation,cbar_tick_size,cbar_label_size,\
                    vmin,vmax,text_size,cax,extend,store_dir):
    grid = gridspec.GridSpec(1, 3, width_ratios=[1,1,1])
    fig = plt.figure(figsize=fig_size)
    for var in variables:
        for idx,scenario in enumerate(scenarios):
            ifile=source_dir.format(scenario,var)
            ax = fig.add_subplot(grid[idx])
            var_name=get_var_name(var)
            plot_basemap(ifile,var_name,border,cmap,vmin,vmax)
            ax.text(0.97, 0.97, scenario, verticalalignment='top', horizontalalignment='right',
                        transform=ax.transAxes, color='black', fontsize=text_size)
        cax = plt.axes(cax)
        var_min,var_max = get_vmin_vmax_SWE(var,scenarios,source_dir)
        extend = cbar_extend((vmin,vmax),(var_min,var_max))
        unit = cbar_unit(var)
        plot_colorbar(' ',vmin,vmax,cax,cmap,cbar_tick_size,cbar_label_size,unit,orientation,extend)
        fig.savefig(store_dir.format(var))
