#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from tweetlib import get_all_tweets, write_out_csv

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Provide twitter handle as argument")
        sys.exit()

    if not os.path.exists('results'):
        os.mkdir('results')

    alltweets = get_all_tweets(sys.argv[1])

    write_out_csv(alltweets, sys.argv[1])
