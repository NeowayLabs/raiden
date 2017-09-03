from collections import namedtuple

BenchmarkResult = namedtuple('BenchmarkResult', ['chunk_size'])

def parse(rawdata):
    lines = rawdata.readlines()
    chunk_size, lines = _parse_chunk_size(lines)
    return BenchmarkResult(chunk_size=chunk_size)

def _parse_chunk_size(lines):
    chunksize_prefix = "RAID chunk size (KB):"
    for i, line in enumerate(lines):
        if not line.startswith(chunksize_prefix):
            continue

        parsed_chunk_size = line.split(chunksize_prefix)
        return int(parsed_chunk_size[1]), lines[i+1:]

    raise Exception("Unable to locate chunk size prefix on benchmark log")
