#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import tweepy
import csv
import yaml


def load_yaml(filename):
    with open(filename, 'r') as f:
        data = yaml.load(f)
    return data


def get_all_tweets(screen_name):
    # Twitter allows access to a users most recent 3240 tweets with this method

    # Authorize twitter, initialize tweepy
    config = load_yaml('config.yml')
    secrets = config['secrets']
    auth = tweepy.OAuthHandler(secrets['consumer_key'],
                               secrets['consumer_secret'])
    auth.set_access_token(secrets['access_token'],
                          secrets['access_secret'])
    api = tweepy.API(auth)

    # Initialize a list to hold all the tweepy Tweets
    alltweets = []

    # Make initial request for most recent tweets (200 is the max count)
    new_tweets = api.user_timeline(screen_name=screen_name,
                                   count=200)

    # Save most recent tweets
    alltweets.extend(new_tweets)

    # Save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # Keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("Getting tweets before id {}".format(oldest))

        # All subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name,
                                       count=200,
                                       max_id=oldest)

        # Save most recent tweets
        alltweets.extend(new_tweets)

        # Update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...{} tweets downloaded so far".format(len(alltweets)))

    # Transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at,
                 tweet.text, tweet.source,
                 tweet.entities['hashtags'],
                 tweet.entities['symbols'],
                 tweet.entities['user_mentions'],
                 tweet.entities['urls'],
                 tweet.retweet_count,
                 tweet.favorite_count]
                 for tweet in alltweets]

    # Write the csv
    filename = os.path.join('results', '{}_tweets.csv'.format(screen_name))
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'created_at', 'text', 'source',
                         'hashtags', 'symbols', 'user_mentions', 'urls',
                         'retweet_count', 'favorite_count'])
        writer.writerows(outtweets)

    return


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Provide twitter handle as argument")
        sys.exit()

    if not os.path.exists('results'):
        os.mkdir('results')

    get_all_tweets(sys.argv[1])
