#!/usr/bin/python

from bs4 import BeautifulSoup
from imgurpython import ImgurClient
import datetime
import httplib
import os
import sys
import urllib

# Variable initialization and user input
client_id = '59c1b99c1853757';
client_secret = 'e33c8751716b4f4b5d04aa04d957e06289aa1dae';
client = ImgurClient(client_id, client_secret);

subreddit = None;

while not subreddit:
	subreddit = raw_input('Subreddit Name: ');	
directory = raw_input('Image Folder Directory (current directory by default): ');

url_object = urllib.urlopen('https://www.reddit.com/r/' + subreddit);

if url_object.getcode() != 200:
	print("Unable to reach %s..." % subreddit);
	sys.exit();
else:
	print("Connected to https://www.reddit.com/r/" + subreddit + "...");

# Check for existence of specified directory with image folder for today
day = datetime.date.today().day;
month = datetime.date.today().month;
year = datetime.date.today().year;
file_date = str(month) + '_' + str(day) + '_' + str(year);

if directory and directory[0] is '/':
	abs_path = directory;
	if not os.path.exists(directory):
		os.makedirs(directory);
else:
	abs_path = os.path.dirname(os.path.abspath(__file__));

if not os.path.exists(abs_path + '/reddit_' + file_date):
	os.makedirs(abs_path + '/reddit_' + file_date);

# Get image links from subreddit using BeautfiulSoup package
raw_links = [];
img_links= [];
r = url_object.read();
soup = BeautifulSoup(r, 'lxml');
pieces = soup.findAll('p', { 'class' : 'title' });
for piece in pieces:
	raw_links.append(piece.find('a')['href']);

print("Collecting imgur links...");

for link in raw_links:	

	# Check if imgur is in the reddit link's url
	if 'imgur' not in link:		
		continue;	

	file_extension = link.split('.')[-1];

	# Different ways to handle images, image sources, and albums/galleries
	if 'jpg' in file_extension or 'png' in file_extension:		
		img_links.append(link);
	elif 'gallery' in link.split('/') or 'a' in link.split('/'):			
		for index, value in enumerate(link.split('/')):			
			if value == 'gallery' or value == 'a':				
				imgur_album = client.get_album(link.split('/')[index+1]);		
				break;
		images = imgur_album.images;
		for image in images:
			img_links.append(image['link']);
	else:
		imgur_r = urllib.urlopen(link).read();
		imgur_soup = BeautifulSoup(imgur_r, 'lxml');
		imgur_link = imgur_soup.find('div', { 'class' : 'post-image' }).find('a')['href'];										
		if '//i.imgur.com' in imgur_link:				
			img_links.append('https:' + imgur_link);

		
# Iterate through compiled list of links to save and name images
img_number = 0;

print('Saving images to your computer...');

for img_link in img_links:
	file_extension = img_link.split('.')[-1];
	if 'jpg' in file_extension or 'png' in file_extension:
		urllib.urlretrieve(img_link, abs_path + '/reddit_' + file_date + '/' + subreddit + '_' + str(img_number) + '.' + file_extension);
		img_number += 1;

print('Process Complete!');
