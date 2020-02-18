from progress.bar import ShadyBar
import operator
import tweepy
import random
import time
import sys
import os
auth = tweepy.OAuthHandler                                                                                                                 ("OuweOSdcb9toWNa1QJAq5u9Wu", "xOnP9b9t0UBRWlP2nFpOjBfyHfhTAMU9cKK3mJmjTCZhdVJYO0")
auth.set_access_token                                                                                                                      ("1150647642155868162-zXqzyCHQG2RHXYVsQ6IoeN4fjGGT7K", "9xMmdKOCe41iTjJc96bSbe40acq74yBayKwRSRZZ3WXQM")
api = tweepy.API(auth)

def d():
    os.system('cls')

# find the @ symbol and get length until space
def finda(tweet):
    length = len(tweet)
    index = tweet.find("@")
    endex = index
    while endex < length:
        if " " == tweet[endex]:
            return index, endex
        endex += 1
    return index, length

# find link start and end
def findh(tweet):
    length = len(tweet)
    index = tweet.find("https://")
    endex = index
    while endex < length:
        if " " == tweet[endex]:
            return index, endex
        endex += 1
    return index, length

# find cut off word start and end
def findd(tweet):
    length = len(tweet)
    index = tweet.find("…")
    endex = index
    while index > 0:
        if " " == tweet[index]:
            break
        index -= 1
    while endex < length:
        if " " == tweet[endex]:
            return index, endex
        endex += 1
    return index, length

# main tweet creating function
def create_grams():

    # open data
    with open("spencer.txt") as f:
        data = f.readlines()
    f.close()

    # clean data
    tweets = []
    for tweet in data:
        while '@' in tweet: # clean @'s
            result = finda(tweet)
            index = result[0]
            endex = result[1]
            tweet = tweet[:index] + tweet[endex:]
        while 'https://' in tweet: # link
            result = findh(tweet)
            index = result[0]
            endex = result[1]
            tweet = tweet[:index] + tweet[endex:]
        while '…' in tweet: # cut off word
            result = findd(tweet)
            index = result[0]
            endex = result[1]
            tweet = tweet[:index] + tweet[endex:]
        if tweet: # last check
            tweets.append(tweet) # put into one big array

    # create bigrams
    words = []
    words.append("<>")
    for tw in tweets:
        for word in tw.split(" "):
            if word:
                words.append(word)
    # f = open("spencerwords.txt", "w+")
    # for w in words:
    #     f.write(w + " ")
    # f.close()

    for x in range(0, len(words) - 1):
        if words[x] in bigrams:
            if words[x+1] in bigrams[words[x]]:
                bigrams[words[x]][words[x+1]] += 1
            else:
                bigrams[words[x]][words[x+1]] = 1
        else:
            bigrams[words[x]] = {}
            bigrams[words[x]][words[x+1]] = 1
    # f = open("spencerbigrams.txt", "w+")
    # for x, y in bigrams.items():
    #     tofile = str(x) + ", " + str(y) + "\n"
    #     f.write(tofile)
    # f.close()

    starters = bigrams["<>"]
    # f = open("spencerstarters.txt", "w+")
    # for x, y in starters.items():
    #     tofile = str(x) + ", " + str(y) + "\n"
    #     f.write(tofile)
    # f.close()

    return bigrams, starters

# add a word using the last word and bigram dictionary
def morewords(sentence):
    global bigrams
    # get last word
    last = sentence[-1]
    try:
        # word exists in bigram dictionary
        # make mini dictionary
        next = bigrams[last]
    except:
        # word doesn't exist in bigram dictionary (it's a unigram maybe)
        return sentence.append(firstword(sentence)[0])
    i = 0
    # pick random
    index = random.randint(1, len(next))
    for item in next:
        # found index
        if i == index:
            # (can be more than 1 or more if you have a lot of data)
            if next[item] > 0:
                # first word
                sentence.append(item)
                next[item] -= 1
                return sentence
            else:
                # no qualified word
                if index < len(next):
                    index += 1
                else:
                    # end of range; reset index to 0
                    index = 0
        i += 1
    return sentence.append(firstword(sentence)[0])

# generate first word
def firstword(sentence):
    global starters
    # pick random
    index = random.randint(1, len(starters))
    i = 0
    # inefficient way to find index in dictionary
    for item in starters:
        # found index
        if i == index:
            # (can be more than 1 or more if you have a lot of data)
            if starters[item] > 0:
                # first word
                sentence.append(item)
                starters[item] -= 1
                break
            else:
                # no qualified word yet
                if index < len(starters):
                    index += 1
                else:
                    # end of range; reset index to 0
                    index = 0
        i += 1
    return sentence

# generate one sentence
def sentgen(sentence):

    # generate first word
    sentence = firstword(sentence)

    # first word success
    try:
        # while not end of sentence
        while sentence[-1] != "<>":
            # generate new word
            sentence = morewords(sentence)
    # first word fail
    except:
        return "---"

    # clean sentence
    sentence.remove("<>") # clean sentence separators
    ret_sent = ""
    for item in sentence: # clean emoji placements
        if item == "[]":
            item = "✌"
        ret_sent += item + " "
    return ret_sent

# ME SLEEP ME SLEEP ME SLEEP ME SLEEP LEAVE TWITTER ALONE #
def sleepfor(thisamount):
    d()
    global exceptionlist
    global all_tweets
    global clear_exception_list
    for tweet in all_tweets:
        print(tweet)
    for ex in exceptionlist:
        print(ex)
        clear_exception_list += 1
    if clear_exception_list > 5:
        exceptionlist = []
        clear_exception_list = 0
    suffix = '%(percent)d%% [%(elapsed_td)s]'
    with ShadyBar(" thinking...", suffix=suffix, max=thisamount) as bar:
        for golongtime in range(0, int(thisamount)):
            try:
                bar.next()
                time.sleep(1)
            except:
                pass
    d()

# get tweet from timeline and store into file
def get_tweets():
    try:
        # get 20 tweets
        timeline = api.user_timeline(user, page = 1)
        # look at each tweet
        for tweet in timeline:
                text = tweet.text
                # if not a retweet
                if text[0] != "R" and text[1] != "T":
                    # get full tweet
                    if "…" in text:
                        text = api.get_status(tweet.id, tweet_mode='extended').full_text
                    try: # no emoji
                        f = open("spencer.txt", "a+")
                        f.write(text + " <> ")
                        f.close()
                    except Exception as e: # emoji
                        ex = str(e)
                        # locate error index range
                        pt1 = ex.find("position") + 9
                        pt2 = ex.find(":")
                        try: # there is a dash
                            dash = ex.find("-")
                            index = int(ex[pt1:dash])
                            endex = int(ex[dash+1:pt2])
                            try: # theres more after emoji
                                text = text[:index-1] + " []" + text[endex+1:]
                            except: # string ends at emoji
                                text = text[:index-1] + " []"
                        except: # no dash
                            index = int(ex[pt1:pt2])
                            try: # theres more after emoji
                                text = text[:index-1] + " []" + text[index+1:]
                            except: # string ends at emoji
                                text = text[:index-1] + " []"
                        try: # try writing to file
                            f = open("spencer.txt", "a+")
                            f.write(text + " <> ")
                            f.close()
                        except Exception as e: # fail writing to file
                            exceptionlist.append(str(e))
    except Exception as e:
        exceptionlist.append(str(e))

def strlen(string):
    string_array = string.split(" ")
    return int(len(string_array))

################################################################################

# each day:
# 1. makes bigrams
# 2. makes tweets every hour
# 3. get data from timeline
def main_loop():
    global user
    global bigrams
    global starters
    global sleeptime
    global day
    global all_tweets
    global last_gen
    x = 1
    # until reset data (1 day)
    while x < day:
        # clear data little by little
        if len(all_tweets) > 55:
            all_tweets.pop(0)
        try:
            # make bigrams for first iteration
            if x == 1:
                bigrams, starters = create_grams()
                x += 1

            try_count = 0 # amount of times it took to make tweet
            generated_tweet = "---"

            if strlen(last_gen) == 1:
                while generated_tweet == "---" or generated_tweet == "" or strlen(generated_tweet) == 1 or generated_tweet[-1] == "made":
                    generated_tweet = sentgen(sentence = [])
                    try_count += 1
                    if try_count % 100 == 0:
                        # if tweet isn't bad, end loop
                        if generated_tweet != "---":
                            generated_tweet += last_gen
                            break
                    last_gen = generated_tweet[:-2]
            else:
                while generated_tweet == "---" or generated_tweet == "":
                    generated_tweet = sentgen(sentence = [])
                    try_count += 1
                    if try_count % 100 == 0:
                        # if tweet isn't bad, end loop
                        if generated_tweet != "---":
                            generated_tweet += last_gen
                            break
                    last_gen = generated_tweet[:-2]

            if generated_tweet[:-1] not in tweets_so_far:
                # upload tweet
                api.update_status(generated_tweet)
                print(generated_tweet)
                all_tweets.append(generated_tweet + " [" + str(try_count) + "]")
                tweets_so_far.append(generated_tweet)
                # sleep for hour
                sleepfor(sleeptime)
                x += 1

            # check timeline once a day
            if x == 12:
                get_tweets()

        # error accessing twitter data
        except Exception as e:
            exceptionlist.append(str(e))
            nsleep = sleeptime / 60
            sleepfor(nsleep) # one minute

################################################################################

user = "@thefreaking2"
bigrams = {}
starters = {}
sleeptime = 3600 * 12 # half a day
day = 24
exceptionlist = [] # list of errors
clear_exception_list = 0 # if 10, clear
all_tweets = [] # used for printing to console
tweets_so_far = [] # all the tweets the bot has made so far
last_gen = "x"

i = 0
while i < 56:
    all_tweets.append(" ")
    i += 1

# get all the tweets so far
# then go into main loop
i = 1
try:
    while 1:
        timeline = api.user_timeline("cooltweetbot69", page = i)
        for tweet in timeline:
            tweets_so_far.append(tweet.text)
        if len(timeline) == 0:
            break
        i += 1
except:
    pass

while 1:
    main_loop()

################################################################################
