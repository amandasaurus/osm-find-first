# -*- coding: utf-8 -*-

__author__ = 'Rory McCann'
__email__ = 'rory@technomancy.org'
__version__ = '0.1.0'

import requests
import csv
import argparse
import sys
from xml.etree import ElementTree
import logging

logger = logging.getLogger(__name__)

def is_int(x):
    try:
        int(x)
        return True
    except:
        return False

def is_osm_type(x):
    return x in ['node', 'way', 'relation']

# osm_type ("node"/"way"/"relation"), osm_id, osm_uid, osm_user, osm_timestamp (ISO formatted)
def find_first(known_data, osm_objs):
    if len(osm_objs) == 0:
        return known_data

    # ensure it's correct format
    osm_objs = [{'osm_type': str(x['osm_type']), 'osm_id': str(x['osm_id'])} for x in osm_objs]

    known_data_indexed = {(x['osm_type'], x['osm_id']): x for x in known_data}
    missing_objs = [x for x in osm_objs if (x['osm_type'], x['osm_id']) not in known_data_indexed]

    logger.info("Need to query OSM for %d objects", len(missing_objs))

    for obj in missing_objs:
        assert is_osm_type(obj['osm_type'])
        assert is_int(obj['osm_id'])
        url = "http://api.openstreetmap.org/api/0.6/{osm_type}/{osm_id}/1".format(**obj)
        response = requests.get(url)
        parsed = ElementTree.fromstring(response.content)
        attrib = parsed[0].attrib

        osm_uid = attrib['uid']
        osm_user = attrib['user']
        osm_timestamp = attrib['timestamp']
        logger.debug("Got details for %s %s", obj['osm_type'], obj['osm_id'])

        known_data.append({'osm_id': obj['osm_id'], 'osm_type': obj['osm_type'], 'osm_uid': osm_uid, 'osm_user': osm_user, 'osm_timestamp':osm_timestamp})

    return known_data

def find_first_from_csv(csv_filename, osm_objs):
    with open(csv_filename) as fp:
        csv_reader = csv.DictReader(fp)
        known_data = list(csv_reader)

    new_data = find_first(known_data, osm_objs)

    write_to_csv(csv_filename, new_data)

    osm_objs = []

def write_to_csv(filename, result_data):
    with open(csv_filename, 'w') as fp:
        csv_writer = csv.DictWriter(fp, ['osm_type', 'osm_id', 'osm_user', 'osm_uid', 'osm_timestamp'])
        csv_writer.writeheader()
        csv_writer.writerows(new_data)


def main(argv):

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.setLevel(logging.DEBUG)

    find_first_from_csv('ieadmins.csv', [{'osm_type': 'relation', 'osm_id': '4121287'},{'osm_type':'relation', 'osm_id':'4072665'}])


if __name__ == '__main__':
    main(sys.argv[1:])
