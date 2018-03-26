#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tweepy
import csv
import yaml


def load_yaml(filename):
    with open(filename, 'r') as f:
        data = yaml.load(f)
    return data


def authorize_api(filename='config.yml'):
    """
    Authorize twitter, initialize tweepy, uses config.yml by default
    """
    config = load_yaml('config.yml')
    secrets = config['secrets']
    auth = tweepy.OAuthHandler(secrets['consumer_key'],
                               secrets['consumer_secret'])
    auth.set_access_token(secrets['access_token'],
                          secrets['access_secret'])
    api = tweepy.API(auth)

    return api


def get_tweet(id_num):
    """
    Get a single tweet based on the id number of the tweet
    """
    api = authorize_api()

    print("Getting tweet {}".format(id_num))

    # Get the tweet
    tweet = api.get_status(id_num)

    return tweet


def get_all_tweets(screen_name):
    """
    Twitter allows access to a users most recent 3240 tweets with this method
    """
    api = authorize_api()

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

    return alltweets


def write_out_csv(alltweets, screen_name, path='results'):
    """
    Write all tweets list to an output .csv file
    """

    # Transform the tweepy tweets into a 2D array that will populate the .csv
    outtweets = [[tweet.id_str, tweet.created_at,
                 tweet.text, tweet.source,
                 tweet.entities['hashtags'],
                 tweet.entities['symbols'],
                 tweet.entities['user_mentions'],
                 tweet.entities['urls'],
                 tweet.retweet_count,
                 tweet.favorite_count]
                 for tweet in alltweets]

    # Write the .csv
    filename = os.path.join(path, '{}_tweets.csv'.format(screen_name))
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'created_at', 'text', 'source',
                         'hashtags', 'symbols', 'user_mentions', 'urls',
                         'retweet_count', 'favorite_count'])
        writer.writerows(outtweets)

    return
