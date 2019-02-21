#!/usr/bin/env python3

import numpy as np
import soundfile as sf
import AADG3
from math import factorial
from scipy.special import lpmn
from argparse import ArgumentParser

parser = ArgumentParser(description=
"""Reads an AADG3 input file and writes a sound file containing a
realisation of the power spectrum but with pure sine waves with random
but constant phases.  I mainly use this to cross-check that the AADG3
timeseries sounds right.""")
parser.add_argument('filename', type=str,
                    help="name of input AADG3 input file")
parser.add_argument('ogg', type=str,
                    help="name of output OGG sound file")
parser.add_argument('--rate', type=int, default=44100,
                    help="sampling rate in Hz (default=44100)")
parser.add_argument('--N', type=int, default=None,
                    help="number of samples (default=n_cadences from "
                    "AADG3 input file)")
args = parser.parse_args()

TAU = 2.*np.pi

nml, modes, rot = AADG3.load_all_input(args.filename)
mu = np.cos(np.radians(nml['inclination']))
lmax = max(modes['l'])
E = np.array(lpmn(lmax, lmax, mu)[0].T)
for l in range(lmax+1):
    for m in range(l+1):
        E[l][m] = E[l][m]**2*factorial(l-m)/factorial(l+m)

N = args.N if args.N else nml['n_cadences']
x = np.zeros(N)
t = np.arange(N)*nml['cadence']

for row in modes:
    l = row['l']
    # height = 2.*row['power']/np.pi/row['width']*nml['p(%i)' % l]
    height = row['power']*nml['p(%i)' % l]
    freq = row['freq']/1e6  # uHz -> Hz
    x += height*E[l][0]*np.sin(TAU*(freq*t + np.random.rand()))

    for m in range(1, l+1):
        split = rot[(rot['l']==l)
                    &(rot['m']==m)
                    &(rot['n']==row['n'])]['splitting']/1e6
        if len(split) > 1:
            split = split[0]

        x += height*E[l][m]*(
            np.sin(TAU*((freq + m*split)*t + np.random.rand())) +
            np.sin(TAU*((freq - m*split)*t + np.random.rand())))

x = x/np.max(np.abs(x))
sf.write(args.ogg, x, args.rate)
