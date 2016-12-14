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
USER_INFOS_PATH = os.path.join(DATA_DIR, "user_infos.json")
CRED_PATH = os.path.join(ROOT_DIR, "config", "credentials.json")


def groups(items, grp_size):
    chunk = []
    for item in items:
        chunk.append(item)
        if len(chunk) == grp_size:
            yield chunk
            del chunk[:]
    yield chunk


async def collect_users(ctx, user_ids):
    users = []
    for chunk in groups(user_ids, 100):
        req = bw.api.users.lookup(user_id=",".join(str(s) for s in chunk))
        users.extend((await ctx(req, timeout=90)).body)
    return users


if __name__ == '__main__':
    with open(RETWEET_IDS_PATH) as fp:
        retweet_ids = json.load(fp)
        user_ids = {i for items in retweet_ids.values() for i in items}


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

        user_infos = loop.run_until_complete(collect_users(ctx, user_ids))
        print("\tcollected {}".format(len(user_infos)))

    with open(USER_INFOS_PATH, 'w') as fp:
        json.dump(user_infos, fp)
