import urllib2
from bs4 import BeautifulSoup
import json
from pprint import pprint
import requests
import subprocess
import os
import time

show_num = {}
ws = "%20"
with open('shows.json') as data_file:    
    data = json.load(data_file)
    show_num = {}

for x in data:
	show = x.replace(" ", "+")
	season = int(data[x]["season"])
	episode = int(data[x]["episode"])
	quality = data[x]["quality"]
	release = data[x]["release"]
	s = str(season)
	e = str(episode)
	if season < 10:
		s = "0"+s
	if episode < 10:
		e = "0"+e
	x = "s"+s+"e"+e

	if season == 0:
		x = time.strftime("%Y/%m/%d").replace("/", ".")

	pirate = "https://thepiratebay.org/search/{}+{}+{}+{}/0/99/208".format(show, x, quality, release)
	headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
	hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
	       #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
	req = urllib2.Request(pirate, headers=hdr)
	response = urllib2.urlopen(req)
	soup = BeautifulSoup(response, "html.parser")

	link_found = False
	for link in soup.find_all('a', href=True):
		if "magnet" in link['href']:
			link_found = link['href']
			#print link_found

	if link_found:
		os.startfile(link_found)
		episode += 1
		show_num[show] = episode

if len(show_num) > 0:
	with open("shows.json", "r+") as jsonFile:
	    data = json.load(jsonFile)

	    for x in show_num:
	    	sh = x.replace("+", " ")
	    	data[sh]["episode"] = show_num[x]

	    jsonFile.seek(0)  # rewind
	    jsonFile.write(json.dumps(data))
	    jsonFile.truncate()



