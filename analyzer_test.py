import unittest

import bench
import analyzer

class AnalyzerTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_analyzer_overall(self):
        benchmarkresults = [
                BenchmarkResult(
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
                )
        ]
