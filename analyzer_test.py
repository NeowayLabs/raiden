import unittest

import bench
import analyzer

class AnalyzerTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_analyzer_bestconfigs(self):
        benchmark_results = [
                bench.BenchmarkResult(
                    chunk_size_kb=512,
                    blocksize_tests=[
                        bench.BlockSizeTestResult(blocksize_kb=8, results=[
                                bench.OperationTestResult(
                                    operation="sequential write",
                                    latency_ms=bench.Latency(min=1.0,max=299.0,avg=2.45),
                                    throughput_kbs=325885,
                                ),
                                bench.OperationTestResult(
                                    operation="sequential read",
                                    latency_ms=bench.Latency(min=0.0, max=369.016, avg=1.5460999999999998),
                                    throughput_kbs=516940,
                                ),
                        ]),
                    ]
                ),
                bench.BenchmarkResult(
                    chunk_size_kb=256,
                    blocksize_tests=[
                        bench.BlockSizeTestResult(blocksize_kb=16, results=[
                                bench.OperationTestResult(
                                    operation="sequential write",
                                    latency_ms=bench.Latency(min=1.0,max=299.0,avg=4.45),
                                    throughput_kbs=425885,
                                ),
                                bench.OperationTestResult(
                                    operation="sequential read",
                                    latency_ms=bench.Latency(min=0.0, max=369.016, avg=1.0),
                                    throughput_kbs=316940,
                                ),
                        ]),
                    ]
                )
        ]

        configs = analyzer.bestconfigs(benchmark_results)

        self.assertEqual([
            analyzer.RaidConfig(
                chunk_size_kb=512,
                blocksize_kb=8,
                operation="sequential write",
                latency_ms=bench.Latency(min=1.0,max=299.0,avg=2.45),
                throughput_kbs=325885,
            ),
            analyzer.RaidConfig(
                chunk_size_kb=256,
                blocksize_kb=16,
                operation="sequential read",
                latency_ms=bench.Latency(min=0.0, max=369.016, avg=1.0),
                throughput_kbs=316940,
            ),
        ], configs.best_latency)

        self.assertEqual([
            analyzer.RaidConfig(
                chunk_size_kb=256,
                blocksize_kb=16,
                operation="sequential write",
                latency_ms=bench.Latency(min=1.0,max=299.0,avg=4.45),
                throughput_kbs=425885,
            ),
            analyzer.RaidConfig(
                chunk_size_kb=512,
                blocksize_kb=8,
                operation="sequential read",
                latency_ms=bench.Latency(min=0.0, max=369.016, avg=1.5460999999999998),
                throughput_kbs=516940,
            ),
        ], configs.best_throughput)

if __name__ == '__main__':
    unittest.main()
