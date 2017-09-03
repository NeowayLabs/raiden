import unittest

import parser


class ParserTests(unittest.TestCase):

    def test_parse(self):

        with open("./testdata/chunk-size-512k.log", "r") as rawdata:
            parsed_chunk_test = parser.parse(rawdata)
            self.assertEqual(512, parsed_chunk_test.chunk_size_kb)
            self.assertEqual([
                BlockSizeTest(blocksize_kb=8, results=[
                        OperationTestResult(
                            operation="sequential write",
                            latency_ms=Latency(min=1.0,max=299.0,avg=2.45),
                            throughput_kbs=325885,
                        ),
                        OperationTestResult(
                            operation="sequential read",
                            latency_ms=Latency(min=0.0, max=369016.0, avg=1546.10),
                            throughput_kbs=516940,
                        ),
                ]),
                BlockSizeTest(blocksize_kb=16, results=[
                        OperationTestResult(
                            operation="sequential write",
                            latency_ms=Latency(min=1.0, max=309.0, avg=2.46),
                            throughput_kbs=650900,
                        ),
                ]),
            ], parsed_chunk_test.blocksize_tests)

if __name__ == '__main__':
    unittest.main()
