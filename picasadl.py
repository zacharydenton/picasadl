#!/usr/bin/env python
# downloads picasa web albums
import gdata.photos.service
import gdata.media
import gdata.geo

class Album:
	def __init__(self, gd_client=None, title="Untitled", numphotos=0, picasa_id=None):
		self.gd_client = gd_client
		self.title = title
		self.numphotos = int(numphotos)
		self.picasa_id = picasa_id
	
	def __str__(self):
		ending = ''
		if self.numphotos != 1:
			ending = 's'

		return "%s (contains %i photo%s)" % (self.title, self.numphotos, ending)

	def download(self, location=None):
		if self.gd_client is not None:
			return True
		else:
			return False

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
		results = []
		for album in albums.entry:
			results.append(Album(self.gd_client, album.title.text, album.numphotos.text, album.gphoto_id.text))
		return results

	def download_albums(self, user=None, location=''):
		if user is None:
			user = self.email
		albums = self.get_albums(user)
		for album in albums:
			album.download(location)

def main():
	import settings

	downloader = PicasaDownloader(settings.email, settings.password)

	for album in downloader.get_albums():
		if album.download():
			print album

if __name__ == "__main__":
	main()
