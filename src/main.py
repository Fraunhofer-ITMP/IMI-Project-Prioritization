# -*- coding: utf-8 -*-

"""Main file to reproduce the results."""

from fair_vocab_mapping import get_fair_mapping
from scrapper import get_metadata

if __name__ == '__main__':
    get_metadata()
    get_fair_mapping()
