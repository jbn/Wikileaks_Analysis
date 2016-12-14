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
CRED_PATH = os.path.join(ROOT_DIR, "config", "credentials.json")


async def collect_tweets_of(ctx, screen_name):
    tweets, observed_ids = [], set()
    max_id, kwargs = None, {'screen_name': screen_name,
                            'count': 200,
                            'include_rts': 'true'}
    while True:
        req = bw.api.statuses.user_timeline(**kwargs)
        page = await ctx(req, timeout=90)
        statuses = page.body

        # Stop when there are no new entries.
        status_ids = {d['id'] for d in statuses}
        if not (status_ids - observed_ids):
            break

        # Add unique statuses.
        for status in statuses:
            if status['id'] not in observed_ids:
                tweets.append(status)

        observed_ids.update(status_ids)
        kwargs['max_id'] = min(status_ids) - 1

    return tweets


if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(CRED_PATH) as fp:
        cfg = json.load(fp)

    app_cred = bw.AppCredentials(cfg['app_key'], cfg['app_secret'])

    client_cred = bw.ClientCredentials(cfg['user_id'],
                                       cfg['user_token'],
                                       cfg['user_secret'])

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    with aiohttp.ClientSession() as conn:
        req_processor = bw.ClientRequestProcessor(client_cred)
        ctx = bw.ContextualizedProcessor(conn, app_cred, req_processor)

        tweets = loop.run_until_complete(collect_tweets_of(ctx, 'wikileaks'))
        print("Collected {} tweets".format(len(tweets)))

    with open(TWEETS_PATH, 'w') as fp:
        json.dump(tweets, fp)
