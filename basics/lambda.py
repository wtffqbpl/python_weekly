#! coding: utf-8

import contextlib
import io
import unittest


def lambda_test():
    strings = ['foo', 'card', 'bar', 'aaaa', 'abab']
    strings.sort(key=lambda x: len(set(x)))

    print(' '.join(strings))


class TestLambda(unittest.TestCase):
    def test_sum(self):
        # Start Capture stdout
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            lambda_test()

        self.assertEqual('aaaa foo abab bar card\n', f.getvalue())


if __name__ == '__main__':
    unittest.main()