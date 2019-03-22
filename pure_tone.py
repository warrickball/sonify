#!/usr/bin/env python3

import numpy as np
import soundfile as sf
from argparse import ArgumentParser

parser = ArgumentParser(description=
"""Saves a sound file corresponding to a 
pure sine wave at a given frequency.""")
parser.add_argument('frequency', type=float,
                    help="frequency for pure sine wave (in Hz)")
parser.add_argument('filename', type=str,
                    help="filename for output sound file")
parser.add_argument('--rate', type=int, default=44100,
                    help="sampling rate in Hz (default=44100)")
parser.add_argument('-t', type=float, default=10.0,
                    help="duration of sound file in seconds (default=10)")
args = parser.parse_args()

t = 2.*np.pi*np.arange(0., args.t, 1.0/args.rate)
sf.write(args.filename, 0.999*np.sin(args.frequency*t), args.rate)
