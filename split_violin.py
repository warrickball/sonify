#!/usr/bin/env python3

# takes the Wikipedia violin sound and splits it into the four
# individual notes

import numpy as np
import soundfile as sf

data, rate = sf.read('G,_D,_A_and_E_on_violin.ogg')
gaps = [210000, 400000, 580000]
gaps.insert(0, 0)
gaps.append(len(data))

for i, note in enumerate(['G', 'D', 'A', 'E']):
    sf.write('%s_on_violin.ogg' % note, data[gaps[i]:gaps[i+1]], rate)
