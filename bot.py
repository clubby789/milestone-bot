import praw,re,os
from os.path import join, dirname
from dotenv import load_dotenv
import urllib.request
import time
import quote
try:
	from win10toast import ToastNotifier
	home = 1
except:
	home = 0

with open ("blacklist.txt", 'r') as f:
	blacklist = f.readlines()
blacklist = [line.rstrip('\n') for line in blacklist]
#Some users break this apparently? 
#Could also add some kind of opt-out system

def isConsecutive(number): #Checks if number is consecutive (e.g. 12345)
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
	elif karma.endswith("420") and int(karma) < 6000:
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
	#Return value of 1 indicates milestone; in future possibly 
	#based on the actual number for custom messages

def wake(): #Dyno dies if it doesn't get regular requests
	try:
		urllib.request.urlopen('https://desolate-tundra-24392.herokuapp.com/')
	except Exception:
		pass

def quoteString():
	quote = getQuote()
	if quote == -1:
		return "Sorry, couldn't get your inspirational quote :("
	else:
		return "Inspirational quote: {} ^(From inspirobot.me)".format(quote)

if home==1:
	toaster = ToastNotifier() #If running on home system, create a notifier

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
#Get env variables


milestoneText = """You've hit a karma milestone ({karma})!

^(I am a bot, made by u/"""+botAuthor +""". If I'm doing something wrong, please message my author)

{quote}"""

reddit = praw.Reddit(client_id=client_id,
					client_secret=client_secret,
					user_agent=user_agent,
					username=username,
					password=password)
#Authenticate with Reddit
subreddit = reddit.subreddit(sub)
print("Bot started!")
startTime=time.time()

while True:
	curTime = time.time()
	if curTime - startTime >= (25*60):
		wake() #Ping server every 25 mins
		startTime = curTime
	for submission in subreddit.new(limit=1000):
		#Fetch 1000 posts and check their authors
		#TODO: Switch this to Pushshift and fetch last day of posts
		#Possibly also comments
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
					send = False 		#Make sure we haven't already messaged author
								#about the milestone. Also reduces spam for 
			if send:				#users hitting multiple milestones
				try:
					author.message('Karma Milestone', milestoneText.format(karma=karma, quote=quoteString()))
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
			

