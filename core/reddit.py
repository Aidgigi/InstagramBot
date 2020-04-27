import praw, textwrap
from core.database import db
import core.constants as constants

from prawcore.exceptions import RequestException, Forbidden, ServerError
from praw.exceptions import APIException, ClientException

class RedditClass:
    def __init__(self, client_id, client_secret, password, user_agent, username):
        self.reddit = praw.Reddit(
                    client_id = client_id,
                    client_secret = client_secret,
                    password = password,
                    user_agent = user_agent,
                    username = username)

        print("\'Reddit\' instance initialized!")

    #this will take a url and a connection, and upload to the sub using the desired method
    def uploadToSub(self, url, caption, conn_id):
        #getting the connection
        self.connection = db.returnConnection(conn_id)
        if self.connection == False:
            print("[REDDIT] Warning! Upload failed due to above error!")
            return False

        #getting the subreddit, and other things we need
        try:
            self.subreddit = self.reddit.subreddit(self.connection['connection']['subreddit'])
        except Exception as e:
            print(f"[REDDIT] Error! {e}!")
            return False

        self.mode = self.connection['connection']['mode']
        self.mode2 = self.connection['connection']['mode2']
        self.instaAccountPK = self.connection['connection']['instagramAccountPK']
        self.instaAccount = self.connection['connection']['instagramAccountUsername']

        self.title = f"New post by @{self.instaAccount} on Instagram"

        #posting the image
        try:
            self.post = self.subreddit.submit(self.title, url = url, send_replies = False)
        except Exception as e:
            print("[REDDIT] Warning! Bot it not allowed to post here!")
            return False

        #applying mode settings
        if self.mode == 2 or self.mode == 4:
            try:
                self.post.mod.distinguish(how = 'yes', sticky = True)
                self.post.mod.approve()
            except Exception as e:
                print(f"[REDDIT] Warning! Could no distinguish! ({e})")

        if self.mode == 3 or self.mode == 4:
            try:
                self.post.mod.lock()
                self.post.mod.approve()
            except Exception as e:
                print(f"[REDDIT] Warning! Could not lock! ({e})")

        #applying mode2 settings
        if self.mode2 == 2:
            self.postComment = self.post.reply(f"Caption: \"{caption}\"")

        if self.mode2 == 3:
            self.postComment = self.post.reply(f"[Find @{self.instaAccount} on Instagram!](https://www.instagram.com/{self.instaAccount}/)")

        if self.mode2 == 4:
            self.postComment = self.post.reply(f"Caption: \"{caption}\".\n\n[Find @{self.instaAccount} on Instagram!](https://www.instagram.com/{self.instaAccount}/)")

        #seeing if the new comment needs to be stickied, locked, or both.
        if self.mode2 == 2 or self.mode2 == 3 or self.mode2 == 4:
            if self.mode == 2:
                if self.postComment:
                    self.postComment.mod.distinguish(how = 'yes', sticky = True)

            if self.mode == 3 or self.mode == 4:
                if self.postComment:
                    self.postComment.lock()


    #this function is involed with registering the user
    def register(self):
        #making and unread messages list
        self.unreadInbox = []

        for item in self.reddit.inbox.unread(limit = None):
            #appending the list and reading it
            self.unreadInbox.append(item)
            self.reddit.inbox.mark_read(self.unreadInbox)
            self.unreadInbox = []

            #checking if the item is a message
            if 'Message' not in repr(item):
                print(f"[REDDIT] Warning! Item {item} is not a message!")
                return False

            if 'SubredditMessage' in repr(item):
                print(f"[REDDIT] Warning! Item {item} is not a message!")
                return False

            #checks passed, getting message item
            self.message = item
            if 'register' in self.message.subject:
                if ';' not in self.message.body:
                    print("[REDDIT] Warning! Improperly fomatted request!")
                    self.message.reply(textwrap.dedent(f"""Sorry u/{self.message.author}, but your request appears to be improperly formatted. Please, add parameters and seperate them by semicolons (\";\") and try again."""))
                    return False

                if ';' in self.message.body:
                    self.contents = self.message.body.split(';')
                    print(self.contents)




red = RedditClass(constants.REDDIT_CLIENT_ID, constants.REDDIT_CLIENT_SECRET, constants.REDDIT_PASSWORD, constants.REDDIT_USER_AGENT, constants.REDDIT_USERNAME)
