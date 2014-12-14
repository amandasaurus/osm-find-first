#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_osm_find_first
----------------------------------

Tests for `osm-find-first` module.
"""

import unittest
import tempfile

import osm_find_first


class TestOsmFindFirst(unittest.TestCase):

    def testInt(self):
        for good in [1, '1', 1.0]:
            self.assertTrue(osm_find_first.is_int(good), msg=repr(good))
        for bad in ['foo']:
            self.assertFalse(osm_find_first.is_int(bad), msg=repr(bad))

    def testOSMType(self):
        for good in ['node', 'way', 'relation']:
            self.assertTrue(osm_find_first.is_osm_type(good), msg=repr(good))
        for bad in ['foo']:
            self.assertFalse(osm_find_first.is_osm_type(bad), msg=repr(bad))

    def testWriteResultsToCSV(self):
        outputfile = tempfile.NamedTemporaryFile()
        outputfilename = outputfile.name

        results = [{'osm_type': 'relation', 'osm_id': 2227344, 'osm_user': 'brianh', 'osm_uid': 19612, 'osm_timestamp': '2012-06-12 15:24:49+01'}]

        osm_find_first.write_to_csv(outputfilename, results)

        outputfile.seek(0,0)
        
        self.assertEqual(outputfile.read().decode("utf8"), 'osm_type,osm_id,osm_user,osm_uid,osm_timestamp\nrelation,2227344,brianh,19612,2012-06-12 15:24:49+01\n')
        outputfile.close()

    def testReadMissingFromCSV(self):
        csv_content = 'osm_type,osm_id\nrelation,123\n'

        outputfile = tempfile.NamedTemporaryFile()
        outputfilename = outputfile.name
        outputfile.write(csv_content.encode("utf8"))
        outputfile.seek(0)

        missing = osm_find_first.read_missing_from_csv(outputfilename)

        self.assertEqual(missing, [{'osm_type': 'relation', 'osm_id': '123'}])

        outputfile.close()
        

if __name__ == '__main__':
    unittest.main()
