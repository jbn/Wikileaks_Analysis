all: data/tweets.json data/retweet_ids.json data/user_infos.json data/merged.json data/wikileaks.json

data/tweets.json: bin/collect_tweets.py
	./bin/collect_tweets.py

data/retweet_ids.json: bin/collect_retweet_ids.py
	./bin/collect_retweet_ids.py

data/user_infos.json: bin/collect_user_infos.py
	./bin/collect_user_infos.py

data/merged.json: bin/merge.py
	./bin/merge.py

data/wikileaks.json: bin/simplify.py bin/record_pipeline.py
	./bin/simplify.py
