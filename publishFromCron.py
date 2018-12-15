#!/usr/bin/python

####
##
## publishFromCron.py: publish a project by specifying the project name as a sys.argv argument; cron-friendly
## Created by: Fredrik Walloe
## Creation date: 15-12-2018
## Version: 1
## Status: works fine without known errors
##
## Usage: ./publishFromCron.py someProjectNameInOneWord
##
####

#### IMPORTS ####
import sys
from publishToTwitter import  publishToTwitter

#### VARIABLES ####
debugMode = False

#### FUNCTIONS ####

# prints text passed to it when debugMode is set to True
def debug(text):
   if debugMode is True:
       print(text)

#### MAIN ####
publishToTwitter(sys.argv[1])
