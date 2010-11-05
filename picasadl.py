#!/usr/bin/env python
# downloads picasa web albums
import urllib
import os
import os.path

import gdata.photos.service
import gdata.media
import gdata.geo

def show_progress(count, block_size, total_size):
	completed = (float(count) * float(block_size)) / float(total_size)
	if completed > 1.0:
		completed = 1.0
	print "%0.1f percent complete" % (completed * 100.0)

class Photo:
	def __init__(self, photo, album, gd_client=None):
		self.photo = photo
		self.album = album
		
		self.gd_client = gd_client

		self.url = self.photo.content.src
		self.title = self.photo.title.text
		self.gphoto_id = self.photo.gphoto_id.text
	
	def __str__(self):
		return "%s" % self.title

	def download(self, destination=None):
		destination = os.getcwd() + '/' + destination + '/%s/%s' % (self.album.title, self.title)

		try:
			if not os.path.isdir(os.path.dirname(destination)):
				os.makedirs(os.path.dirname(destination))
			urllib.urlretrieve(self.url, destination, show_progress)
		except Exception as e:
			print e
			print "unable to download %s" % self

class Album:
	def __init__(self, album, gd_client=None):
		self.album = album

		self.gd_client = gd_client

		self.title = self.album.title.text
		self.numphotos = int(self.album.numphotos.text)
		self.gphoto_id = self.album.gphoto_id.text
	
	def __str__(self):
		ending = ''
		if self.numphotos != 1:
			ending = 's'

		return "%s (contains %i photo%s)" % (self.title, self.numphotos, ending)

	def download(self, destination=None):
		if self.gd_client is None:
			return False
		for photo in self.photos():
			photo.download(destination)

	def photos(self):
		if self.gd_client is None:
			return
		photos = self.gd_client.GetFeed(
				'/data/feed/api/user/default/albumid/%s?kind=photo' % 
				(self.gphoto_id))
		for photo in photos.entry:
			 yield Photo(photo, self, self.gd_client)

class PicasaDownloader:
	def __init__(self, email, password, source='picasadl'):
		self.email = email
		self.password = password
		self.source = source

		self.gd_client = gdata.photos.service.PhotosService()
		self.gd_client.email = self.email
		self.gd_client.password = self.password
		self.gd_client.source = self.source
		self.gd_client.ProgrammaticLogin()
	
	def get_albums(self, user=None):
		if user is None:
			user = self.email
		albums = self.gd_client.GetUserFeed(user=user)
		for album in albums.entry:
			yield Album(album, self.gd_client)

	def download_albums(self, user=None, destination=''):
		if user is None:
			user = self.email
		for album in self.get_albums(user):
			album.download(destination)

def main():
	import settings
	from pprint import pprint

	downloader = PicasaDownloader(settings.email, settings.password)

	for album in downloader.get_albums():
		album.download('photos')

if __name__ == "__main__":
	main()
