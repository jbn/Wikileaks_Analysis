import jmespath
from dateutil.parser import parse as parse_date

ESSENTIALS = [('id', 'tweet_id'),
              ('text', 'tweet_text'),
              ('length(text)', 'n_chars'),
              ('favorite_count', 'n_favorites'),
              ('retweet_count', 'n_retweets'),
              ('length(entities.hashtags)', 'n_hashtags'),
              ('length(entities.urls)', 'n_urls'),
              ('length(entities.user_mentions)', 'n_mentions'),
              ('is_quote_status', 'is_quote_status'),
              ('source', 'source')]

ESSENTIALS = [(jmespath.compile(k), v) for k, v in ESSENTIALS]


def copy_essentials(src, dst):
    for k1, k2 in ESSENTIALS:
        dst[k2] = k1.search(src)


def extract_date(src, dst):
    dst['created_at'] = parse_date(src['created_at']).isoformat()
