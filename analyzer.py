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

def bestconfigs(bench_results, filter_blocksize=None, show_all=False):
    best_latency = []
    best_throughput = []
    grouped = _group_by_operation(bench_results)

    for operation in grouped:
        configs = grouped[operation]

        if filter_blocksize is not None:
            filter_blocksize = int(filter_blocksize)
            configs = [cfg for cfg in configs if cfg.blocksize_kb == filter_blocksize]

        sorted_by_latency = sorted(configs, key=lambda cfg: cfg.latency_ms.avg)
        sorted_by_throughtput = sorted(configs, key=lambda cfg: cfg.throughput_kbs, reverse=True)

        if show_all:
            best_latency.extend(sorted_by_latency)
            best_throughput.extend(sorted_by_throughtput)
        else:
            best_latency.append(sorted_by_latency[0])
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
