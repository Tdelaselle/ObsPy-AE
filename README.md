
# Welcome to the __ObsPy Acoustic Emission__ repository

<div>
Script for Converting Acoustic Emission Datastreaming to Obspy stream for signal processing, plotting and facilitate rapid application development.

<div>
  


## About

This script processes acoustic emission data stored in _txt_ or _tdms_ files and converts it into an ObsPy stream format, saved in mseed format or serialized with pickle. It uses command-line arguments to specify various parameters including data file paths, export formats, and sensor configurations.
    
From Obspy documentation: 
    
    "ObsPy is an open-source project dedicated to provide a Python framework for processing seismological data. 
    It provides [...] seismological signal processing routines which allow the manipulation of seismological time series 
    (see [Beyreuther2010], [Megies2011], [Krischer2015]). 
    The goal of the ObsPy project is to facilitate rapid application development for seismology."

As Acoustic emission datastreaming are analogous to seismograms and as there is no open access tools to recompose AE streaming, read, pre-processed (clean, filter, downsample, ...), plot and analyse it with signal processing classical methods, we develop this script to run  Obspy procedures and performed easily and rapidly these operations.    

This package was written and documented by [Théotime de la Selle](https://github.com/ThéotimedeLaSelle).

This work was supported by the __ANR project e-Warnings__.


## Dependencies

AE_Obspy requires the following python libraires: 
- argparse
- glob
- pickle
- numpy
- obspy
- tqdm

## Usage and example

 python3 AE_Obspy.py -data <data_directory> -save <save_directory> -f <export_format> -files <file_range> -d <start_date> -ch <channels> -sampling <sampling_rates> -sensors <sensors_references> -head <header_size> -col <number_of_columns>
  
    python3 AE_Obspy.py -data ./test_2ch/ -save ./ -f mseed -files 0 3 -d 2023-01-01T00:00:00.000 -ch 1 2 -sampling 2 5 -sensors nano30 micro200 -head 13 -col 1

## Arguments
-data, --datapath: str
Filepath to the directory containing data files. Default is an empty string.

-save, --savepath: str
Filepath to save the Obspy stream. Default is an empty string.

-f, --format: str
Format of the exported stream (either 'pkl' or 'mseed'). Default is 'mseed'

-files, --filesindex: tuple (first, last)
Indices of the first and last files to load. If not specified, all files are loaded.

-d, --date: str
Starting time of the stream in 'YYYY-MM-DDTHH:mm:ss.sss' format. Default is '1900-01-01T00:00:00.000'

-ch, --channels: list of int
List of channel numbers. Default is [1].

-sampling, --sampling: list of int
List of sampling frequencies (in MHz) for each channel. Default is [2].

-sensors, --sensors: list of str
List of sensor references for each channel. Default is ["-"].

-head, --header_size: int
Number of lines in the header of the TXT files. Default is 13.

-col, --columns: int
Number of columns in txt files (1 or 2). Default: 1
  


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
