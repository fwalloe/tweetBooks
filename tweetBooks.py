#!/usr/bin/python

####
##
## tweetBooks.py: a command-line interface for downloading a text, parsing it into tweet-form and publishing the tweets
## Created by: Fredrik Walloe
## Creation date: 15-12-2018
## Version: 1.0
## Status: works fine with no known errors
##
## Usage: N/A
##
####

#### IMPORTS ####
import argparse
import sys
from downloadBookByURL import downloadByURL
from fitTextInTweets import fitTextToTweet
from publishToTwitter import  publishToTwitter

#### VARIABLES ####
debugMode = False

#### FUNCTIONS ####

# prints text passed to it when debugMode is set to True
def debug(text):
   if debugMode is True:
       print(text)

#### MAIN ####

parser = argparse.ArgumentParser(description='Publish a Text Tweet-by-Tweet')

parser.add_argument('-d', '--download', action='store_true', help = "Download a text")

parser.add_argument('-f', '--fit', action='store_true', help = "Parse a text to make it fit a tweet")

parser.add_argument('-p', '--publish', action='store_true', help = "Publish the next tweet")

args = parser.parse_args()



if (args.download):
    projectName = input("Choose a project name: ")
    URL = input("Provide URL that the text should be downloaded from: ")

    downloadByURL(projectName.strip(), URL.strip())

if (args.fit):
    projectName = input("Specify an existing project that should be parsed: ")
    hashtag = input("Choose a hashtag (without the #): ")

    filePath = projectName + "/" + projectName + ".txt"
    print(filePath)
    fitTextToTweet(filePath, hashtag)

if (args.publish):
    areCredentialsSet = input("Have you created a Buffer account and manually set Buffer credentials in publishToTwitter.py?\n1. Yes\n2. No\n") 
    if str("1") in areCredentialsSet:
        projectName = input("Specify the name of an existing project to publish the next pending tweet for that project: ")
        publishToTwitter(projectName)

    else: 
        print("Sort that out first and then come back here")
        sys.exit(1)
    

