import cPickle
import os
import matplotlib.pyplot as plt
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from spectrum_file import SpectrumFileReader

def show_tsf(path):
    result = []
    f = open(path, 'r')
    while True:
        try:
            ts, samples = cPickle.load(f)
            tsf_of_start_of_sample = -1  # reset tsf time base to start of sample
            for tsf, freq, noise, rssi, sdata in SpectrumFileReader.decode(samples):
                if tsf_of_start_of_sample == -1:
                    tsf_of_start_of_sample = tsf
                tsf_offset = tsf - tsf_of_start_of_sample
                #print ts, tsf, tsf_offset
                result.append(tsf_offset)
        except EOFError:
            break  # hit EOF
    f.close()
    return result


def show_kernel_time(path):
    result = []
    ts_start = -1
    f = open(path, 'r')
    while True:
        try:
            ts, samples = cPickle.load(f)
            if ts_start == -1:
                ts_start = ts
            ts_offset = ts - ts_start
            ts_offset = (ts_offset.seconds * 1000000) + ts_offset.microseconds  # convert to us
            #print ts_start, ts_offset
            result.append(ts_offset)
        except EOFError:
            break  # hit EOF
    f.close()
    return result


# helper for to plot
def cnt_files_in_dir(path):
    cnt = 0
    for filename in os.listdir(path):
        if filename.endswith(".bin"):
            cnt += 1
    return cnt

# open all .bin files in subdir and process them. Create one subplot per file to compare measurements
def main():
    path_to_dumps = "../spectral_data"
    dataset_index = 0
    plt.figure(0)
    plots = cnt_files_in_dir(path_to_dumps)
    for filename in os.listdir(path_to_dumps):
        if filename.endswith(".bin"):
            print "process file: %s" % filename
            filepath = path_to_dumps + os.path.sep + filename
            # tsf
            x_vals = show_tsf(filepath)
            plt.subplot2grid((2, plots), (0, dataset_index))
            plt.title(filename)
            plt.xlabel("samples")
            plt.ylabel("tsf in samples [us]")
            plt.plot(x_vals)

            x_vals = show_kernel_time(filepath)
            plt.subplot2grid((2, plots), (1, dataset_index))
            plt.title(filename)
            plt.xlabel("samples")
            plt.ylabel("time of samples [us]")
            plt.plot(x_vals)

            dataset_index += 1

    plt.show()

if __name__ == '__main__':
    main()
