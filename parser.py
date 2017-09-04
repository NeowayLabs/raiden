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


def parse(rawdata):
    lines = rawdata.readlines()
    chunk_size, lines = _parse_chunk_size(lines)
    blocksize_tests = _parse_blocksize_tests(lines)
    return BenchmarkResult(chunk_size_kb=chunk_size, blocksize_tests=blocksize_tests)


def _parse_chunk_size(lines):
    chunksize_prefix = "RAID chunk size (KB):"
    for i, line in enumerate(lines):
        if not line.startswith(chunksize_prefix):
            continue

        parsed_chunk_size = line.split(chunksize_prefix)
        return int(parsed_chunk_size[1]), lines[i+1:]

    raise Exception("Unable to locate chunk size prefix on benchmark log")


def _parse_blocksize_tests(lines):
    blocksize_tests = []
    while lines != []:
        blocksize_test, lines = _parse_blocksize_test(lines)
        blocksize_tests.append(blocksize_test)
    return blocksize_tests


def _parse_blocksize_test(lines):
    blocksize_test_start_prefix = "========== starting tests with blocksize:"
    blocksize_test_end = "========== done =========="

    for i, line in enumerate(lines):

        if line.startswith(blocksize_test_start_prefix):
            blocksize_kb = int(line.split(blocksize_test_start_prefix)[1].split(" ")[1].replace("K",""))
            start = i

        if line.startswith(blocksize_test_end):
            end = i
            break

    results = _parse_operation_test_results(lines[start:end])
    lines = lines[end+1:]
    return BlockSizeTestResult(
            blocksize_kb=blocksize_kb,
            results=results,
    ), lines

def _parse_operation_test_results(lines):

    for i, line in enumerate(lines):
        if not line.startswith("testing"):
            continue

        operation, newlines = _parse_operation_test_result(lines[i:])
        operations = _parse_operation_test_results(newlines)
        operations.append(operation)
        return operations

    return []

def _parse_operation_test_result(lines):

    parsed_operation = lines[0].split(" ")
    operation = parsed_operation[1].strip() + " " + parsed_operation[2].strip()

    throughput_kbs_prefix=parsed_operation[2].strip()

    for i, line in enumerate(lines[1:]):
        if throughput_kbs_prefix == line.split(":")[0].strip():
            throughput_kbs = _parse_throughput(line)
            continue

        if "lat (msec): " in line:
            latency_ms = _parse_latency(line)
            end = i + 1
            break

    return OperationTestResult(
        operation=operation,
        throughput_kbs=throughput_kbs,
        latency_ms=latency_ms,
    ), lines[end+1:]

def _parse_throughput(line):
    # ("write: "io=35480MB, bw=302754KB/s, iops=37844, runt=120004msec
    pass

def _parse_latency(line):
    # if line.startswith("lat (msec): "min=1, max=307, avg= 2.64, stdev= 3.79
    pass
