from InstagramAPI import InstagramAPI
from database import db

#this class makes communicating with instagram api straightforward
class InstaAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.iGram = InstagramAPI(self.username, self.password)
        self.iGram.login()

    #this function takes a username and returns a pk, AKA user id
    def addAccount(self, targetUsername):

        self.iGram.searchUsername(targetUsername)
        response = self.iGram.LastJson

        if 'message' in response and response['satus'] == 'fail':
            return False

        if response['status'] == 'ok':
            return response['user']['pk']


    #this function checks if there are any new images from a given account
    #and if so, uploads that image and returns the imgur URL
    def getImage(self, conn_id, user_id):
        #getting the pk of the most recent post checked
        recentPost = db.returnConnection(conn_id)
