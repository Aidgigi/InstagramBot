#importing all of the things we need for the database models
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from core.database import db

class accntCon(db.Base):
    __tablename__ = "SUB_ACCOUNT_CONNECTION"

    id = Column(Integer, primary_key = True)
    subreddit = Column(String)
    instagramAccountPK = Column(BigInteger)
    instagramAccountUsername = Column(String)
    previousPost = Column(BigInteger)
    owner = Column(String)
    postCount = Column(Integer)
    mode = Column(Integer)
    premium = Column(Boolean)

    def repr(self):
        return f'SubCon Model'


#a log helpful in making sure that we only post once
class postLog(db.Base):
    __tablename__ = "BOT_POST_LOG"

    submissionId = Column(String)
    instagramPostId = Column(String, primary_key = True)
    subreddit = Column(String)
    instagramAccount = Column(String)
    time = Column(Integer)

    def repr(self):
        return f'PostLog Model'
