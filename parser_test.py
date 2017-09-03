import unittest

import parser


class ParserTests(unittest.TestCase):

    def test_parse(self):

        with open("./testdata/chunk-size-512k.log", "r") as rawdata:
            parsed_chunk_test = parser.parse(rawdata)
            self.assertEqual(512, parsed_chunk_test.chunk_size)

if __name__ == '__main__':
    unittest.main()
