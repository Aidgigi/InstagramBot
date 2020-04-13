from InstagramAPI import InstagramAPI
import database

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
