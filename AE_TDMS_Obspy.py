"""
Script for Converting Acoustic Emission Datastreaming (TDMS) to Obspy Stream saved in MSEED format or serialized with pickle.

Description:
    This script processes acoustic emission data stored in TDMS files and converts it into an Obspy stream format (either PKL or MSEED). It uses command-line arguments to specify various parameters including data file paths, export formats, and sensor configurations.
    From Obspy documentation: 
    "ObsPy is an open-source project dedicated to provide a Python framework for processing seismological data. It provides [...] seismological signal processing routines which allow the manipulation of seismological time series (see [Beyreuther2010], [Megies2011], [Krischer2015]). The goal of the ObsPy project is to facilitate rapid application development for seismology."

    As Acoustic emission datastreaming are analogous to seismograms and as there is no open access tools to recompose AE streaming, read, pre-processed (clean, filter, downsample, ...), plot and analyse it with signal processing classical methods, we develop this script to run  Obspy procedures and performed easily and rapidly these operations.    


Dependencies:
    - argparse
    - pickle
    - numpy
    - obspy
    - tqdm
    - nptdms

Usage:
    python AE_Obspy.py -data <data_directory> -save <save_directory> -f <export_format> -files <file_range> -d <start_date> -ch <channels> -sampling <sampling_rates> -sensors <sensors_references> -head <header_size> -col <number_of_columns>

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
        

Example:
    python3 AE_Obspy.py -data ./data/ -save ./output/ -f mseed -files 0 5 -d 2023-01-01T00:00:00.000 -ch 1 2 -sampling 2 5 -sensors nano30 micro200 -head 13 -col 1

    python3 AE_Obspy.py -data ./Raw_data/C6C7SD_5083_2.3_S1/ -save ./data/ -f pkl -files 0 5 -d 2023-01-01T00:00:00.000 -ch 2 -sampling 2 -sensors nano30 -head 13 -col 1 -n C6C7SD_5083_2.3_S1_ch2 


    Made by Théotime de la Selle in August 2024.
"""

import argparse
import pickle
import os

import numpy as np
import obspy
import nptdms

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
    "-ch",
    "--channels",
    nargs='+',
    help='List of integers containing each channel number (ex: 1 2 3). Default: [1]',
    type=int,
    default=[1],
)
parser.add_argument(
    "-f",
    "--format",
    help="format of exported stream (pkl or mseed). Default: mseed.",
    type=str,
    default="mseed",
)
parser.add_argument(
    "-d",
    "--date",
    help="Starting time of the stream. Follow format: 'YYYY-MM-DDTHH:mm:ss.sss'",
    type=str,
    default="1900-01-01T00:00:00.000",
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

def load_tdms_into_stream(
    dirpath, starttime,channels
):    
    
    print(f"Loading data of ",dirpath)

    # Create Obspy stream
    stream = obspy.core.Stream()
    
    # Collect data, information and add Trace to stream for each channel
    with nptdms.TdmsFile.open(dirpath) as tdms_file:
        group_name = "Transient"
        for ch in channels:
            channel_name = "Ch"+str(ch)
            channel = tdms_file[group_name][channel_name]
            data = channel[:]
            times = channel.time_track()
        
            sampling = 1/(times[1]-times[0])
            
            header = {
                "sampling_rate": sampling,
                "npts": len(data),
                "starttime": starttime,
                "delta": 1.0 / sampling,
                "network": "AE_stream",
                "station": "Galling",
                "location": "",
                "channel": channel_name,
            }
            
            stream.append(obspy.Trace(data=data, header=header))

    return stream

# Loop over all channels to add traces in stream
stream = load_tdms_into_stream(ARGUMENTS.datapath,obspy.UTCDateTime(ARGUMENTS.date),ARGUMENTS.channels)

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
