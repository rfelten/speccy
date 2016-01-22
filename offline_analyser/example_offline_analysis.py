import cPickle
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from spectrum_file import SpectrumFileReader


def process(fn):
    f = open(fn, 'r')
    while True:
        try:
            ts, sample_data = cPickle.load(f)
            for tsf, freq, noise, rssi, sdata in SpectrumFileReader.decode(sample_data):
                print ts, tsf, freq, noise
        except EOFError:
            break


# open all .bin files and process content
def main():
    path_to_dumps = "../spectral_data"
    for fn in os.listdir(path_to_dumps):
        if fn.endswith(".bin"):
            process(path_to_dumps + os.path.sep + fn)

if __name__ == '__main__':
    main()
