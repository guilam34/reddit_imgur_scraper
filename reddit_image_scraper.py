#!/usr/bin/python

from bs4 import BeautifulSoup
from imgurpython import ImgurClient
import datetime
import httplib
import os
import urllib

# Variable initialization and user input
client_id = '59c1b99c1853757';
client_secret = 'e33c8751716b4f4b5d04aa04d957e06289aa1dae';
client = ImgurClient(client_id, client_secret);

subreddit = None;

while not subreddit:
	subreddit = raw_input('Subreddit Name: ');	
directory = raw_input('Image Folder Directory (current directory by default): ');

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
r = urllib.urlopen('https://www.reddit.com/r/' + subreddit).read();
soup = BeautifulSoup(r, 'lxml');
links = soup.findAll('p', { 'class' : 'title' });
img_links = [];

for link in links:
	img_href = link.find('a')['href'];

	# Check if imgur is in the reddit link's url
	if 'imgur' not in img_href:		
		continue;	

	file_extension = img_href.split('.')[-1];

	# Different ways to handle images, image sources, and albums/galleries
	if 'jpg' in file_extension or 'png' in file_extension:		
		img_links.append(img_href);
	elif 'gallery' in img_href.split('/') or 'a' in img_href.split('/'):			
		imgur_album = client.get_album(img_href.split('/')[-1]);		
		images = imgur_album.images;
		for image in images:
			img_links.append(image['link']);
	else:
		imgur_r = urllib.urlopen(img_href).read();
		imgur_soup = BeautifulSoup(imgur_r, 'lxml');
		imgur_link = imgur_soup.find('div', { 'class' : 'post-image' }).find('a')['href'];										
		if '//i.imgur.com' in imgur_link:				
			img_links.append('https:' + imgur_link);

		
# Iterate through compiled list of links to save and name images
img_number = 0;

for img_link in img_links:
	file_extension = img_link.split('.')[-1];
	if 'jpg' in file_extension or 'png' in file_extension:
		urllib.urlretrieve(img_link, abs_path + '/reddit_' + file_date + '/' + subreddit + '_' + str(img_number) + '.' + file_extension);
		img_number += 1;
