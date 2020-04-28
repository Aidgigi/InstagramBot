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

                #checking if the request has valid parameters
                if ';' in self.message.body:
                    self.contents = self.message.body.split(';')
                    del self.contents[-1]

                    #checking the amount of parameters
                    if len(self.contents) <= 3:
                        print("[REDDIT] Warning! To many args in request!")
                        self.message.reply(textwrap.dedent(f"Sorry u/{self.message.author}, but your request didn't have enough arguments. Please add the correct, properly formatted parameters."))
                        return False

                    if len(self.contents) > 4:
                        print("[REDDIT] Warning! To many args in request!")
                        self.message.reply(textwrap.dedent(f"Sorry u/{self.message.author}, but your request had too many arguments. Please add the correct, properly formatted parameters."))
                        return False

                    #length check passed, checking every arg
                    if len(self.contents) == 4:
                        #getting the subreddit and checking if the user is a mod there
                        try:
                            self.subreddit = self.reddit.subreddit(self.contents[0])
                        except Exception as e:
                            print("[REDDIT] Warning! Cannot find subreddit!")
                            self.message.reply(textwrap.dedent(f"""Sorry u/{self.message.author}, but I cannot find a subreddit with the name r/{self.contents[0]}.\r
                            \rThe subreddit may be banned, locked to me, or may not exist. If your subreddit is private, I will need to be added as an approved user or moderator in order to see it."""))
                            return False

                        #got the sub, checking if user is a mod there
                        if self.message.author not in self.subreddit.moderator():
                            print(f"[REDDIT] Warning! {self.message.author} does not moderate r/{self.subreddit}!")
                            self.message.reply(textwrap.dedent(f"Sorry u/{self.message.author}, but you do not moderate r/{self.subreddit}"))
                            return False

                        if self.message.author in self.subreddit.moderator():
                            #here we check every mod if they are the user, and check what perms they have
                            for moderator in self.subreddit.moderator():
                                if moderator == self.message.author and moderator.mod_permissions[0] == 'all':
                                    self.isFullMod = True

                            #user isnt a full mod
                            if not self.isFullMod:
                                print(f"[REDDIT] Warning! User {self.message.author} is not a full moderator of r/{self.subreddit}.")
                                self.message.reply(textwrap.dedent(f"Sorry u/{self.message.author}, but you are not a full moderator or r/{self.subreddit}."))
                                return False

                    #the first checks have passed, checking the instagram account
                    if self.isFullMod and self.isFullMod == True:
                        #importing instagram to avoid circular imports
                        from core.instagram import ig
                        if ig.returnId(self.contents[1]) == False:
                            self.message.reply(textwrap.dedent(f"Sorry u/{self.message.author}, but the Instagram account @{self.contents[1]} does not exist. Please submit a new request with a valid Instagram account."))
                            return False

                        #instagram account exists and isn't private, moving on
                        else:
                            #checking our mods
                            if any(call in str(self.contents[2]) for call in ['1', '2', '3', '4']) == False and any(call in str(self.contents[3]) for call in ['1', '2', '3', '4']) == False:
                                print(f"[REDDIT] Warning! Mode argument out of range!")
                                self.message.reply(textwrap.dedent(f"Sorry u/{self.message.author}, but one of your mode arguments is out of range. Please select 1, 2, 3, or 4 for your mode and mode2."))
                                return False

                            #it passed the checks
                            if any(arg in str(self.contents[2]) for arg in ['1', '2', '3', '4']) and any(arg in str(self.contents[3]) for arg in ['1', '2', '3', '4']):
                                #checking if the bot is a mod
                                for moderator in self.subreddit.moderator():
                                    if moderator == 'InstaRedditBot' and any(arg in str(moderator) for arg in ['all', 'post']):
                                        self.botIsMod = True
                                else:
                                    self.botIsMod = False

                                if self.botIsMod = False and any(arg in str(self.contents[2]) for arg in ['2', '3', '4']):
                                    print(f"[REDDIT] Warning! Mode requires bot to be added as moderator!")
                                    self.message.reply(textwrap.dedent(f"""Sorry u/{self.message.author}, but you have selected mode {self.contents[2]}, which requires the bot to be added as a moderator.\r
                                    \rPlease, add u/InstaRedditBot as a moderator with \"Post\" permissions, and try again."""))
                                    return False

                                #adding to the db, and checking if it was successful!
                                self.newConnection = db.createConnection(str(self.subreddit), str(self.contents[1]), str(self.message.author), int(self.contents[2]), int(self.contents[3]))

                                #account already connected to subreddit
                                if self.newConnection == False or self.newConnection == 0:
                                    print(f"[REDDIT] Warning! Request failed due to above error!")
                                    self.message.reply(textwrap.dedent(f"""Sorry u/{self.message.author}, but your request cannot be completed. This is because an Instagram account has already been connection to r/{self.subreddit}.\r
                                    \rIf you would like to connect another account to r/{self.subreddit}, contact u/Aidgigi in order to purchase InstaRedditBot premium."""))
                                    return False

                                #account not connected
                                if self.newConnection:
                                    print(f"[REDDIT] Message! u/{self.message.author} has connected @{self.contents[1]} to r/{self.subreddit} with connection ID {self.newConnection}!")
                                    self.message.reply(textwrap.dedent(f"Thank you u/{self.message.author}! Instagram account [@{self.contents[1]}](https://www.instagram.com/{self.contents[1]}/) has been successfully connected to r/{self.subreddit}!"))
                                    return True








red = RedditClass(constants.REDDIT_CLIENT_ID, constants.REDDIT_CLIENT_SECRET, constants.REDDIT_PASSWORD, constants.REDDIT_USER_AGENT, constants.REDDIT_USERNAME)
