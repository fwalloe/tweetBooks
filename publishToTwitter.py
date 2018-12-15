#!/usr/bin/python

####
##
## publishToTwitter.py: gets a prepared tweet from file, logs into a Twitter account, publishes the tweet and then writes the tweet number to file
## Created by: Fredrik Walloe
## Creation date: 14-12-2018
## Version: 1.0
## Status: works as expected with no known errors
##
## Usage: after running downloadBookByURL.py and fitTextInTweets.py, publishToTwitter.py can be used to publish the tweets to twitter
##
####

#### IMPORTS ####
import requests         # used to send tweets to Buffer, which then forwards the tweets to Twitter 
import re               # used to find the tweet number
import datetime         # used when writing to a log that keeps track of whether publications have been successful. 
import sys              # used to quit if the file that should be read from cannot be found

#### VARIABLES ####
debugMode = False
lineReached = 0
tweet = ""

clientID = ""                       # Buffer client ID, which can be found under 'registered apps' after you create an application
clientSecret = ""           # Buffer client Secret, which will be sent by email after you create an application
redirectURI = ""                   # Buffer redirect, which can be found under 'registered apps' after you create an application; a default redirect was used here
bufferToken = ""          # Buffer Token, which can be found under 'registered apps' after you create an application; if you need more than one a separate authentication process is required          
bufferProfileID = ""

#### FUNCTIONS d####

# prints text passed to it when debugMode is set to True
def debug(text):
   if debugMode is True:
       print(text)

def publishToTwitter(projectName):
    # As the script is intended to be run hourly / daily it makes sense to save the progress to file
    getLineReached = open(projectName + "/lineReached", "r")

    for line in getLineReached:
        lineReached = line.strip().replace("\n", "")

    # Tweets are retrieved from this file 
    try:
        getTweet = open(projectName + "/" + projectName + ".txt", "r")
    except: 
        print("Failed to open file that should contain the parsed tweets for this project. If you have not yet used to --download and --fit options, use those first and then try this option again. If yout've already run those options, verify that you entered the correct project name (note that project names are case-sensitive.")
        sys.exit(1)

    # loop through each of the prepared tweets 
    for line in getTweet:
        if line.strip():

            # Each tweet is numbered in the format (somenumber/).  
            tweetNumberPattern = r'(\(\d*\/\))'
            tweetNumber = re.findall(tweetNumberPattern, line)
            tweetNumber = str(tweetNumber).split("/)")[0].split("(")[-1].strip()
            
            # find the 
            if int(lineReached) == int(tweetNumber):
                debug(line)
                tweet = line
                break

    """
        Buffer requires you to a) create an account b) create an application, c) get a token (requires a separate GET request if you need more than one) and d) the information below supplied as data in the POST request: 
        - a profile ID (found in the URL on your Buffer profile)
        - the text that should be shared; a tweet in this case
        - 'now' is optional and means that the tweet will be shared immediately
        - client ID, which can also be found after creating an 
    """
    data = {"profile_ids": bufferProfileID, "text": tweet, "now": 'now', "client_id": clientID,
                "client_secret": clientSecret,
                "redirect_uri": redirectURI,
                "access_token": bufferToken
    }

    # buffer also requires that the content-type is set like this
    headers = {"Content-Type": "application/x-www-form-urlencoded"}



    # connect to Buffer and publish the tweet
    response = requests.post('https://api.bufferapp.com/1/updates/create.json', headers = headers, data = data)

    # change debugMode to True to print these
    debug(response)
    debug(response.text)
    debug(response.reason)
    debug(response.status_code)
    debug(response.cookies)

    # write the last line to file
    with open(projectName + "/lineReached", "w") as f:
        # only update lineReached if the attempt to publish the tweet succeeded 
        if str(200) in str(response.status_code):
            lineReached = int(lineReached) + 1                # because the tweet was published the last reach tweet value should increment by one
            f.write(str(lineReached))


    # keep a log of successful / unsuccesful attempts to tweet; can be used to figure out when a problem occurred. 
    with open("publicationLog.txt", "a") as f:
        now = datetime.datetime.now()
        print(response.status_code)
        if str(200) in str(response.status_code):
            f.write(str(now.day) + "/" + str(now.month) + "/" + str(now.year) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + " -> published tweet successfully\n")
        else:
            f.write(str(now.day) + "/" + str(now.month) + "/" + str(now.year) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + " -> failed to publish tweet\n")



