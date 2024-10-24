"""
Script for Converting Acoustic Emission Datastreaming (TXT) to Obspy Stream saved in MSEED format or serialized with pickle.

Description:
    This script processes acoustic emission data stored in TXT files and converts it into an Obspy stream format (either PKL or MSEED). It uses command-line arguments to specify various parameters including data file paths, export formats, and sensor configurations.
    From Obspy documentation: 
    "ObsPy is an open-source project dedicated to provide a Python framework for processing seismological data. It provides [...] seismological signal processing routines which allow the manipulation of seismological time series (see [Beyreuther2010], [Megies2011], [Krischer2015]). The goal of the ObsPy project is to facilitate rapid application development for seismology."

    As Acoustic emission datastreaming are analogous to seismograms and as there is no open access tools to recompose AE streaming, read, pre-processed (clean, filter, downsample, ...), plot and analyse it with signal processing classical methods, we develop this script to run  Obspy procedures and performed easily and rapidly these operations.    


Dependencies:
    - argparse
    - glob
    - pickle
    - numpy
    - obspy
    - tqdm

Usage:
    python AE_ASCII_Obspy.py -data <data_directory> -save <save_directory> -f <export_format> -files <file_range> -d <start_date> -ch <channels> -sampling <sampling_rates> -sensors <sensors_references> -head <header_size> -col <number_of_columns> -n <output_name>

Arguments:
    -data, --datapath: str
        Filepath to the directory containing data files. Default is an empty string.
    -save, --savepath: str
        Filepath to save the Obspy stream. Default is an empty string.
    -f, --format: str
        Format of the exported stream (either 'pkl' or 'mseed'). Default is 'mseed'.
    -files, --filesindex: tuple (first, last)
        Indices of the first and last files to load. If not specified, all files are loaded.
    -d, --date: str
        Starting time of the stream in 'YYYY-MM-DDTHH:mm:ss.sss' format. Default is '1900-01-01T00:00:00.000'.
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
    -n, --name: str
    	Resulting file name. Default: "current".
        

Examples:
    python3 AE_ASCII_Obspy.py -data ./data/ -save ./output/ -f mseed -files 0 5 -d 2023-01-01T00:00:00.000 -ch 1 2 -sampling 2 5 -sensors nano30 micro200 -head 13 -col 1 -n Obspy_stream

    python3 AE_ASCII_Obspy.py -data ./test_2ch/ -save ./ -f mseed -files 0 3 -d 2023-01-01T00:00:00.000 -ch 1 2 -sampling 2 5 -sensors nano30 micro200 -head 13 -col 1 -n test_ch2_Obspy


    Made by Théotime de la Selle in August 2024.
"""

import argparse
import glob
import pickle
import os

import numpy as np
import obspy
import tqdm

# Argument parser
parser = argparse.ArgumentParser(
    description="Convert acoustic emission datastreaming (txt) to Obspy stream (pkl or mseed)"
)
parser.add_argument(
    "-data",
    "--datapath",
    help="Filepath to directory containing data files",
    type=str,
    default="",
)
parser.add_argument(
    "-save",
    "--savepath",
    help="filepath to save the obspy stream.",
    type=str,
    default="",
)
parser.add_argument(
    "-f",
    "--format",
    help="format of exported stream (pkl or mseed). Default: mseed.",
    type=str,
    default="mseed",
)
parser.add_argument(
    "-files",
    "--filesindex",
    nargs='+',
    help="First and last files to load (ex: 0 10). No value: all files are loaded.",
    type=int,
    default=(0,0),
)
parser.add_argument(
    "-d",
    "--date",
    help="Starting time of the stream. Follow format: 'YYYY-MM-DDTHH:mm:ss.sss'",
    type=str,
    default="1900-01-01T00:00:00.000",
)
parser.add_argument(
    "-ch",
    "--channels",
    nargs='+',
    help='List of integers containing each channel number (ex: 1 2 3). Default: [1]',
    type=int,
    default=[1],
)
parser.add_argument(
    "-sampling",
    "--sampling",
    nargs='+',
    help='List of integers containing sampling frequencies (MHz) for each channel (ex: 2 5 2). Default: 2',
    type=int,
    default=[2],
)
parser.add_argument(
    "-sensors",
    "--sensors",
    nargs='+',
    help='List of strings containing sensors references for each channel (ex: nano30 micro200). Default: -',
    type=str,
    default=["-"]
)
parser.add_argument(
    "-head",
    "--header_size",
    help='Number of lines in header of txt files. Default: 13',
    type=int,
    default=13,
)
parser.add_argument(
    "-col",
    "--columns",
    help='Number of columns in txt files (1 or 2). Default: 1',
    type=int,
    default=1,
)
parser.add_argument(
    "-n",
    "--name",
    help='Resulting file name. Default: "current"',
    type=str,
    default="current",
)

# Parse arguments
ARGUMENTS = parser.parse_args()

def load_txt_into_stream(
    dirpath, stream, sampling_rate, Channel, starttime, sensor
):    
    
    print(f"Loading data of channel",Channel)

    # Get list of files
    # ------- /!\ Datastreaming files must have their channel number specified in their names through the form "_N_" (anywhere in the file name)
    filepaths = list(filter(os.path.isfile, glob.glob(dirpath + "*" + "_" + Channel + "_*")))
    filepaths.sort(key=lambda x: os.path.getmtime(x))
    if ARGUMENTS.filesindex[0] != ARGUMENTS.filesindex[1] :
        filepaths = filepaths[ARGUMENTS.filesindex[0]:ARGUMENTS.filesindex[1]]
          
    # Collect data
    data = list()
    for filepath in tqdm.tqdm(filepaths):
        if ARGUMENTS.columns == 1:
            # /!\ Encoding may need to be changed ('latin-1' if accents in files, even in the header) 
            data.append(np.loadtxt(filepath, skiprows=ARGUMENTS.header_size,encoding='latin-1'))  # for 1 column files 
        else :  
            data.append(np.loadtxt(filepath, delimiter=',', usecols=(1), skiprows=ARGUMENTS.header_size))    # for 2 columns files

    # Get numpy array
    data = np.hstack(data)
    n_samples = data.shape[0]

    # Obspy stream header definition
    header = {
        "sampling_rate": sampling_rate,
        "npts": n_samples,
        "starttime": starttime,
        "delta": 1.0 / sampling_rate,
        "network": "AE",
        "station": "streaming",
        "location": sensor,
        "channel": Channel,
    }

    stream.append(obspy.Trace(data=data, header=header))

    return stream

# Loop over all channels to add traces in stream
stream = obspy.Stream()
for i in range (len(ARGUMENTS.channels)):
    stream = load_txt_into_stream(ARGUMENTS.datapath,stream,ARGUMENTS.sampling[i]*1e6,str(ARGUMENTS.channels[i]),obspy.UTCDateTime(ARGUMENTS.date),ARGUMENTS.sensors[i])

# Control stream 
print(stream)
stream.plot(rasterized=True) # if needed ; could be long

"""
Saving procedures
"""
filepath = ARGUMENTS.savepath+"Stream_"+ARGUMENTS.name

if ARGUMENTS.format == "pkl":
    # Save obspy stream (serialized with pickle)
    with open(filepath+".pkl", "wb") as file:
        pickle.dump(stream, file, protocol=pickle.HIGHEST_PROTOCOL)
else :
    # Save obspy stream (mseed)
    stream.write(filepath+".mseed", format="MSEED")
    
print(f"Stream saved in format",ARGUMENTS.format)
