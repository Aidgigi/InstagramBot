import asyncio, time
from timeloop import Timeloop
from datetime import timedelta
from core.database import db
from core.instagram import ig

timer = Timeloop()

checkTime = 10

class Thread():
    #"""This should check for posts ever 30 seconds"""

    @staticmethod
    def start(block=False):
        try:
            #Thread.set_format()
            timer.start(block)
        except Exception as e:
            print(e)

    @staticmethod
    def stop():
        try:
            timer.stop()
        except Exception as e:
            print(e)

async def search():
    #this will use data from the database to check for posts

    #exporting the connections, making sure there are some to check, and checking
    connections = db.connectionsExport()

    if connections != False:
        for connection in connections:
            try:
                ig.getAndUpload(connection)

            #better safe than sorry
            except Exception as e:
                print(f"[THREAD] Error! {e}!")


@timer.job(interval=timedelta(seconds=checkTime))
def checkForPosts():
    #"""Run the process asynchronously on a timer."""
    asyncio.run(search())
