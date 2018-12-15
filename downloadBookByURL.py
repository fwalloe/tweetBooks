#!/usr/bin/python

####
##
## downloadBookByURL.py: downloads a text and saves it to file
## Created by: Fredrik Walloe
## Creation date: 14-12-2018
## Version: 1.0
## Status: works as expected with no known errors, but there are some static values that should be set by sys.argv 
##
## Usage: use tweetBooks.py -d to download a file 
##
####

#### IMPORTS ####
import requests
import os

#### VARIABLES ####
debugMode = False

#### FUNCTIONS ####

# prints text passed to it when debugMode is set to True
def debug(text):
   if debugMode is True:
       print(text)

#### MAIN ####
def downloadByURL(projectName, URL):
    url = URL
    response = requests.get(url)

    fileName = "unparsed" + projectName + "/" + projectName + ".txt"

    # create the path if neccessary
    os.makedirs(os.path.dirname(fileName), exist_ok=True)

    # place the project in a separate folder
    with open(fileName, "w+") as f:
        f.write(response.text)
