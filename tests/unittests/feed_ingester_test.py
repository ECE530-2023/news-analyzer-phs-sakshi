"""Tests Feed Ingester module"""
import logging
import src.FeedIngester.IngesterFeed as IngesterFeed


def test_ingest_file():
    """
    :return: tests file ingestion
    """
    testcases = [
        [None, False],
        ['file 1', True]
    ]
    for test in testcases:
        logging.info("testing case" + str(test))
        assert IngesterFeed.ingest_file(test[0]) == test[1]


test_ingest_file()
