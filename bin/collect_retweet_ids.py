#!/usr/bin/env python

import asyncio
import os
import json

import aiohttp
import brittle_wit as bw


THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.join(THIS_DIR, os.pardir)
DATA_DIR = os.path.join(ROOT_DIR, "data")
TWEETS_PATH = os.path.join(DATA_DIR, "tweets.json")
RETWEET_IDS_PATH = os.path.join(DATA_DIR, "retweet_ids.json")
CRED_PATH = os.path.join(ROOT_DIR, "config", "credentials.json")


async def collect_retweeter_ids_for(ctx, tweet_id):
    req = bw.api.statuses.retweeters_ids(tweet_id)

    ids = set()
    cursor = bw.Cursor(req)
    for page_req in cursor:
        resp = await ctx(page_req)
        ids.update(resp.body['ids'])
        cursor.update(resp)

    return list(ids)


if __name__ == '__main__':
    with open(TWEETS_PATH) as fp:
        tweet_ids = [t['id'] for t in json.load(fp)
                     if t.get('retweet_count', 0) > 0]

    with open(CRED_PATH) as fp:
        cfg = json.load(fp)

    app_cred = bw.AppCredentials(cfg['app_key'], cfg['app_secret'])

    client_cred = bw.ClientCredentials(cfg['user_id'],
                                       cfg['user_token'],
                                       cfg['user_secret'])

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    retweet_ids = {}
    with aiohttp.ClientSession() as conn:
        req_processor = bw.ClientRequestProcessor(client_cred)
        ctx = bw.ContextualizedProcessor(conn, app_cred, req_processor)

        for tweet_id in tweet_ids:
            print("Processing", tweet_id)
            coro = collect_retweeter_ids_for(ctx, tweet_id)
            retweet_ids[tweet_id] = loop.run_until_complete(coro)
            print("\tcollected {}".format(len(retweet_ids[tweet_id])))

    with open(RETWEET_IDS_PATH, 'w') as fp:
        json.dump(retweet_ids, fp)
