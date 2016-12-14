#!/usr/bin/env python

import os
import json

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.join(THIS_DIR, os.pardir)
DATA_DIR = os.path.join(ROOT_DIR, "data")
TWEETS_PATH = os.path.join(DATA_DIR, "tweets.json")
RETWEET_IDS_PATH = os.path.join(DATA_DIR, "retweet_ids.json")
USER_INFOS_PATH = os.path.join(DATA_DIR, "user_infos.json")
DATA_PATH = os.path.join(DATA_DIR, "merged.json")


if __name__ == '__main__':
    with open(TWEETS_PATH) as fp:
        tweets = json.load(fp)


    with open(RETWEET_IDS_PATH) as fp:
        retweet_ids = {int(k): v for k, v in json.load(fp).items()}


    with open(USER_INFOS_PATH) as fp:
        user_infos = {nfo['id']: nfo for nfo in json.load(fp)}

    for tweet in tweets:
        tweet_id = tweet['id']
        retweeters = retweet_ids.get(tweet_id, {})
        tweet['retweet_ids'] = retweeters
        tweet['retweeter_infos'] = [user_infos[uid] for uid in retweeters
                                    if uid in user_infos]

    with open(DATA_PATH, "w") as fp:
        json.dump(tweets, fp)
