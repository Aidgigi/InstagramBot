#importing all of the things we need for the database
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, session
from sqlalchemy.ext.declarative import declarative_base

#importing all of the modules we need for different things
import time
import operator
import json
import random
import core.constants as constants #the module containing all of the various credentials we may need


"""This class represents the main db, and everything it may need to do"""
class mainDB:

    #our init function, to get everything started
    #initializing the database class
    def __init__(self, url):
        self.url = url

        #this logs into and creates a database instance
        self.engine = create_engine(self.url)
        self.db = scoped_session(sessionmaker(bind = self.engine))
        self.meta = MetaData(self.engine)

        #making a base
        self.Base = declarative_base()

        """Coming up are some very important models that represent the different
        tables present in our db"""

        #our sub/account connection table
        class accntCon(self.Base):
            __tablename__ = "SUB_ACCOUNT_CONNECTION"

            id = Column(Integer, primary_key = True)
            subreddit = Column(String)
            instagramAccount = Column(String)
            previousPost = Column(String)
            owner = Column(String)
            postCount = Column(Integer)
            mode = Column(Integer)
            premium = Column(Boolean)

            def repr(self):
                return f'SubCon Model {self.id}'

        #a log helpful in making sure that we only post once
        class postLog(self.Base):
            __tablename__ = "BOT_POST_LOG"

            submissionId = Column(String)
            instagramPostId = Column(String, primary_key = True)
            subreddit = Column(String)
            instagramAccount = Column(String)
            time = Column(Integer)

            def repr(self):
                return f'postLog Model {self.subreddit}'

    #a function for creating the tables
    def createTabs(self):
        #reflecting the db locally
        self.meta.reflect(bind = self.engine)

        #checking to make sure that the tables dont exist, if a table doesnt exist, it's made
        self.Base.metadata.create_all(self.engine, self.Base.metadata.tables.values(), checkfirst = True)

        print('tables created')

    def createConnection(self, subreddit, instaAccount, owner, mode):
        #reflecting the db locally
        self.meta.reflect(bind = self.engine)

        #creating a unique ID for the connection
        idMin = 11111111
        idMax = 99999999
        loopState = True

        while loopState == True:
            randomId = random.randint(idMin, idMax)

            if len(self.db.query(Users).filter_by(id = int(randomId)).all()) == 0:
                loopState == False

            else:
                loopState == True

        #adding the connection
        self.db.add(accntCon(
            id = randomId,
            subreddit = subreddit,
            instagramAccount = instaAccount,
            previousPost = 'xxxxxx',
            owner = owner,
            postCount = 0,
            mode = mode,
            premium = False
        ))

    def returnConnection(self, conn_id):
        #reflecting the db locally
        self.meta.reflect(bind = self.engine)

        self.connectionTables = self.db.query(Users).filter_by(id = int(conn_id)).all()

        if len(self.connectionTables) == 0:
            return 0
            print("[DATABASE] Warning! Connection not found!")

        if len(self.connectionTables) >= 2:
            return 1
            print("[DATABASE] Fatal Error! Multiple connections share an ID!")

        else:
            self.connectionTable = self.connectionTables[0]

        #formatting and returning the data
        return {"connection":{
            "id": self.userRow.id,
            "subreddit": self.userRow.subreddit,
            "instaAccount": self.userRow.instaAccount,
            "previousPost": self.userRow.previousPost,
            "owner": self.userRow.owner,
            "postCount": self.userRow.postCount,
            "mode": self.userRow.mode,
            "premium": self.userRow.premium
        }}


db = mainDB(constants.DATABASE_URL)
