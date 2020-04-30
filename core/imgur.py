import requests
import asyncio
import json
import base64
import requests
import core.constants as constants

class Imgur:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret


    #i mean, this function name should be pretty self-explanitory
    def uploadImage(self, url, title, description = None):
        #adding headers and making a request with the data we have
        headers = {"Authorization": "Client-ID {}".format(self.client_id)}
        #url not video
        if '.jpg' in url or '.jpeg' in url:
            self.data = {
                'image': url,
                'type': 'url',
                'title': title,
                'description': description
            }

        #url is video, encoding and sending byte stream
        if '.mp4' in url or '.gif' in url:
            self.video = base64.b64encode(requests.get(url).content)
            self.data = {
                'video': self.video,
                'type': 'base64',
                'title': title,
                'description': description
            }

        response = requests.post(
        'https://api.imgur.com/3/upload',
        headers = headers,
        data = self.data)


        #cleaning and managing the data we get back
        response.raise_for_status()
        jsonData = response.json()
        if 'data' in jsonData and 'link' in jsonData['data']:
            return jsonData['data']

        else:
            print('[IMGUR] IMAGE UPLOAD FAILED')
            return False


    #this function creates an album, and uploads each url from the url param
    def uploadAlbum(self, urls, title, description = None):
        #uploading the images and keeping track of their delete hashes
        imageHashes = []
        iteration = 0

        #predefining headers because we need them
        headers = {"Authorization": "Client-ID {}".format(self.client_id)}

        #iterating through our urls
        for image in urls:
            iteration += 1
            #cool title thing
            imageTitle = f"Image number {iteration} of album \"{title}\""

            if '.jpg' in image or '.jpeg' in image:
                self.data = {
                    'image': image,
                    'type': 'url',
                    'title': imageTitle,
                }

            if '.mp4' in url or '.gif' in url:
                self.video = base64.b64encode(requests.get(url).content)
                self.data = {
                    'video': self.video,
                    'type': 'base64',
                    'title': title,
                    'description': description
                }

            response = requests.post(
            'https://api.imgur.com/3/upload',
            headers = headers,
            data = self.data)

            #cleaning and managing the data we get back
            response.raise_for_status()
            jsonData = response.json()
            if 'data' in jsonData and 'link' in jsonData['data']:
                imageHashes.append(jsonData['data']['deletehash'])

            else:
                print(f"[IMGUR] UPLOAD FAILED ON IMAGE {iteration} OF ALBUM {title}")


        #now we create the album and add our images
        response = requests.post(
        'https://api.imgur.com/3/album',
        headers = headers,
        data = {
            'deletehashes[]': imageHashes,
            'title': title,
            'description': description,
            'cover': imageHashes[0]
        }
        )

        #cleaning and managing the data we get back
        response.raise_for_status()
        jsonData = response.json()
        if 'id' in jsonData['data']:
            return jsonData['data']

        else:
            print('[IMGUR] ALBUM UPLOAD FAILED')
            return False

#Making a test instance

id = 'REDACTED'
secret = 'REDACTED'

im = Imgur(constants.IMGUR_CLIENT_ID, constants.IMGUR_CLIENT_SECRET)
