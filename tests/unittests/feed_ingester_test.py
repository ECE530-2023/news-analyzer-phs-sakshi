"""Tests Feed Ingester module"""
import logging
import src.FeedIngester.ingester_feed as IngesterFeed
import json


def test_ingest_file():
    """
    :return: tests file ingestion
    """
    testcases = [
        [None, False],
        [json.dumps({'filename': 'file 1', 'content': 'something'}), True]
    ]
    for test in testcases:
        logging.info("testing case" + str(test))
        assert IngesterFeed.ingest_file(test[0]) == test[1]


test_ingest_file()
