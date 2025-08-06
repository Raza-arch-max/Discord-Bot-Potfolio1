import os
import asyncio
import discord
import tweepy
import asyncpraw
from dotenv import load_dotenv
from utils import load_seen, save_seen

load_dotenv()

# Reddit setup
reddit = asyncpraw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

subreddits_to_monitor = ["UGCjobs"]

# Twitter setup (v2 with bearer token)
twitter_client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))

# Discord setup
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Needed to read message content

client = commands.Bot(command_prefix="!", intents=intents)


DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

seen = load_seen()

import asyncpraw
import os

async def fetch_reddit_posts():
    reddit = asyncpraw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

    new_posts = []
    subreddits_to_monitor = ["UGCjobs"]

    for subreddit_name in subreddits_to_monitor:
        try:
            subreddit = await reddit.subreddit(subreddit_name)
            async for submission in subreddit.new(limit=10):
                if submission.id not in seen["reddit"]:
                    seen["reddit"].append(submission.id)
                    text = f"📌 **Reddit Post**\n**Title:** {submission.title}\n🔗 {submission.url}"
                    new_posts.append(text)
        except Exception as e:
            print(f"❌ Error with subreddit '{subreddit_name}': {e}")

    await reddit.close()  # ✅ Important to close the session
    return new_posts



from tweepy.errors import TooManyRequests
import asyncio

async def fetch_twitter_posts():
    try:
        tweets = twitter_client.search_recent_tweets(
            query="your query",
            max_results=10,
            tweet_fields=["author_id", "text", "created_at"]
        )
        return tweets.data or []
    except TooManyRequests:
        print("Rate limit hit, sleeping 15 minutes...")
        await asyncio.sleep(900)
        return await fetch_twitter_posts()
    except Exception as e:
        print(f"Twitter fetch error: {e}")
        return []


def text_crop(text, max_len=280):
    return text if len(text) <= max_len else text[:max_len] + "..."

async def post_to_discord():
    await client.wait_until_ready()
    channel = client.get_channel(DISCORD_CHANNEL_ID)

    while not client.is_closed():
        reddit_posts = await fetch_reddit_posts()
        twitter_posts = await fetch_twitter_posts()
        all_posts = reddit_posts + twitter_posts

        for post in all_posts:
            await channel.send(post)
            await asyncio.sleep(1)  # slight delay to avoid rate limiting

        save_seen(seen)
        await asyncio.sleep(600)  # 10 minutes

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    client.loop.create_task(post_to_discord())

client.run(os.getenv("DISCORD_TOKEN"))