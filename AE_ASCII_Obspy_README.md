
# AE_ASCII_Obspy script

This script processes acoustic emission data stored in _.txt_ files and converts it into an ObsPy stream format, saved in mseed format or serialized with pickle. It uses command-line arguments to specify various parameters including data file paths, export formats, and sensor configurations.

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
