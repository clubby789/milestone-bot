import praw,re
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

client_id=os.environ.get('client_id')
client_secret=os.environ.get('client_secret')
user_agent=os.environ.get('user_agent')
username=os.environ.get('rUsername')
password=os.environ.get('password')
sub=os.environ.get('sub')
botAuthor=os.environ.get('author')


milestoneText = """You've hit a karma milestone ({karma}). Maybe you should make a post about it!

^(I am a bot, made by """+botAuthor +""". If I'm doing something wrong, please message my author)"""

reddit = praw.Reddit(client_id=client_id,
					client_secret=client_secret,
					user_agent=user_agent,
					username=username,
					password=password)

subreddit = reddit.subreddit(sub)


while True:
	for submission in subreddit.new(limit=100):
		author = submission.author
		karma = str(int(author.comment_karma) + int(author.link_karma))
		if karma.endswith("69") or karma.endswith("420") or karma.endswith("666"):
			send = True
			for message in reddit.inbox.sent(limit=50):
				if message.dest == author:
					send = False
			if send:
				author.message('Karma Milestone', milestoneText.format(karma=karma))
				print("Sent message to {author} for getting {karma} karma".format(author=author,karma=karma))
