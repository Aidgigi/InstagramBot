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
from core.models import accntCon, postLog


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


    #a function for creating the tables
    def createTabs(self):
        #reflecting the db locally
        self.meta.reflect(bind = self.engine)

        #checking to make sure that the tables dont exist, if a table doesnt exist, it's made
        self.Base.metadata.create_all(self.engine, self.Base.metadata.tables.values(), checkfirst = True)

        print('[DATABASE] Tables Created!')
        return True

    def createConnection(self, subreddit, instaAccount, owner, mode):
        #reflecting the db locally
        self.meta.reflect(bind = self.engine)

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

        #getting the connection for the given id
        self.connectionTables = self.db.query(accntCon).filter_by(id = int(conn_id)).all()

        if len(self.connectionTables) == 0:
            print(f"[DATABASE] Warning! No connection has been found with ID {conn_id}")
            return False

        if len(self.connectionTables) >= 2:
            print(f"[DATABASE] Fatal Error! Multiple connections have been found with ID {conn_id}. Investigation needed!")
            return False

        if len(self.connectionTable) == 1:
            self.connectionTable = self.connectionTables[0]

        try:
            #adding the data to our table
            self.connectionTable.previousPost = previousPost
            self.connectionTable.postCount += postCount

            #committing the changes
            self.db.commit()
            return self.connectionTable.id

        except Exeption as e:
            print(f"[DATABASE] Error! {e}!")
            return False

    def connectionsExport(self):
        #need a blank list that we can append and return
        self.connectionIds = []

        #reflecting the db locally
        self.meta.reflect(bind = self.engine)

        #getting every row, appening each row's id, and returning
        self.connections = self.db.query(accntCon).all()

        if len(self.connections) == 0:
            print("[DATABASE] Warning! There are no rows present in the system!")
            return False

        for row in self.connections:
            self.connectionIds.append(row.id)

        return self.connectionIds



db = mainDB(constants.DATABASE_URL)
