
# coding: utf-8

# In[ ]:

#!/usr/bin/python

import requests
import sys
import datetime
import optparse
import urllib2
from BeautifulSoup import BeautifulSoup
import textwrap
import simplejson as json
import csv
from array import *
api_key = KEY
base_url = "https://eu.api.battle.net/wow/"
guild_name = "Phased"
guild_realm = "Karazhan"

def query_api(url):
    try:
        s = requests.get(url).json()
        pass
    except Exception:
        #raise e
        pass
    try:
        if s["reason"]:
            print "ERROR: " + s["reason"]
            sys.stop()
    except:
        return s
    
def guild_members(guild_name, guild_realm, api_key, base_url):
    req_url = base_url + "guild/" + guild_realm + "/" + guild_name + "?fields=members&locale=en_GB&apikey=" + api_key
    guild_chars_name = []
    guild_chars_level = []
    guild_chars_realm = []
    s = query_api(req_url)
    for i in xrange(1,len(s["members"])):
        ind_names = i-1
        guild_chars_name.append(s["members"][ind_names]["character"]["name"])
        guild_chars_level.append(s["members"][ind_names]["character"]["level"])
        guild_chars_realm.append(s["members"][ind_names]["character"]["realm"])
        
    guild_chars_name, guild_chars_realm = remove_non_max(guild_chars_name, guild_chars_realm, guild_chars_level)
    return guild_chars_name, guild_chars_realm

def remove_non_max(guild_chars_name, guild_chars_realm, guild_chars_level):
    while guild_chars_level.count(110) < len(guild_chars_level):
        for i in xrange(0,len(guild_chars_level)):
            if guild_chars_level[i] != 110:
                del guild_chars_name[i]
                del guild_chars_realm[i]
                del guild_chars_level[i]
                break
                
    remove_non_max(guild_chars_name, guild_chars_realm, guild_chars_level)
    return guild_chars_name, guild_chars_realm


# In[ ]:



