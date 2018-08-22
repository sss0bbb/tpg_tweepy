# tpg_tweepy
### parse @thepointsguy for deal alerts
### I would be very surprised if there aren't 1000 things that do this already. Much of this is for personal practice working with tweepy and storing tweets to file as json

prerequisites: 

1. generate twitter api keys 
    1. https://apps.twitter.com/
    2. create new app
    3. find your new consumer key
    4. find your new consumer secret
2. fill a configuration file with the format shown in tpg_dealalerts.sample.conf
3. pip install -r requirements.txt

**usage**: tpg_dealalerts_clean.py [-h] -c config_file -d db_file [-e]

twitter flight deal notifier

optional arguments:
  * -h, --help  show this help message and exit
  * -c CONFIG   required configuration file for connecting to twitter api and
              optionally sending email
  * -d DB       json db file (optional)
  * -e          send email (optional)

#### tpg_dealalerts_clean.py is more of a finished product
#### tpg_dealalerts_stream.py is a work in progress and is the obvious evolution of this idea
