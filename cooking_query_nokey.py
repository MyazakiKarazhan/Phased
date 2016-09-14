
# coding: utf-8

# In[25]:

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
    for i in xrange(0,len(s["members"])):
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

def checkRecipeName(api_key, base_url, recipe_id):
    req_url = base_url + "recipe/" + str(recipe_id) + "?locale=en_GB&apikey=" + api_key
    
    recipe = query_api(req_url)
    
    try:
        if recipe["profession"] == "Cooking":
            return recipe["name"]
        else:
            return "Non-Cooking Recipe"
    except Exception:
        return "Non-Cooking Recipe"
    
def getPlayerRecipes(api_key, base_url, player_name, player_realm):
    req_url = base_url + "character/" + player_realm + "/" + player_name + "?fields=professions&locale=en_GB&apikey=" + api_key

    s = query_api(req_url)
    
    cooking_id = 0
    for i in xrange(0, len(s["professions"]["secondary"])):
        if s["professions"]["secondary"][i]["name"] == "Cooking":
            cooking_id = i
    
    s = s["professions"]["secondary"][cooking_id]["recipes"]
    
    for i in xrange(0,len(s)):
        if int(s[i]) > 200000:
            s[i] = checkRecipeName(api_key, base_url, s[i])
        else:
            s[i] = "Non-Cooking Recipe"
    
    return s

def populateGuildRecipeList(new_recipes, player_name, recipe_list):
    player_name = player_name.encode('utf-8')
    inds = [i for i, x in enumerate(new_recipes) if x == "Non-Cooking Recipe"]
    for i in sorted(inds, reverse=True):
        del new_recipes[i]
        
    for i in xrange(0,len(new_recipes)):
        try:
            ind_recipe = recipe_list[0].index(new_recipes[i])
            recipe_list[1][ind_recipe] = recipe_list[1][ind_recipe] + ", " + player_name
        except Exception:
            recipe_list[0].append(new_recipes[i])
            recipe_list[1].append(player_name)
    
    return recipe_list

def save_to_txt(recipe_save):
    try:
        os.remove("guild_cooking.csv")
    except Exception:
        pass
    
    f = open('guild_cooking.csv', 'w')

    for i in xrange(0,len(recipe_save)):
        s = recipe_save[i]
        f.write(s)

    f.close()
    
guild_chars_name, guild_chars_realm = guild_members(guild_name, guild_realm, api_key, base_url)

recipe_list = []
recipe_list.append([])
recipe_list.append([])

for i in xrange(0,3):#len(guild_chars_name)):
    new_recipes = getPlayerRecipes(api_key, base_url, guild_chars_name[i], guild_chars_realm[i])
    recipe_list = populateGuildRecipeList(new_recipes, guild_chars_name[i], recipe_list)
    print "Finished: " + guild_chars_name[i].encode('utf-8') + " (" + str(i+1) + " of " + str(len(guild_chars_name)) + ")"

recipe_save = []

for i in xrange(0, len(recipe_list[0])):
    recipe_name = str(recipe_list[0][i])
    recipe_chars = str(recipe_list[1][i])
    save_line = recipe_name + ", " + recipe_chars + "\n"
    recipe_save.append(save_line)
    
save_to_txt(recipe_save)

