import numpy as np
import pyopencl as cl
import sys
import argparse
import os
from time import time

from batched_regression import _print_memory_usage, find_best_models_gpu


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Performs massive multilinear regresions from the combinatorics of predictors from 1 to MaxPredictors). Selects the best model base on some criteria (RMSE) by default")
    parser.add_argument('-i', dest="input_file",
                        help="CSV file with predictors data")
    parser.add_argument('-w', dest="window", default=300,
                        help="Window of data to perform regressions.  Recommended: 300 for hourly data, 50 for daily data")
    parser.add_argument('-n', dest="max_predictors", help="Max numbers of predictors to combine", default=8)
    parser.add_argument('-o', dest="output_file", default=None,
                        help="Output file with combinations and metrics results")
    parser.add_argument('-m', dest="metric", default="rmse",
                        help="Metric to be calculated for the possible model")
    parser.add_argument('-d', dest="device", default="gpu",
                        help="Device to use to perform calculations")

    args = parser.parse_args()

    input_file = args.input_file
    window = args.window
    max_predictors = args.max_predictors
    output_file = args.ouput_file if args.output_file else "{}-w{}-mp{}.csv".format(input_file, window, max_predictors)
    metric = args.metric
    device = args.device

    if any(x is None for x in [input_file, window, max_predictors, output_file, metric]):
        parser.print_help()
        sys.exit(0)

    return input_file, int(window), int(max_predictors), metric, output_file, device


# _print_memory_usage("Initial State: ")
start_time = time()
input_file, window, max_predictors, metric, output_file, device = parse_arguments()
if device == "gpu":
    print "Running calculations on GPU"
    ordered_combs = find_best_models_gpu(file_name=input_file, max_predictors=max_predictors, metric=metric,  window=window)
    "Should dump to output_file=output_file"
print "Using GPU to do regressions took {}".format(time() - start_time)