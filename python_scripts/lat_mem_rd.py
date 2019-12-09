# script to run lat_mem_rd and generate line charts
# Run this in the root directory of lmbench
# It assumes that the benchmark binaries are in the root/build/bin directory

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

bm_name = "lat_mem_rd"

result_dir = "/results/lat_mem_rd/"
bm_bin_dir = "/build/bin/"
memory_size_default_str = "512M"
stride_default_str = "128"

stride_strs = ["64", "128", "256", "512"]

base_command = [bm_name, "-N", "1", "-P", "1",
                memory_size_default_str, stride_default_str]

linux_command_prefix = ["taskset", "0x1"]

def run_one_bm(command):
    res = subprocess.run(command, stderr=subprocess.PIPE)
    result_text_array = res.stderr.decode('utf-8').splitlines()[1:-1]
    return result_text_array

def split_result_array(result_text_array):
    # assumes the element of the results array is of the format
    # %.5f %.3f
    # note the space in between the two floats
    val1 = [float(i.split(' ')[0]) for i in result_text_array]
    val2 = [float(i.split(' ')[1]) for i in result_text_array]
    return val1, val2

def plot(df, mem_size, result_dir):
    fig1, ax1 = plt.subplots()
    for column in df.drop('Size', axis=1):
        ax1.plot(df['Size'], df[column], marker='', \
                 linewidth=1, alpha=0.9, label=column)
    ax1.set_xscale("log", basex=2)
    ax1.get_xaxis().set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.3f'))
    plt.legend(title="Stride")
    plt.xlabel('Array Size in MB', fontsize=18)
    plt.ylabel('Latency in ns', fontsize=18)
    result_graph_name = result_dir + 'lat_mem_rd_{0}.png'.format(mem_size)
    plt.savefig(result_graph_name)

def run_bm(command, result_dir):
    # If there is an existing run
    df_pk_name = result_dir + 'lat_mem_rd_{0}.pkl'.format(command[-2])
    try:
        df = pd.read_pickle(df_pk_name)
        plot(df, command[-2], result_dir)
        return
    except:
        #rerun experiments
        df = pd.DataFrame()
        for s in stride_strs:
            print("Running stride %s" %(s))
            command[-1] = s
            res = run_one_bm(command)
            size, time = split_result_array(res)
            if df.empty:
                df["Size"] = size
            df[s] = time
        df.to_pickle(df_pk_name)
        plot(df, command[-2], result_dir)

def main():
    print("Running %s on OS %s" % (bm_name, platform.system()))
    curr_dir = os.getcwd()

    # Build dir for the results
    result_abs_path = curr_dir + result_dir
    if not os.path.exists(result_abs_path):
        os.makedirs(result_abs_path)
    print("Storing output plot in %s" %(result_abs_path))
    bin_abs_path = curr_dir + bm_bin_dir

    # Run the binaries and store the results
    # Assemble the command - does not support Windows for now
    command = base_command
    command[0] = bin_abs_path + command[0]
    if platform.system() == "Linux":
        command = linux_command_prefix + command
    memory_size_str = memory_size_default_str
    if len(sys.argv) == 1:
        # Run with default memory size
        print("Total memory size %s" %(memory_size_str))
        run_bm(command, result_abs_path)
    else:
        memory_size_str = sys.argv[1]
        print("Total memory size %s" %(memory_size_str))
        command[-2] = memory_size_str
        run_bm(command, result_abs_path)


if __name__ == "__main__":
    main()
