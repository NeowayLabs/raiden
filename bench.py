from collections import namedtuple

BenchmarkResult = namedtuple(
    'BenchmarkResult',
    ['chunk_size_kb', 'blocksize_tests'],
)

BlockSizeTestResult = namedtuple(
    'BlockSizeTestResult',
    ['blocksize_kb', 'results'],
)

OperationTestResult = namedtuple(
    'OperationTestResult',
    ['operation', 'latency_ms', 'throughput_kbs'],
)

Latency = namedtuple( 'Latency', ['min', 'max', 'avg'])
