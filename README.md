# What is this?

This repository allows you to replicate my cursory analysis of [@wikileaks](http://twitter.com/wikileaks) over the 2016 election cycle.

See the medium post: [Who Watches Wikileaks?](https://medium.com/@generativist/who-watches-wikileaks-982c50fab0f7#.3kkef32l0)

## Installation

First, setup the project and environment.

```sh
git clone https://github.com/jbn/Wikileaks_Analysis.git
cd Wikileaks_Analysis
conda create --name wikileaks_analysis python=3.5  # Or, virtual_env equiv.
source activate wikileaks_analysis
pip install -r requirements.txt
```

Then you have to edit `config/credentials.json.orig`, adding your [Twitter Developer API credentials](https://dev.twitter.com/). Then, rename that file to `config/credentials.json`.

Then, run

```sh
make
```

to collect the data.

Notebook to get you started with the data is in `notebooks`.

The original tweet ids are in the `original_tweet_ids.txt` for exact replication, if desired.

## TODO

1. Bayesian switch-point analysis over various metrics (esp. over the retweet ratio) for detecting changes in interaction patterns, outside of just electoral leaking.
2. Linguistic analysis for detecting a regime change in content.
3. The collector collects the 100 most recent retweeters for each tweet, along with their user information. This affords the opportunity to look at the alter interactions of wikileaks, overtime. That's want I really wanted to do, but I ran out of time. The 100 limit is an API constraint. (And, sometimes it's less, for deleted tweets, which offers some signal, too).
4. Submit a PR for more ideas.
