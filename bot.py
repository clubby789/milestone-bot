import praw,re
import os
from os.path import join, dirname
from dotenv import load_dotenv
import urllib.request
import time
home = 1
try:
	from win10toast import ToastNotifier
except:
	home = 0

with open ("blacklist.txt", 'r') as f:
	blacklist = f.readlines()
blacklist = [line.rstrip('\n') for line in blacklist]

def isConsecutive(number):
	l = list(str(number))
	l = [ int(x) for x in l ]
	cons = 1
	for x in range(0,len(l)-1):
		if not (l[x]+1 == l[x+1]):
			cons = 0
	if cons == l:
		return 1
	else:
		return 0

def milestone(karma):
	if int(karma) < 1:
		return -1
	if karma.endswith("6969"):
		return 1
	elif karma.endswith("420"):
		return 1
	elif karma == "666":
		return 1
	elif "69420" in karma:
		return 1
	elif "42069" in karma:
		return 1
	elif (int(karma)%10000 == 0):
		return 1
	elif isConsecutive(karma)==1:
		return 1
	else:
		return -1

def wake():
	urllib.request.urlopen('https://desolate-tundra-24392.herokuapp.com/')

if home==1:
	toaster = ToastNotifier()

dotenv_path = join(dirname(__file__), '.env')
try:
	load_dotenv(dotenv_path)
except:
	print("On google")
client_id=os.environ.get('client_id')
client_secret=os.environ.get('client_secret')
user_agent=os.environ.get('user_agent')
username=os.environ.get('rUsername')
password=os.environ.get('password')
sub=os.environ.get('sub')
botAuthor=os.environ.get('author')


milestoneText = """You've hit a karma milestone ({karma}). Maybe you should make a post about it!

^(I am a bot, made by u/"""+botAuthor +""". If I'm doing something wrong, please message my author)"""

reddit = praw.Reddit(client_id=client_id,
					client_secret=client_secret,
					user_agent=user_agent,
					username=username,
					password=password)

subreddit = reddit.subreddit(sub)
print("Bot started!")
startTime=time.time()

while True:
	curTime = time.time()
	if curTime - startTime >= (25*60):
		wake()
		startTime = curTime
	for submission in subreddit.new(limit=1000):

		author = submission.author
		if author == '[removed]' or author == None or author in blacklist:
			try:
				print("Author is "+author+", skipping...")
			except TypeError:
				print("Author is none, skipping...")
			continue
		
		try:
			karma = str(int(author.comment_karma) + int(author.link_karma))
		except Exception as e:
			print(e)
			print(submission)
			continue
		if milestone(karma) == 1:
			send = True
			for message in reddit.inbox.sent(limit=50):
				if message.dest == author:
					send = False
			if send:
				try:
					author.message('Karma Milestone', milestoneText.format(karma=karma))
					logText = "Sent message to {author} for getting {karma} karma".format(author=author,karma=karma)
					print(logText)
					if home==1:
						toaster.show_toast("Message sent!", logText, threaded=True,
						icon_path=None,duration=3)
					try:
						with open("logtext.txt",'a') as f:
							f.write("\n"+logText)
					except:
						print("No log")
				except Exception as e: 
					print(e)
			

