#!/usr/bin/env python3


import numpy as np
import soundfile as sf
from argparse import ArgumentParser

parser = ArgumentParser(description=
"Creates red, pink and white noise files.")
parser.add_argument('-T', type=float, default=10.0,
                    help="desired length of sound files, in seconds "
                    "(default=10.0)")
parser.add_argument('--rate', type=float, default=44100,
                    help="integer sampling rate, in Hz (default=44100)")
args = parser.parse_args()

f = np.linspace(0., args.rate//2, int(args.T*args.rate//2)+1)

colours = ['white', 'pink', 'red']

for i, colour in enumerate(colours):
    # don't bother putting much power where we can't hear it (~< 20 Hz)
    p = np.hstack((np.zeros(100), 1/f[100:]**i))
    a = np.sqrt(p)*np.exp(2j*np.pi*np.random.rand(len(p)))

    x = np.fft.irfft(a)
    x = x/np.max(np.abs(x))
    x = np.vstack((x, np.roll(x, 1))).T
    sf.write('%s_noise.ogg' % colour, x, args.rate)
