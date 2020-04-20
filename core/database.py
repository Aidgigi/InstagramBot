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



    #a function for creating the tables
    def createTabs(self):
        #reflecting the db locally
        self.meta.reflect(bind = self.engine)
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

        #checking to make sure that the tables dont exist, if a table doesnt exist, it's made
        self.Base.metadata.create_all(self.engine, self.Base.metadata.tables.values(), checkfirst = True)

        print('[DATABASE] Tables Created!')
        return True

    def createConnection(self, subreddit, instaAccount, owner, mode):
        #reflecting the db locally
        self.meta.reflect(bind = self.engine)
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

        #creating a unique ID for the connection
        idMin = 11111111
        idMax = 99999999
        loopState = True

        subTable = self.db.query(accntCon).filter_by(subreddit = str(subreddit)).all()

        if len(subTable) != 0 and subTable[0].premium == False:
            print(f"[DATABASE] Warning! A connection has already been attributed to r/{subreddit}. (Non-premium)")
            return False

        while loopState == True:
            randomId = random.randint(idMin, idMax)

            if len(self.db.query(accntCon).filter_by(id = int(randomId)).all()) == 0:
                loopState = False

            if len(self.db.query(accntCon).filter_by(id = int(randomId)).all()) != 0:
                loopState = True

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

        self.db.commit()
        print(f"[DATABASE] Message! Connect with ID {randomId} has been created!")
        return randomId

    def returnConnection(self, conn_id):
        #reflecting the db locally
        self.meta.reflect(bind = self.engine)
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

        self.connectionTables = self.db.query(accntCon).filter_by(id = int(conn_id)).all()

        if len(self.connectionTables) == 0:
            return False
            print("[DATABASE] Warning! Connection not found!")

        if len(self.connectionTables) >= 2:
            return False
            print("[DATABASE] Fatal Error! Multiple connections share an ID!")

        else:
            self.connectionTable = self.connectionTables[0]

        #formatting and returning the data
        return {"connection":{
            "id": self.connectionTable.id,
            "subreddit": self.connectionTable.subreddit,
            "instaAccount": self.connectionTable.instaAccount,
            "previousPost": self.connectionTable.previousPost,
            "owner": self.connectionTable.owner,
            "postCount": self.connectionTable.postCount,
            "mode": self.connectionTable.mode,
            "premium": self.connectionTable.premium
        }}

    def updateTable(self, conn_id, previousPost, postCount):
        #reflecting the db locally
        self.meta.reflect(bind = self.engine)
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


db = mainDB(constants.DATABASE_URL)
