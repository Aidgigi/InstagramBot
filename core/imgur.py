import requests
import pyimgur
#import constants

class imgur:
    def __init__(self, client_id, client_secret, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token

        #I know, wrapping an object in an object is stupid,
        #but I'm doing this keep the code clean. You should honestly thank me.
        self.imgurInstance = pyimgur.Imgur(self.client_id, client_secret = self.client_secret, refresh_token = self.refresh_token)


    #i mean, this function name should be pretty self-explanitory
    def uploadImage(self, url, title, description = None):

        image = self.imgurInstance.upload_image(url = url, title = title, description = description)

        return image


    def uploadAlbum(self, urls, title, description = None):

        #i just need this to do a county thing
        imageNum = 0
        imageIDs = []



        for image in urls:
            imageNum += 1
            image = self.imgurInstance.upload_image(url = image, title = f'Image number {imageNum} of album "{title}"')
            imageIDs.append(image.id)

        #making an album
        album = self.imgurInstance.create_album(title = title, description = description, images = imageIDs)

        #finally, adding these images to the album
        #album.add_images(imageIDs)

        #for some minor testing
        return album
