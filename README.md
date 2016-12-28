# tpg_tweepy
parse @thepointsguy for deal alerts

prerequisites: 

1. generate twitter api keys 
    1. https://apps.twitter.com/
    2. create new app
    3. find your new consumer key
    4. find your new consumer secret
2. fill a configuration file with the format shown in tpg_dealalerts.empty.conf
3. pip install -r requirements.txt

usage: ./tpg_dealalerts_clean.py -c conf_file

tpg_dealalerts_stream.py is a work in progress and is the obvious evolution of this idea
