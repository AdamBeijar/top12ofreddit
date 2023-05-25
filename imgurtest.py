from traceback import print_tb
from numpy import e
import praw
from dotenv import load_dotenv
import os
import datetime
import requests
from findGifFPS import gifToMp4
from pathlib import Path


load_dotenv()
# Create an instance of the Reddit API client
reddit = praw.Reddit(
    client_id=str(os.getenv("reddit_client")),
    client_secret=str(os.getenv("reddit_secret")),
    user_agent="YOUR_USER_AGENT",
)

# Fetch the top 12 posts from r/memes
subreddit = reddit.subreddit("memes")
top_memes = subreddit.top(limit=500, time_filter="day")

current_filename = "test.mp4"


def processGifv(meme, current_filename):
    file_path = f"./photosAndGifs/{current_filename}.mp4"
    print(".gifv")
    # replace the .gif extension with .mp4
    url = meme.url.replace(".gifv", ".mp4")
    try:
        response = requests.get(url, headers={"User-Agent": "MyBot"}, verify=False)
        img_data = response.content
    except Exception as e:
        print(e)
        return False
    try:
        with open(f"./test/{current_filename}.mp4", "wb") as f:
            f.write(img_data)
    except Exception as e:
        print(e)
        return False
    realpath = Path(file_path)
    return {"filestr": file_path, "Path_path": realpath}


for idx, meme in enumerate(top_memes):
    # if meme.url includes imgur
    current_filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}-top-{idx}"
    if (
        str(meme.url).endswith(".jpg")
        or str(meme.url).endswith(".png")
        or str(meme.url).endswith(".jpeg")
    ):
        continue
    elif str(meme.url).endswith(".gif"):
        continue
    else:
        print(meme.url)
        # if meme.url has .gifv, remove it and add .gif
        processGifv(meme, current_filename)
