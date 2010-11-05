#!/usr/bin/env python
# downloads picasa web albums
import gdata.photos.service
import gdata.media
import gdata.geo

import settings

gd_client = gdata.photos.service.PhotosService()
gd_client.email = settings.email
gd_client.password = settings.password
gd_client.source = 'exampleCo-exampleApp-1'
gd_client.ProgrammaticLogin()
