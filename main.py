import core.database as database
from core.database import db
import time

"""The main function, basically does everything"""
#db.createTabs()

#adding a test account to the system
subreddit = 'mytestsubgoaway'
instaAccount = 'me_ginise'
owner = 'Aidgigi'
mode = 0
test = db.createConnection(subreddit, instaAccount, owner, mode)
print(test)
