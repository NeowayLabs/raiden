from collections import namedtuple

RaidConfig = namedtuple(
    'RaidConfig',
    [
        'chunk_size_kb',
        'blocksize_kb',
        'operation',
        'latency_ms',
        'throughput_kbs'
    ],
)

BestConfigs = namedtuple(
    'BestConfigs',
    [ 'best_latency', 'best_throughput' ],
)

def bestconfigs(bench_results):
    return BestConfigs(best_latency=[], best_throughput=[])
