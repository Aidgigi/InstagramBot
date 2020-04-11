import requests
import asyncio
import json
#import constants
#import constants

class imgur:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret


    #i mean, this function name should be pretty self-explanitory
    async def uploadImage(self, url, title, description = None):
        #adding headers and making a request with the data we have
        headers = {"Authorization": "Client-ID {}".format(self.client_id)}
        response = requests.post(
        'https://api.imgur.com/3/upload',
        headers = headers,
        data = {
            'image': url,
            'type': 'url',
            'title': title,
            'description': description
        }
        )

        #cleaning and managing the data we get back
        response.raise_for_status()
        jsonData = response.json()
        if 'data' in jsonData and 'link' in jsonData['data']:
            return jsonData['data']

        else:
            print('[IMGUR] IMAGE UPLOAD FAILED')


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
            imageTitle = f"Image number {iteration} of album {title}"

            response = requests.post(
            'https://api.imgur.com/3/upload',
            headers = headers,
            data = {
                'image': image,
                'type': 'url',
                'title': imageTitle,
            }
            )

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
        if 'id' in jsonData:
            return jsonData['id']

        else:
            print('[IMGUR] ALBUM UPLOAD FAILED')

#Making a test instance

id = 'REDACTED'
secret = 'REDACTED'


im = imgur(id, secret)
