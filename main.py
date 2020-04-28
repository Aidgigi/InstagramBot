import core.database as database
from core.database import db
from core.instagram import ig
from core.imgur import im
from core.reddit import red
from core.thread import Thread
#from core.reddit import red
import time, asyncio

"""Creating tables, defining the main function, and starting the thread!"""
db.createTabs()

#our main function. really! thats it!
async def mainFn():
    red.register()
    asyncio.sleep(1)

#running the stuff
if __name__ == "__main__":
	Thread.start()
	asyncio.run(mainFn())
	Thread.stop()
