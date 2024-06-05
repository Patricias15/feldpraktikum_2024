## Overview

Short explanation for the use of different python scripts regarding field exercise data analysis.

# Feldpraktikum SoSe 2019 - Turnau

## Table of Contents

* [Dependencies and Setup](#Dependencies-and-Setup)
* [Structure](#Structure)
* [Pressure reduction to MSL](#Pressure-reduction-to-MSL)
* [Data conversions](#Data-conversions)
* [Theodolite cuts](#Theodolite-cuts)
* [Google Earth kml files](#Google-Earth-kml-files)
* [Plotting routines](#Plotting-routines)



### Dependencies and Setup
**Some modules require Python 3!** Dependencies can be found in the **feldprakt_env.yml** file. Download the repository, move it to any path you wish for. You can either install all packages by hand, or you can use `
```sh
conda env create -f feldprakt_env.yml
```
inside the
```sh
/feldprakt/
```
folder for a one-step installation of all dependencies. When installed, a new environment named **feldprakt** is created, remember to activate the environment before executing any files.


### Structure

The general structure looks like:
```sh
/feldprakt/main_control.py
```
Control script for all working steps. If the underlying methods are only used and not modified, no other file has to be executed. The file itself is explained via comments inside.

```sh
/feldprakt/data/
```
Contains all different kinds of data, separated in subfolders. New data has to be sorted accordingly. Usually, new data consist of excel files only, hence move it to **/feldprakt/data/excel/**.

```sh
/feldprakt/python/
```
All python files which are used via the **main_control.py** file reside in this subfolder. Only modify them, if you want to change some functionality of the toolkit.

```sh
/feldprakt/figures/
```
Python generated plots are saved in this directory.

## Python scripts

### Pressure reduction to MSL

```sh
pressure_reduction_msl.py
```
Reduces the pressure to the mean sea level. Needs station observed pressure, temperature, dew-point temperature as well as station height and station latitude.
Can also be run on the command line via:
```sh
python pressure_reduction_msl.py PRESSURE TEMPERATURE DEW-POINT_TEMPERATURE STATION_HEIGHT STATION_LATITUDE
```

### Theodolite cuts

```sh
theo_single_cut.py
```
Single cut using data from one theodolite. To be able to calculate a vertical profile, the assumption of a constant vertical velocity (2.4 m/s) is made, which corresponds to a helium filled balloon with a circumference of about 1.6m.
A figure with two plots is created, the first visualizes the horizontal translation with color coded height, and the second one a vertical profile of wind velocity and direction.
Input: An excel file generated by the thedolite data processing software.


```sh
theo_double_cut.py
```
Double cut using data from two different theodolite observations of the same balloon. No assumption about the vertical velocity needs to be made, but the result is very sensitive to the accuracy of the measurements.
The generated figure is the same as in the single cut case.
Input: Two excel files (each from a different theodolite of the same balloon measurement) generated by the thedolite data processing software.

### Google Earth kml files
```sh
raso_to_kml.py
```
Downloads radio sounding data from the University of Wyoming server, calculates geographical location (longitude/latitude) for each data point available and writes the result into a kml file for the use with Google Earth (visualizing the trajectory).
Input: Station name, hour and date.
Can also be run on the command line via:
```sh
python raso_to_kml.py STATIONNAME HOUR YYYYMMDD
```


```sh
theo_to_kml.py
```
Same as above, but for theodolite measurements.
Input: An excel file generated by the thedolite data processing software.

### Plotting routines
```sh
plotting_routines.py
```
Different plotting settings can be targeted via the **plotroutine** variable. Available values are:
* 'hobo_single': Plots specified meteorological parameters as a time series plot for a single station.
* 'hobo_multi': Plots a comparison between 5 specified hobo stations for all variables.
* 'hobo_precip': Plots precipitation ticks, 1hourly and 3 hourly precipitation for a single station.
* 'syn_observation': Creates 2 figures. A time series plot containing thermodynamic at the top and dynamic parameter values of different measurement tools and synoptic observations such as cloudiness below and a bar plot encapsulating observed and approximated (spread formula) cloud base height.
* 'syn_forecast': Creates a figure containing 8 plots where forecasted parameters and validation values are displayed.
