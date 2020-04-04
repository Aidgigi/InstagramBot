#importing all of the things we need for the database
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, session
from sqlalchemy.ext.declarative import declarative_base

#importing all of the modules we need for different things
import time
import operator
import json
import core.constants    #the module containing all of the various credentials we may need


"""This class represents the main db, and everything it may need to do"""
class mainDB:

    #our init function, to get everything started
    #initializing the database class
    def __init__(self, url):
        self.url = url

        #this logs into and creates a database instance
        self.engine = create_engine(self.url)
        self.db = scoped_session(sessionmaker(bind=self.engine))
        self.meta = MetaData(self.engine)

        #making a base
        self.Base = declarative_base()

        """Coming up are some very important models that represent the different
        tables present in our db"""

        #our sub/account connection table
        class accntCon(self.Base):
            __tablename__ = "SUB_ACCOUNT_CONNECTION"

            id = Column(Integer,
                        primary_key = True)
            subreddit = Column(String)
            instagramAccount = Column(String)
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
