import unittest

import parser
import bench


class ParserTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @unittest.skip("TODO")
    def test_parse(self):

        with open("./testdata/chunk-size-512k.log", "r") as rawdata:
            parsed_chunk_test = parser.parse(rawdata)

            self.assertEqual(512, parsed_chunk_test.chunk_size_kb)

            self.assertEqual(
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
                parsed_chunk_test.blocksize_tests[0],
            )

            self.assertEqual(
                bench.BlockSizeTestResult(blocksize_kb=16, results=[
                        bench.OperationTestResult(
                            operation="sequential write",
                            latency_ms=bench.Latency(min=1.0, max=309.0, avg=2.46),
                            throughput_kbs=650900,
                        ),
                ]),
                parsed_chunk_test.blocksize_tests[1],
            )

    def test_parse_regression_03_09_2017(self):
        # Just validates no exception
        with open("./testdata/regression-test-03-09-2017.log", "r") as rawdata:
            res = parser.parse(rawdata)
            self.assertNotEqual(0, len(res))

    def test_parse_regression_04_09_2017(self):
        # Just validates no exception
        with open("./testdata/regression-test-04-09-2017.log", "r") as rawdata:
            res = parser.parse(rawdata)
            self.assertNotEqual(0, len(res))

if __name__ == '__main__':
    unittest.main()
