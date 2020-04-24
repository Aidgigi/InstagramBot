from InstagramAPI import InstagramAPI
from database import db
import asyncio
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


    def getRecentImage(self, targetUsername):
        self.instaId = returnId(targetUsername)
        if self.instaId == False:
            return False

        #getting the user id, getting the feed, formatting, and returning the most recent pk
        self.userId = returnId(targetUsername)

        if self.userId == False:
            print(f"[INSTAGRAM] Warning! Unable to get feed of user {targetUsername} due to above error!")
            return False

        self.iGram.getUserFeed(userId)
        self.userFeed = self.iGram.LastJson
        if self.userFeed['num_results'] == 0:
            print(f"[INSTAGRAM] Warning! Feed of user {targetUsername} is empty!)
            return False

        if 'message' in self.userFeed and self.userFeed['status'] == 'fail':
            print(f"[INSTAGRAM] Warning! Unknown Instaram API error: \"{message}\"!")
            return False

        return self.userFeed['items'][0]['pk']


    #this function checks if there are any new images from a given account
    #and if so, uploads that image and returns the imgur URL
    async def getImage(self, conn_id):
        #getting the pk of the most recent post checked
        self.connection = db.returnConnection(conn_id)
        if self.connection != False:
            self.recentPost = self.connection['previousPost']
            self.targetPk = self.connection['instagramAccount']

        #getting the account's most recent post (from instagram)
        self.accountRecentPost = getRecentImage(self.targetUsername)
        if self.accountRecentPost == False:
            print("[INSTAGRAM] Warning! Returning recent image failed due to above error!")
            return False

        if self.recentPost == self.accountRecentPost:
            print(f"[INSTAGRAM] Message! No new posts were found for user {targetUsername}")


ig = InstaAPI(constants.INSTAGRAM_USERNAME, constants.INSTAGRAM_PASSWORD)
