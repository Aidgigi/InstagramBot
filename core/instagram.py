from InstagramAPI import InstagramAPI
from core.imgur import im
import asyncio
import codecs
import core.constants as constants

#this class makes communicating with instagram api straightforward
class InstaAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.iGram = InstagramAPI(self.username, self.password)
        self.iGram.login()

    #this function takes a username and returns a pk, AKA user id
    def returnId(self, targetUsername):

        self.iGram.searchUsername(targetUsername)
        self.response = self.iGram.LastJson

        if 'message' in self.response and self.response['satus'] == 'fail':
            print(f"[INSTAGRAM] Warning! No Instagram account found with username: {targetUsername}!")
            return False

        if self.response['status'] == 'ok':
            return self.response['user']['pk']


    def getRecentImages(self, targetUsername):
        #getting the user id, getting the feed, formatting, and returning the most recent pk
        self.userId = self.returnId(targetUsername)
        if self.userId == False:
            return False


        if self.userId == False:
            print(f"[INSTAGRAM] Warning! Unable to get feed of user {targetUsername} due to above error!")
            return False

        self.iGram.getUserFeed(self.userId)
        self.userFeed = self.iGram.LastJson
        if self.userFeed['status'] == 'fail' and 'message' in self.userFeed:
            print(f"[Instagram] Warning! Finding feed failed due to: {self.userfeed['message']}")
            return 0

        if self.userFeed['num_results'] == 0:
            print(f"[INSTAGRAM] Warning! Feed of user {targetUsername} is empty!")
            return False

        if 'message' in self.userFeed and self.userFeed['status'] == 'fail':
            print(f"[INSTAGRAM] Warning! Unknown Instaram API error: \"{message}\"!")
            return False

        return self.userFeed


    #this function checks if there are any new images from a given account
    #and if so, uploads that image and returns the imgur URL
    def getAndUpload(self, conn_id):
        #blank list that will eventually hold our url[s]
        self.urlOut = []

        #getting the pk of the most recent post checked
        from core.database import db
        self.connection = db.returnConnection(conn_id)
        if self.connection != False:
            self.recentPost = self.connection['connection']['previousPost']
            self.targetPk = self.connection['connection']['instagramAccountPK']
            self.targetUsername = self.connection['connection']['instagramAccountUsername']

        if self.connection == False:
            print("[INSTAGRAM] Warning! Failed due to above error!")
            return False

        #getting the account's most recent post (from instagram)
        self.accountFeed = self.getRecentImages(self.targetUsername)
        self.accountRecentPost = self.accountFeed['items'][0]['pk']
        if self.accountRecentPost == False:
            print("[INSTAGRAM] Warning! Returning recent image failed due to above error!")
            return False

        if self.recentPost == self.accountRecentPost:
            #print(f"[INSTAGRAM] Message! No new posts were found for user {targetUsername}")
            return self.urlOut

        if 'carousel_media' in self.accountFeed['items'][0]:
            for slide in self.accountFeed['items'][0]['carousel_media']:
                if slide['media_type'] == 1:
                    self.urlOut.append(slide['image_versions2']['candidates'][0]['url'])

        if 'carousel_media' not in self.accountFeed['items'][0]:
            if self.accountFeed['items'][0]['media_type'] == 1:
                self.urlOut.append(self.accountFeed['items'][0]['image_versions2']['candidates'][0]['url'])

        """Now, we do something with our data"""
        #making a title
        self.postTitle = f"New post from Instagram user @{self.connection['connection']['instagramAccountUsername']} for r/{self.connection['connection']['subreddit']}"
        #getting the caption
        if 'caption' in self.accountFeed['items'][0]:
            if self.accountFeed['items'][0]['caption'] != None:
                self.preCap = self.accountFeed['items'][0]['caption'].encode("utf-8").decode("utf-8")
                self.postCaption = f"Caption from post: \"{self.preCap}\""

        if len(self.urlOut) == 0:
            print("[INSTAGRAM] Warning! Program recevied empty out list! Quitting!")
            return 0

        if len(self.urlOut) == 1:
            image = im.uploadImage(self.urlOut[0], self.postTitle, self.postCaption)

        if len(self.urlOut) >=2 :
            image = im.uploadAlbum(self.urlOut, self.postTitle, self.postCaption)

        #updating the database with some info
        db.updateTable(self.connection['id'], self.accountRecentPost, 1)

        #formatting and returning a link
        if 'link' in image:
            return image['link']

        if 'id' in image:
            return f"https://imgur.com/a/{image['id']}"




ig = InstaAPI(constants.INSTAGRAM_USERNAME, constants.INSTAGRAM_PASSWORD)
