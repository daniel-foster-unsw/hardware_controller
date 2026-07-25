"""
Helper functions for packet assertions.
"""


def assert_packets(actual, expected):

    assert len(actual) == len(expected)

    for a, e in zip(actual, expected):

        assert a == e