# Discord-Bot-Cses
Discord bot for tracking and comparing cses problemset progress of you and your friends.


# Requirements:
1. One of you must have solved most of cses problems, the bot will login to this account and track the progress of others.
2. He should be willing to set up the bot or share his user login cookies with the bot owner. 
3. Is case the problem-set is updated you need to restart the bot and with the updated problem set in problems/all.csv file and change the topics variable defined 
   in the main.py accordingly. For extracting the problems you can use extract_probs.py

# Instructions for adding the bot to your server
1. Generate your user login header and cookies from the cURL.(Ref: https://stackoverflow.com/questions/23102833/how-to-scrape-a-website-which-requires-login-using-python-and-beautifulsoup,
    2nd answer)
2. Create a bot account from, https://discord.com/developers/applications and give it general chat,message,send file priviliges.
2. Change the TOKEN in .env file to your bot's token.
3. Change the headers and cookies in .env file to your's. 
4. Host the bot on replit.
5. Add bot to your server.


# Commands/Features
Use these commands in the text channel to interact with the bot
1. !add _username_ : add user (must be a valid cses handle). The user will be prompted to clone a collab notebook to extract his stats(login info reqd.) and then upload using the !file command to initilize his data.
    Alternatively the user can use extract_stats.py locally.
2. !file _usserID_ (#username.csv attachment): upload the data of solved problems for user that you want to add. Only requrired once, the bot track the submission done by the user
    after it is added. The userID of the user (not the username) is requiered. The user will be added when the file is uploaded.
3. !users : shows list of all users
4. !topics : shows list of topics
5. !stats _all/topic/problem name_ : Show the number of problem solved stats for the requested topic/all topics. In case of problem name, the soltuion time will be shown.
6. !code _username problem name_: The bot sends a solution.cpp file containng the solution code of the rqueest. 


The data-base is stored in users and problems folder. 
