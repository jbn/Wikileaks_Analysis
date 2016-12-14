#!/usr/bin/env python

import json
import os
import sys
from vaquero import ModulePipeline, Vaquero

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.join(THIS_DIR, os.pardir)
DATA_DIR = os.path.join(ROOT_DIR, "data")
DATA_PATH = os.path.join(DATA_DIR, "merged.json")
WIKILEAKS_PATH = os.path.join(DATA_DIR, "wikileaks.json")


if __name__ == '__main__':
    with open(DATA_PATH) as fp:
        tweets = json.load(fp)

    import sys
    sys.path.append(THIS_DIR)
    import record_pipeline
    pipeline = ModulePipeline(record_pipeline)
    vaq = Vaquero(max_failures=0)

    results = []
    for tweet in tweets:
        dst = {}
        with vaq:
            pipeline(tweet, dst)
            results.append(dst)

    with open(WIKILEAKS_PATH, "w") as fp:
        json.dump(results, fp)

    print(vaq.stats())
