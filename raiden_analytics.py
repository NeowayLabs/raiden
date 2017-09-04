import glob
import argparse

import parser
import analyzer

def print_raid_config(cfg):
    print("operation: {}".format(cfg.operation))
    print("chunk_size_kb: {}".format(cfg.chunk_size_kb))
    print("blocksize_kb: {}".format(cfg.blocksize_kb))
    print("latency_ms: {}".format(cfg.latency_ms))
    print("throughput_kbs: {}".format(cfg.throughput_kbs))

argparser = argparse.ArgumentParser(description="Helps analyzing raiden tests output")

argparser.add_argument(
    '--benchmarks-files',
    help="The benchmarks files, the whole output of raiden.sh. Use a pattern name for multiple files, eg: *.log",
    dest='benchmarks_files',
)

args = argparser.parse_args()
if args.benchmarks_files is None:
    parser.print_help()
    exit(0)

benchmarks_files = glob.glob(args.benchmarks_files)
print("analyzing benchmarks_files: {}".format(benchmarks_files))
parsed_results = []

for benchmarks_file in benchmarks_files:
    with open(benchmarks_file, "r") as f:
        parsed_results.append(parser.parse(f))

configs = analyzer.bestconfigs(parsed_results)
print("\n\n==== best configurations for minimum latency (per operation) ====\n")
for cfg in configs.best_latency:
    print_raid_config(cfg)
    print("\n\n")

print("==== best configurations for maximum throughput (per operation) ====\n")
for cfg in configs.best_throughput:
    print_raid_config(cfg)
    print("\n\n")
