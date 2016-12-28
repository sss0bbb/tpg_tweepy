#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Twitter API credentials
consumer_key = "NnvZB9intluuf1fsgz1asKA6p"
consumer_secret = "dy8iKVYM449hbY3PXfhgNmXtrfkMjn88ZLWsYlNnWr4BcAf3nH"
access_key = ""
access_secret = ""

email_server = smtplib.SMTP('smtp.gmail.com', 587)
email_user = 'sssbbb@gmail.com'
email_pass = 'gmhzqlmrjsweerco'
email_recipients = ['sssbbb@gmail.com', 'Anthony.Pernasilice@exeloncorp.com']


def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    api = twitter_auth()
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print "...%s tweets downloaded so far" % (len(alltweets))
    
    #parse out tweets not containing special text
    for tweet in alltweets:
        if text_parse(tweet.text):
            print 'deal found!\n', 'created:', tweet.created_at, '\n', tweet.text, '\n'
            #email_deal(tweet.text)
            if 'hong kong' in tweet.text.lower():
                email_deal(tweet.text)
            
    #transform the tweepy tweets into a 2D array that will populate the csv    
    #outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    #write the csv    
    #write_csv(outtweets)
    
    pass

def twitter_auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return tweepy.API(auth)

def text_parse(text):
    if 'deal' in text.lower() and '$' in text.lower():
        return True
    else:
        return False

def email_deal(text):
    msg = MIMEText(text.encode("utf-8"))
    msg['Subject'] = 'SB test: Airfare Deal Found!'
    msg['From'] = email_user
    msg['To'] = ','.join(email_recipients)
    
    email_server.starttls()
    email_server.login(email_user, email_pass)
    email_server.sendmail(email_user, email_recipients, msg.as_string())
    email_server.quit

def write_csv(screen_name, tweets):
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(tweets)

if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets('thepointsguy')
