#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import sys
from datetime import datetime
import time
import optparse
import urllib2
from BeautifulSoup import BeautifulSoup
import textwrap
import simplejson as json
import csv
from array import *

api_key = "yh5pnbmtfqmhhh675gtrvnfn2at6x4xk"
#keyfile = open("api_key", "r")
#api_key = keyfile.read()

base_url = "https://eu.api.battle.net/wow/"

guild_name = "Phased"
guild_realm = "Karazhan"

dungeon_ids = ([1, "Heroic" ],
[2, "Mythic" ],
[4, "Heroic" ],
[5, "Mythic" ],
[7, "Heroic" ],
[8, "Mythic" ],
[10, "Heroic" ],
[11, "Mythic" ],
[14, "Heroic" ],
[15, "Heroic" ],
[16, "Mythic" ],
[17, "Mythic" ],
[19, "Heroic" ],
[20, "Mythic" ],
[22, "Heroic" ],
[23, "Mythic" ],
[25, "Heroic" ],
[26, "Mythic" ],
[27, "Mythic" ],
[28, "Mythic" ],
[29, "ENlfr" ],
[30, "ENnormal" ],
[31, "ENheroic" ],
[32, "ENmythic" ],
[33, "ENlfr" ],
[34, "ENnormal" ],
[35, "ENheroic" ],
[36, "ENmythic" ],
[37, "ENlfr" ],
[38, "ENnormal" ],
[39, "ENheroic" ],
[40, "ENmythic" ],
[41, "ENlfr" ],
[42, "ENnormal" ],
[43, "ENheroic" ],
[44, "ENmythic" ],
[45, "ENlfr" ],
[46, "ENnormal" ],
[47, "ENheroic" ],
[48, "ENmythic" ],
[49, "ENlfr" ],
[50, "ENnormal" ],
[51, "ENheroic" ],
[52, "ENmythic" ],
[53, "ENlfr" ],
[54, "ENnormal" ],
[55, "ENheroic" ],
[56, "ENmythic" ],
[57, "NHlfr" ],
[58, "NHnormal" ],
[59, "NHheroic" ],
[60, "NHmythic" ],
[61, "NHlfr" ],
[62, "NHnormal" ],
[63, "NHheroic" ],
[64, "NHmythic" ],
[65, "NHlfr" ],
[66, "NHnormal" ],
[67, "NHheroic" ],
[68, "NHmythic" ],
[69, "NHlfr" ],
[70, "NHnormal" ],
[71, "NHheroic" ],
[72, "NHmythic" ],
[73, "NHlfr" ],
[74, "NHnormal" ],
[75, "NHheroic" ],
[76, "NHmythic" ],
[77, "NHlfr" ],
[78, "NHnormal" ],
[79, "NHheroic" ],
[80, "NHmythic" ],
[81, "NHlfr" ],
[82, "NHnormal" ],
[83, "NHheroic" ],
[84, "NHmythic" ],
[85, "NHlfr" ],
[86, "NHnormal" ],
[87, "NHheroic" ],
[88, "NHmythic" ],
[89, "NHlfr" ],
[90, "NHnormal" ],
[91, "NHheroic" ],
[92, "NHmythic" ],
[93, "NHlfr" ],
[94, "NHnormal" ],
[95, "NHheroic" ],
[96, "NHmythic" ])

def query_api(url):
    print url
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

def get_lockouts(guild_chars_name, guild_chars_realm, api_key, base_url):
    char_dungeon_lockouts = []

    for i in xrange(1,len(guild_chars_name)):
        req_url = base_url + "character/" + guild_chars_realm[i] + "/" + guild_chars_name[i] + "?fields=statistics&?locale=en_GB&apikey=" + api_key

        s = query_api(req_url)
        STATS_RAIDS = 5
        STATS_LEGION_RAIDS = 6
        char_dungeon_lockouts.append(s["statistics"]["subCategories"][STATS_RAIDS]["subCategories"][STATS_LEGION_RAIDS]["statistics"])

    return char_dungeon_lockouts

def get_expiry_time(char_dungeon_lockouts, dungeon_ids):

    current_time = int(time.time()) #current unix time
    current_time_utc = datetime.utcnow()
    current_hour = current_time_utc.hour
    current_day = time.strftime("%w") #current day -- 0 = sunday
    # start current_day on Wednesday
    if int(current_day) < 3:
        current_day = int(current_day) + 5
    else:
        current_day = int(current_day) - 3

    # get time until next 7AM UTC
    if current_hour < 7:
        reset_time = date(current_time_utc.year, current_time_utc.month, current_time_utc.day) + 3600*7
        time_remaining = reset_time - int(time.mktime(reset_time.timetuple())) #seconds
    else:
        days_till_reset = current_time_utc.day + (7 - int(current_day))
        hours_till_reset = 7 - current_time_utc.hour
        minutes_till_reset = current_time_utc.minute

        time_remaining = (((hours_till_reset) * 60) + minutes_till_reset) * 60 #seconds

    day_reset = time_remaining
    week_reset = time_remaining + (7 - int(current_day))*(24 * 60 * 60)

    print day_reset
    print week_reset

    for i in xrange(0,len(char_dungeon_lockouts)):
        for j in xrange(0,len(dungeon_ids)):
            s = char_dungeon_lockouts[i][j]["lastUpdated"]
            lockout_remaining = []
            if s == 0:
                lockout_remaining.append("Expired")
            elif dungeon_ids[j][1].find("heroic") | dungeon_ids[j][1].find("Heroic"):
                lockout_remaining.append(day_reset)
            elif dungeon_ids[j][1].find("mythic") | dungeon_ids[j][1].find("Mythic"):
                lockout_remaining.append(week_reset)
            else:
                print "Error with dungeon difficulty."

    return lockout_remaining

def save_to_txt(guild_chars_name, guild_chars_professions1, guild_chars_professions2):
    f = open('guild_profs.csv', 'w')

    for i in xrange(0,len(guild_chars_name)):
        s = guild_chars_name[i] + ', ' + guild_chars_professions1[i] + ', ' + guild_chars_professions2[i] + '\n'
        f.write(s.encode('utf8'))

    f.close()

guild_chars_name, guild_chars_realm = guild_members(guild_name, guild_realm, api_key, base_url)
char_dungeon_lockouts = get_lockouts(guild_chars_name, guild_chars_realm, api_key, base_url)
expiry_times = get_expiry_time(char_dungeon_lockouts, dungeon_ids)

print expiry_times

#save_to_txt(guild_chars_name, guild_chars_professions1, guild_chars_professions2)
