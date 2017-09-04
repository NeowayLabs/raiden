import unittest

import parser
import analyzer

class AnalyzerTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_analyzer_overall(self):
        benchmarkresults = [
                BenchmarkResult(
                    chunk_size_kb=512,
                    blocksize_tests=[
                        parser.BlockSizeTestResult(blocksize_kb=8, results=[
                                parser.OperationTestResult(
                                    operation="sequential write",
                                    latency_ms=parser.Latency(min=1.0,max=299.0,avg=2.45),
                                    throughput_kbs=325885,
                                ),
                                parser.OperationTestResult(
                                    operation="sequential read",
                                    latency_ms=parser.Latency(min=0.0, max=369.016, avg=1.5460999999999998),
                                    throughput_kbs=516940,
                                ),
                        ]),
                    ]
                )
        ]
