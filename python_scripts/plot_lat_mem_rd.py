# script to plot the latency chart given a pickled dataframe

import os
import sys
import subprocess
import datetime
import platform

import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FormatStrFormatter

import lat_mem_rd

def main():
    if len(sys.argv) != 3:
        print("Please specify the input file. ")
        sys.exit()

    path = sys.argv[1]
    size = sys.argv[2]
    result_dir = os.path.dirname(path) + "/"
    print(result_dir)
    try:
        df = pd.read_pickle(path)
        lat_mem_rd.plot(df, size, result_dir)
    except:
        print("Cannot open pickled file. Trying CSV. ")
        try:
            df = pd.read_csv(path)
            df = df.loc[:, 'Size':'512']
            lat_mem_rd.plot(df, size, result_dir)
        except:
            print("Cannot open csv file. ")
            sys.exit()

if __name__ == "__main__":
    main()
