#!/usr/bin/env python

import argparse
import configparser
import os
import tweepy #https://github.com/tweepy/tweepy
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

def arg_parser():
    parser = argparse.ArgumentParser(description = 'twitter flight deal notifier')
    parser.add_argument('-c', dest = 'config', metavar = 'config file')
    args = parser.parse_args()
    return (args)

def twitter_auth():
    consumer_key = get_config_item('tweepy', 'consumer_key')
    consumer_secret = get_config_item('tweepy', 'consumer_secret')
    access_key = ""
    access_secret = ""
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return tweepy.API(auth)

def text_parse(text):
    if 'deal' in text.lower() and '$' in text.lower():
        return True
    else:
        return False

def email_deal(text):
    server = smtplib.SMTP(get_config_item('email', 'server'), int(get_config_item('email', 'port')))
    user = get_config_item('email', 'user')
    pw = get_config_item('email', 'pass')
    recipients = get_config_item('email', 'recipients')
    
    msg = MIMEText(text.encode("utf-8"))
    msg['Subject'] = 'SB test: Airfare Deal Found!'
    msg['From'] = user
    #msg['To'] = ','.join(recipients)
    msg['To'] = recipients
    
    server.starttls()
    server.login(user, pw)
    server.sendmail(user, recipients, msg.as_string())
    server.quit

def write_csv(screen_name, tweets):
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(tweets)

def get_config_item(section, item):
    """
    Retrieves a value based on the section and item requested from the configuration file.
    :param section: Section of the config file
    :param item: item within a section
    :return: config value
    """
    config = configparser.RawConfigParser()
    config_file = args.config
    if not os.path.isfile(config_file):
        logging.error('Configuration file supplied does not exist. Exiting.')
        sys.exit()
    config.read(config_file)
    ret = config[section].get(item)
    return ret

def main(screen_name):
    
    
    api = twitter_auth()
    
    new_tweets = api.user_timeline(screen_name = screen_name,count=50)
    
    #parse out tweets not containing special text
    for tweet in new_tweets:
        if text_parse(tweet.text):
            print 'deal found!\n', 'created:', tweet.created_at, '\n', tweet.text, '\n'
            #email_deal(tweet.text)
            if 'hong kong' in tweet.text.lower():
                print 'hong kong found!'
                #email_deal(tweet.text)
                
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(api, listener=myStreamListener())
    myStream.filter(track=['python'])

if __name__ == '__main__':
    #pass in the username of the account you want to download
    args = arg_parser()
    main('thepointsguy')
