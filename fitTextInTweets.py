#!/usr/bin/python

####
##
## fitTextInTweets.py: parse a text into tweets
## Created by: Fredrik Walloe
## Creation date: 14-12-2018
## Version: 1.0
## Status: works as expected with no known errors
##
## Usage: run tweetBooks --fit and follow the instructions
##
####

#### IMPORTS ####
import sys

#### VARIABLES ####
debugMode = False

#### FUNCTIONS ####

# prints text passed to it when debugMode is set to True
def debug(text):
   if debugMode is True:
       print(text)

def fitTextToTweet(filePath, hashtag):

    # Loop through the file

    try:   
        text = open(filePath.replace("/", "/unparsed"), "r")        # the unparsed text was downloaded to a file located in projectName/unparsedProjectName
    except:
        print("Unable to open project file. Make sure you specified an existing project or use the --download option to create a new project. Project names are case-sensitive")
        sys.exit(1)

    tweets = []             # save tweets to a list
    i = 1                   # the tweet number
    lastLine = ""           # when a line must be cut down to fit into a tweet, the cut words are stored in this variable
        
    # loop through the text and make each line fit into a tweet
    for line in text:
   
        # if the line is not empty
        if str(line).strip():

            line = lastLine + " " + line # text that didn't fit in the last tweet should be part of the next tweet
     
            lastLine = ""
            line = line.replace("\n", "").strip()     # weird spacing doesn't work in tweet-form        
            line = line.replace("  ", " ") # if mashing up lastLine and line together introduces and extra space
            line = line.replace("   ", " ") # if mashing up lastLine and line together introduces and extra space
            line = line.replace("    ", " ") # if mashing up lastLine and line together introduces and extra space

            # if it's longer than 120 characters it's neccessary to manipulate it to make it fit a tweet
            if len(line) > 120:
                        
                # see if it's enough to cut one word
                while len(line) > (140 - len(hashtag) - len(str(5)) - len(str(i))):    # to figure out how many characters we can fit into a tweet we must take the max tweet length of 140 characters, minus the hashtag, tweet number and the three charactes used to encapsulate the tweet number plus two spaces
                    
                    # Save the last word
                    lastLine = line.rsplit(' ', 1)[1] + " " + lastLine    

                    # keep the line minus the last word
                    line = line.rsplit(' ', 1)[0]

            elif str("the end") in line.lower():
                tweets.append(line + " (" + str(i) + "/) #" + hashtag + "\n")
                

            # very short sentences can be annoying too
            elif len(line) < 60:
                lastLine = line

            # can fit in a tweet as-is
            else:
                debug("Tweet ready: " + line + " (" + str(i) + "/) #" + hashtag)
                tweets.append(line + " (" + str(i) + "/) #" + hashtag + "\n")
                i += 1
                   

    for tweet in tweets:
        print(tweet.replace("\n", ""))


    with open(filePath, "w+") as f:
        for tweet in tweets:
            f.write(tweet)


