# InstaRedditBot
A new Reddit bot that serves to make the gap between Reddit and Instagram smaller. Link an Instagram account to your subreddit, wait for the account to post, and voila, the bot posts on your subreddit. With 4 modes, and 4 submodes, how to bot posts is up to you. New features will be added often, so don't be afraid to request one now!

## Adding the Bot
Some information regarding adding the bot, and its modes.

### Modes
The bot's regular and submodes
#### Regular Modes
These are the various modes you can use when registering with the bot.
* `Mode 1` Regular posting
* `Mode 2` The bot's posts will be stickied, and will remain until manually removed.
* `Mode 3` The bot's posts will be locked.
* `Mode 4` The bot's posts will be stickied and locked.
* **Note!** For modes 2, 3, and 4, you will need to add the bot as a moderator with "Post" privileges.

#### Submodes
These submodes will define how the bot comments on its posts.
* `Mode 1` The bot will leave no comment on its post.
* `Mode 2` The bot will comment the caption of the original Instagram post.
* `Mode 3` The bot will comment a link to the original Instagram account.
* `Mode 4` The bot will comment both the original caption, and a link to the Instagram account.
* **Note!** If the regular mode is set to 2, 3, or 4, the comment the bot leaves will follow the same sticky/lock rules.

### Steps
How to connect the bot to your subreddit
#### Step 1
1. Determine which modes you would like the bot to be registered with.
2. If the bot needs moderator privileges, as in the case of modes 2, 3, or 4, add the bot as a mod **before** submitting a request.
3. Make sure you moderate the subreddit you wish to add the bot to, you will need full permissions in order to add it.

#### Step 2
1. Begin a message to u/InstaRedditBot bot [here](https://www.reddit.com/message/compose/?to=InstaRedditBot)
2. In the subject field, add the word "register"
3. In the body, write the subreddit you wish to add the bot to, **without** the "r/".
4. After that, add a semicolon (;). **do not** add a space after the semicolon.
5. After the semicolon, write the Instagram account you wish to add **(no @)**.
6. Repeat step 4.
7. Add your desired mode, then add a semicolon, and your desired submode, finished with another semicolon.
* An example request would look like: `dankmemes;salad.snake;1;4;`

#### Note:
* Each subreddit can only have one Instagram account linked to it for free. If you wish to add multiple—or even unlimited—accounts to your subreddit, please contact
[u/Aidgigi](https://reddit.com/u/Aidgigi) about getting a premium subscription to InstaRedditBot.
* If you wish to have the connection to your subreddit deleted, contact [u/Aidgigi](https://reddit.com/u/Aidgigi) to delete the connection.
* Since others have asked me; no, you do not need to own the Instagram account you wish to connect your sub to. If the Instagram account is private, it also will not work, however PM me and I will manually follow the account you wish to link.

## How it Works

### The Code
The bot is written completely in Python, and the program performs its task through the use of modules. In the ["core"](core/) folder, you can see these modules. What they do is fairly self-explanatory. In each module, the program interfaces with its respective API. Fortunately, the [Reddit API](https://github.com/praw-dev/praw) and [Instagram API](https://pypi.org/project/InstagramAPI/) had wrappers written for them by some very cool people. However, the available Python wrappers for the Imgur API didn't suit my needs, so I wrote my own—extremely small—version. This wrapper is free to use, and distribute, and can be found in [core/imgur.py](core/imgur.py).

In order to check for new posts, a few statements in core/thread.py are ran every 10 seconds. The first asks the database for a list of current connections, if there are none, this function returns False. If there are connections, we iterate through every connection, and plug its ID into a function that checks if the linked Instagram account has any new posts. If this account does, core/instagram.py fetches the post's url, tells core/imgur.py to upload it, the Imgur URL is sent back to core/instagram.py, which tells core/reddit.py to upload it to the correct subreddit. Wow, sorry for that. While this process is happening every 10 seconds, core/reddit.py is constantly because asked by main.py if the bot has any new DMs. If it does, the DM is processed—and if it's valid—will be added to the system. That's really it!

### Hosting
#### Files
The code, along with everything needed to run, is hosted here in this repo. What you're looking at right now is legitimate production code that is running on some linux server halfway across the globe.
#### The Program
Now that we have free and epic file hosting from the generous corporate entity that is Github, we need to run it. The program is ran on web-hosting platform called Heroku. Currently, the bot runs on the free version of Heroku, but once people start paying for premium, I hope to upgrade to faster dynos and a better database. Please contact me on reddit (u/Aidgigi) if you would like to financially support the project.

## Contributing
Yes, I want your help.

If you would like to contribute to the project, write some code, make mine better, and submit a pull request. If I like what you've done, I'll be sure to approve it. If you aren't the programming type, send me a PM on Reddit with your recommendation, and I'll add it to the bot if I like it.
