# AE_TDMS_Obspy script

This script processes acoustic emission data stored in _.tdms_ files and converts it into an ObsPy stream format, saved in mseed format or serialized with pickle. It uses command-line arguments to specify various parameters including data file paths, export formats, and channels configurations.

## Dependencies

AE_TDMS_Obspy requires the following python libraires: 
 - argparse
- pickle
- numpy
- obspy
- tqdm
- nptdms

## Usage and example

    python AE_TDMS_Obspy.py -data <data_directory> -save <save_directory> -f <export_format> -d <start_date> -ch <channels> -n <output_name>
  
    python3 AE_TDMS_Obspy.py -data ./data/ -save ./output/ -f mseed -d 2023-01-01T00:00:00.000 -ch 1 2 -n Obspy_stream_TEST

## Arguments
 -data, --datapath: str
        Filepath to the directory containing data files. Default is an empty string.
    -save, --savepath: str
        Filepath to save the Obspy stream. Default is an empty string.
    -f, --format: str
        Format of the exported stream (either 'pkl' or 'mseed'). Default is 'mseed'.
    -d, --date: str
        Starting time of the stream in 'YYYY-MM-DDTHH:mm:ss.sss' format. Default is '1900-01-01T00:00:00.000'.
    -ch, --channels: list of int
        List of channel numbers. Default is [1].
    -n, --name: str
    	Resulting file name. Default: "current". Default is "current".


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
