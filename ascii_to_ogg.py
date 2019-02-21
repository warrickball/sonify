#!/usr/bin/env python3

import numpy as np
import soundfile as sf
from argparse import ArgumentParser

parser = ArgumentParser(description=
"""Converts input ASCII file, with one number per row, into an Ogg
Vorbis sound file.  Suitable for use with AADG3 timeseries.""")
parser.add_argument('asc', type=str,
                    help="name of input ASCII file")
parser.add_argument('ogg', type=str,
                    help="name of output OGG sound file")
parser.add_argument('--rate', type=int, default=44100,
                    help="sampling rate in Hz (default=44100)")
args = parser.parse_args()

x = np.loadtxt(args.asc)
x = x/np.max(np.abs(x))
sf.write(args.ogg, x, args.rate)
