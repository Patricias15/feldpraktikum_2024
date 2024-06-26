# -*- coding: utf-8 -*-
#
# Python Template
# @Author: SebiMac
# @Date:   2019-03-21 12:51:44 +0100
# @Last modified by:   SebiMac
# @Last modified time: 2019-06-01 00:44:32 +0200

"""
Calculation and plot of a theodolite double cut profile.
"""

import numpy as np
import os
import errno
import pandas as pd
import sys
import matplotlib.pyplot as plt

def main(B=None, phi=None, excel_file1=None, excel_file2=None, titlestr='theodolite example double cut'):
    dt = 10

    # read data from excel file 1
    df1 = pd.read_excel(os.path.join('data', 'excel', excel_file1),
                       usecols=[3, 4], sheet_name='Data')
    df2 = pd.read_excel(os.path.join('data', 'excel', excel_file2),
                       usecols=[3, 4], sheet_name='Data')

    # get important data
    elevation1 = np.array(df1['Unnamed: 3'].values[4:], dtype=float)
    azimuth1 = np.array(df1['Unnamed: 4'].values[4:], dtype=float)
    elevation2 = np.array(df2['Unnamed: 3'].values[4:], dtype=float)
    azimuth2 = np.array(df2['Unnamed: 4'].values[4:], dtype=float)

    # equalise length and convert to radian
    min_length = np.min([len(elevation1), len(elevation2)])
    ele1 = elevation1[:min_length]*np.pi/180
    azi1 = azimuth1[:min_length]*np.pi/180
    ele2 = elevation2[:min_length]*np.pi/180
    azi2 = azimuth2[:min_length]*np.pi/180
    phi = phi*np.pi/180

    s1 = 2*np.pi - azi1 + phi
    s2 = azi2 - (phi + np.pi)
    alpha = azi1 - azi2
    he1 = B/np.sin(alpha) * np.sin(s2)
    he2 = B/np.sin(alpha) * np.sin(s1)

    h1 = he1 * np.tan(ele1)
    h2 = he2 * np.tan(ele2)

    x = he1*np.sin(azi1)
    y = he1*np.cos(azi1)

    #x = he2*np.sin(azi2)# + B*np.sin(phi)
    #y = he2*np.cos(azi2)# + B*np.cos(phi)

    # average height from both solutions
    z = (h1 + h2)/2.

    r = np.column_stack((x, y))
    r_delta = np.diff(r, axis=0)
    v_spd = np.sqrt(r_delta[:,0]**2 + r_delta[:,1]**2)/dt
    v_dir = np.arctan2(r_delta[:,1], r_delta[:,0])*180/np.pi
    v_dir = (270-v_dir) % 360
    # plot
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(14, 6))
    plt.suptitle(titlestr)

    # horizontal translation
    x_cs = np.cumsum(r_delta[:,0])
    y_cs = np.cumsum(r_delta[:,1])

    ax1.plot(x_cs[0], y_cs[0], 'x', color='b', markersize=20)
    ax1.plot(x_cs[-1], y_cs[-1], 'x', color='r', markersize=20)
    ax1.plot(x_cs, y_cs, '--', color='k', linewidth=0.7, alpha=0.7)
    p = ax1.scatter(x_cs, y_cs, c=z[1:], cmap='rainbow')
    plt.colorbar(p, ax=ax1, label='height above ground [m]')

    # set visuals
    dy = np.nanmax(y_cs) - np.nanmin(y_cs)
    dx = np.nanmax(x_cs) - np.nanmin(x_cs)
    ds = dx - dy
    if ds > 0:
        ax1.set_xlim([np.nanmin(x_cs)-100, np.nanmax(x_cs)+100])
        ax1.set_ylim([np.nanmin(y_cs)-ds/2., np.nanmax(y_cs)+ds/2.])
    elif ds < 0:
        ax1.set_xlim([np.nanmin(x_cs)-np.abs(ds)/2., np.nanmax(x_cs)+np.abs(ds)/2.])
        ax1.set_ylim([np.nanmin(y_cs)-100., np.nanmax(y_cs)+100])
    # ax1.set_aspect(aspect=1) # can be used to reduce the whole box to the corret aspect ratio
    ax1.set_title('horizontal translation (blue cross = starting point)')
    ax1.set_xlabel('x [m]')
    ax1.set_ylabel('y [m]')
    ax1.grid(True)

    # vertical plot
    wv = ax2.plot(v_spd[1:], z[1:-1], label='wind velocity')
    ax22 = ax2.twiny()
    wd = ax22.plot(v_dir[1:], z[1:-1], 'r*', label='wind direction')
    ax22.set_xticks(np.arange(0,361,45))
    ax22.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N'])

    ax2.set_xlabel('wind velocity [m/s]')
    ax2.set_ylabel('height above ground [m]')
    ax22.set_xlabel('wind direction [°]')
    lns = wv+wd
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs)
    ax2.grid(True)

    # create figure directory
    fig_dir = 'figures'
    try:
        os.makedirs(fig_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # save figure
    print('Saving figure ...')
    plt.savefig(os.path.join(fig_dir, "".join([excel_file1.split('.')[0], '_double_cut.png'])))
    return None


if __name__ == '__main__':
    B = sys.argv[1]
    phi = sys.argv[2]
    data1 = sys.argv[3]
    data2 = sys.argv[4]
    tstr = sys.argv[5]

    main(B=B, phi=phi, excel_file1=data1, excel_file2=data2, titlestr=tstr)
