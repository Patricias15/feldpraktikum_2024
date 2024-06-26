# -*- coding: utf-8 -*-
#
# Python Template
# @Author: SebiMac
# @Date:   2019-03-21 12:54:43 +0100
# @Last modified by:   Patricia
# @Last modified time: 2024-06-04
"""
Control script for the use of field exercise data tools.
Can be used to play around with the included test data or modified to use other data.
"""
from datetime import datetime
import sys

import python.pressure_reduction_msl as presreduc
import python.raso_to_kml as rasokml
import python.theo_to_kml as theokml
import python.theo_single_cut as thsin
import python.theo_double_cut as thdou
import python.plotting_routines as plotrout
from python.lineplot_klima import new_obs_plot

# 0 = ignore; 1 = execute
workflow_dict = {'pressure_reduction':           0,
                 'theo_calc_single_cut':         0,
                 'theo_calc_double_cut':         1,
                 'raso_to_kml':                  0,
                 'theo_to_kml':                  1,
                 'hobo_single_station':          0,
                 'hobo_compare_stations':        0,
                 'hobo_single_station_precip':   0,
                 'timeseries_syn_observations':  0,
                 'timeseries_syn_forecast':      0}


""" pressure reduction to mean sea level """
if workflow_dict['pressure_reduction'] == 1:
    # specify the variables below, result gets printed
    pressure = 1000.15
    temp = 15
    temp_dew = 10
    h = 200
    latitude = 48
    presreduc.main(p=pressure, T=temp, Td=temp_dew, station_height=h, lat=latitude)


""" Theodolite cuts calculations """
# theodolite single cut
if workflow_dict['theo_calc_single_cut'] == 1:
    # input args
    filename = 'theo2_double_12UTC.xlsx'
    titlestr_for_plot = 'theodolite 2 2024-06-02 12UTC double cut'
    thsin.main(excel_file=filename, titlestr=titlestr_for_plot)

# theodolite double cut
if workflow_dict['theo_calc_double_cut'] == 1:
    # input args
    B = 267 # distance between the two theodolites
    phi = 359.8 # angle between the north and the thedolite connecting line
    excel_file1 = 'theo1_6utc.xlsx' #4138 SN
    excel_file2 = 'theo2_6utc.xlsx'
    titlestr_for_plot='Theodolite double cut 2024-06-05 6UTC'
    thdou.main(B=B, phi=phi, excel_file1=excel_file1, excel_file2=excel_file2, titlestr=titlestr_for_plot)

    thsin.main(excel_file=excel_file1, titlestr='Theodolit single cut (Theo 1) 2024-06-05 06UTC')
    thsin.main(excel_file=excel_file2, titlestr='Theodolit single cut (Theo 2) 2024-06-05 06UTC')


""" Radiosounding to kml file """
# download radiosounding data and create a kml file for google earth
if workflow_dict['raso_to_kml'] == 1:
    # datestr = datetime.now().strftime('%Y%m%d')
    datestr = '20240602'
    rasokml.main(station_name='wien', hour='00', date=datestr)
    rasokml.main(station_name='linz', hour='02', date=datestr)
    rasokml.main(station_name='innsbruck', hour='00', date=datestr)
    rasokml.main(station_name='muenchen', hour='00', date=datestr)
    rasokml.main(station_name='udine', hour='00', date=datestr)
    rasokml.main(station_name='zagreb', hour='00', date=datestr)
    rasokml.main(station_name='ljubljana', hour='06', date=datestr)
    rasokml.main(station_name='graz', hour='02', date=datestr)
    rasokml.main(station_name='wien', hour='00', date=datestr)


""" Theodolite to kml file """
if workflow_dict['theo_to_kml'] and workflow_dict['theo_calc_single_cut'] ==1:
    h = 785
    lon = 15.3175
    lat = 47.5553
    #excel_file = 'theo_single_03UTC.xlsx'
    excel_file = 'theo2_double_06UTC.xlsx'
    theokml.main(stat_height=h, stat_lon=lon, stat_lat=lat, excel_file=excel_file)

if workflow_dict['theo_to_kml'] == 1 and workflow_dict['theo_calc_double_cut'] ==1:
    h = 785
    lon = 15.3175
    lat = 47.5553
    excel_file = 'theo1_6utc.xlsx'
    theokml.main(stat_height=h, stat_lon=lon, stat_lat=lat, excel_file=excel_file)
    excel_file = 'theo2_6utc.xlsx'
    theokml.main(stat_height=h, stat_lon=lon, stat_lat=lat, excel_file=excel_file)


""" Plotting routines """
# timeseries plot for various parameters
if workflow_dict['hobo_single_station'] == 1:
    # creates a single windowed timeseries plot for specified vars
    plotroutine = 'hobo_single'
    excel_filename = 'hobo_lanzenkreuz.xlsx'

    var_dict = {'wind_spd':     1,
                'wind_gusts':   1,
                'wind_dir':     1,
                'temp':         1,
                'rel_hum':      1,
                'pres':         1,
                'radiation':    0}

    titlestr_for_plot = 'hobo example plot'
    figname = 'hobo_exampleplot.png'
    plotrout.main(plotroutine=plotroutine, excel_filename=excel_filename, var_dict=var_dict, titlestr=titlestr_for_plot, figurename=figname)


# compare multiple time series of the same parameter
if workflow_dict['hobo_compare_stations'] == 1:
    # csv dict: first entry: name; second entry: filename
    plotroutine = 'hobo_multi'
    excel_filenames = {'Campingplatz': 'hobo_campingplatz.xlsx',
                     'Lanzenkreuz': 'hobo_lanzenkreuz.xlsx',
                     'Seetal': 'hobo_seetal.xlsx',
                     'Stübming': 'hobo_stuebming.xlsx',
                     'UnterDerLanzen': 'hobo_unterderlanzen_fake_testdata.xlsx'}
    # if wind gusts and/or pressure is plotted
    flag = {'wind_gusts': 1,
            'pressure':   1}

    titlestr_for_plot = 'hobo compare example plot'
    figname = 'hobo_compare_'
    plotrout.main(plotroutine=plotroutine, excel_filename=excel_filenames, titlestr=titlestr_for_plot, figurename=figname, flag=flag)

# timeseries plot for hobo precipitation
if workflow_dict['hobo_single_station_precip'] == 1:
    plotroutine = 'hobo_precip'
    excel_filename = 'hobo_precip.xls'
    figname = 'hobo_example'
    timebegin = '2018082410'
    timeend = '2018082612'
    titlestr_for_plot = 'hobo example observed precipitation'
    plotrout.main(plotroutine=plotroutine, excel_filename=excel_filename, titlestr=titlestr_for_plot, figurename=figname, timebegin=timebegin, timeend=timeend, hour_interval=3, time_freq='3H')



# timeseries plot for synoptic observations (such as cloudiness)
if workflow_dict['timeseries_syn_observations'] == 1:
    plotroutine='syn_observation'
    excel_filename = 'syn_obs_20240604.xlsx'
    figname = 'syn_obs_20240604'
    title = 'synoptic observations 2024-06-04'
    plotrout.main(plotroutine=plotroutine, excel_filename=excel_filename, figurename=figname, titlestr=title)
    new_obs_plot(excel_filename)

# timeseries plot for synoptic forecast
if workflow_dict['timeseries_syn_forecast'] == 1:
    plotroutine='syn_forecast'
    excel_filename = 'syn_forecast_validation_example.xlsx'
    figname = 'syn_forecast_validation_example'
    title = 'synoptic forecast and validation example'
    timebegin = '2019051908'
    timeend = '2019052016'
    timemarker = '2019051915'
    plotrout.main(plotroutine=plotroutine, excel_filename=excel_filename, figurename=figname, titlestr=title, timebegin=timebegin, timeend=timeend, timemarker=timemarker)

    