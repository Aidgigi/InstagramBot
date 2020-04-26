import core.database as database
from core.database import db
from core.instagram import ig
from core.imgur import im
from core.reddit import red
import time

"""The main function, basically does everything"""
db.createTabs()

"""
sub = "mytestsubgoaway"
accnt = "gins.e"
owner = "Aidgigi"
mode = 1
mode2 = 4
newCon = db.createConnection(sub, accnt, owner, mode, mode2)
print(newCon)
"""

def mainFn(conn_id):
    image = ig.getAndUpload(conn_id)
    if image != []:
        print(image)

while True:
    mainFn(17194749)
    time.sleep(5)
