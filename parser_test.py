import unittest

import parser


class ParserTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_parse(self):

        with open("./testdata/chunk-size-512k.log", "r") as rawdata:
            parsed_chunk_test = parser.parse(rawdata)

            self.assertEqual(512, parsed_chunk_test.chunk_size_kb)

            self.assertEqual(
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
                parsed_chunk_test.blocksize_tests[0],
            )

            self.assertEqual(
                parser.BlockSizeTestResult(blocksize_kb=16, results=[
                        parser.OperationTestResult(
                            operation="sequential write",
                            latency_ms=parser.Latency(min=1.0, max=309.0, avg=2.46),
                            throughput_kbs=650900,
                        ),
                ]),
                parsed_chunk_test.blocksize_tests[1],
            )

if __name__ == '__main__':
    unittest.main()
