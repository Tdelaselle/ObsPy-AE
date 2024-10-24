
# Welcome to the __ObsPy Acoustic Emission__ repository

<div>
Script for Converting Acoustic Emission Datastreaming to Obspy stream for signal processing, plotting and facilitate rapid application development.

<div>
  


## About

This script processes acoustic emission data stored in _txt_ or _tdms_ files and converts it into an ObsPy stream format, saved in mseed format or serialized with pickle. It uses command-line arguments to specify various parameters including data file paths, export formats, and sensor configurations.
    
From ObsPy documentation: 
    
    "ObsPy is an open-source project dedicated to provide a Python framework for processing seismological data. 
    It provides [...] seismological signal processing routines which allow the manipulation of seismological time series 
    (see [Beyreuther2010], [Megies2011], [Krischer2015]). 
    The goal of the ObsPy project is to facilitate rapid application development for seismology."

As Acoustic emission datastreaming are analogous to seismograms and as there is no open access tools to recompose AE streaming, read, pre-processed (clean, filter, downsample, ...), plot and analyse it with signal processing classical methods, we develop this script to run  Obspy procedures and performed easily and rapidly these operations.    

This package was written and documented by [Théotime de la Selle](https://github.com/ThéotimedeLaSelle). Any contributions are very welcomed.


This work was supported by the __ANR project e-Warnings__ (ANR-19-CE42-001).

> __Copyright ©️ 2024 Théotime de la Selle__
>
> This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
> This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
> You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

## Installation

Apart from depandencies (see scripts README), no installation is needed.

## Content description

This package provide 2 similar and independant scripts (supported with a respective README.m) dedicated to a different format of acoustic emission data : 

- AE_ASCII_Obspy.py for reading, stacking and converting _.txt_ files (see AE_ASCII_Obspy_README.m)
- AE_TDMS_Obspy.py for reading, stacking and converting _.tdms_ files (see AE_TDMS_Obspy_README.m)

We also provide a 2-channels AE datastreaming in ASCII format splitted in 3 _.txt_ files for testing.
