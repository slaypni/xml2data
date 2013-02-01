import unittest
import xml2data


def suite():
    tests = ['xml2data.testsuite.test_xml2data']
    return unittest.TestLoader().loadTestsFromNames(tests)
