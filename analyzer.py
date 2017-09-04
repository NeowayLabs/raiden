from collections import namedtuple
from collections import defaultdict

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
    best_latency = []
    best_throughput = []
    grouped = _group_by_operation(bench_results)

    for operation in grouped:
        configs = grouped[operation]

        sorted_by_latency = sorted(configs, key=lambda cfg: cfg.latency_ms.avg)
        best_latency.append(sorted_by_latency[0])

        sorted_by_throughtput = sorted(configs, key=lambda cfg: cfg.throughput_kbs, reverse=True)
        best_throughput.append(sorted_by_throughtput[0])

    return BestConfigs(
        best_latency=best_latency,
        best_throughput=best_throughput,
    )

def _group_by_operation(bench_results):

    grouped = defaultdict(list)

    for bench_res in bench_results:
        for blocksize_res in bench_res.blocksize_tests:
            for res in blocksize_res.results:
                config = RaidConfig(
                    chunk_size_kb = bench_res.chunk_size_kb,
                    blocksize_kb = blocksize_res.blocksize_kb,
                    operation = res.operation,
                    latency_ms = res.latency_ms,
                    throughput_kbs = res.throughput_kbs,
                )
                grouped[res.operation].append(config)

    return grouped

def _best_latency():
    pass
