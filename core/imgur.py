import requests
import pyimgur

class imgur:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

        #I know, wrapping an object in an object is stupid,
        #but I'm doing this keep the code clean. You should honestly thank me.
        self.imgurOb = pyimgur.Imgur(self.client_id, client_secret = self.client_secret)

    def uploadImage(self, title)
