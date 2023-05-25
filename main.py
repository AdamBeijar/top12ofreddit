from inspect import trace
import praw
import requests
from findGifFPS import gifToMp4
import datetime
from bs4 import BeautifulSoup
import json
import subprocess
import time
import instagrapi
import os
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image
from captionMaker import makeCaption
import schedule
from localpackages import jsonLogging
import traceback


class instagramRedditBot:
    def __init__(self):
        load_dotenv()
        self.redditCredentials = {
            "client_id": str(os.getenv("reddit_client")),
            "client_secret": str(os.getenv("reddit_secret")),
        }
        self.instagramCredentials = {
            "username": str(os.getenv("instagram_username")),
            "password": str(os.getenv("instagram_password")),
        }
        self.LIMIT = 12
        self.TIME_FILTER = "day"
        self.reddit = praw.Reddit(
            client_id=self.redditCredentials["client_id"],
            client_secret=self.redditCredentials[
                "client_secret"
            ],  # Not needed for read-only Reddit API access
            user_agent="YOUR USER AGENT",
            redirect_uri="http://localhost:8080",
        )
        self.instagram = instagrapi.Client()
        self.instagram.login(
            self.instagramCredentials["username"], self.instagramCredentials["password"]
        )
        # make a variable that is yesterday at 12:00am
        self.last_posted = datetime.datetime.today()
        self.last_posted = self.last_posted - datetime.timedelta(days=1)
        self.last_posted = self.last_posted.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        self.last_memes = self.last_posted.day
        self.logging = jsonLogging.logging()

    def mainLoop(self):
        self.logging.log("Starting main loop", "info")
        # check if it is a new day
        if datetime.datetime.now().day != self.last_memes:
            self.logging.log("New day, resetting last posted", "info")
            self.getTopMemes("memes")
            self.last_memes = datetime.datetime.now().day
            # post first meme of the day
            self.postMeme(self.todays_memes[0])
            self.todays_memes[0]["already_posted"] = True
            self.last_posted = datetime.datetime.now().hour
            self.logging.log("Posted first meme of the day", "info")
        else:
            self.logging.log("Not a new day, continuing", "info")
            for meme in self.todays_memes:
                datetime_obj = datetime.datetime.strptime(
                    meme["date"], "%Y-%m-%dT%H:%M:%S"
                )
                if (
                    not meme["already_posted"]
                    and datetime_obj.hour == datetime.datetime.now().hour
                ):
                    self.logging.log("Posting meme", "info")
                    self.postMeme(meme)
                    meme["already_posted"] = True
                    self.last_posted = datetime.datetime.now().hour
                    break
            self.logging.log("Posted meme", "info")
        self.logging.log("Finished main loop", "info")

    def postMeme(self, meme):
        caption = makeCaption(meme)
        self.logging.log("Caption: " + caption, "info")
        # check what type of file it is
        try:
            if meme["image"].endswith(".mp4"):
                self.logging.log("found .mp4", "info")
                self.instagram.clip_upload(meme["path"], caption=caption)
            else:
                self.logging.log("found .jpg", "info")
                self.instagram.photo_upload(meme["path"], caption=caption)
            os.remove(meme["path"])
        except Exception:
            self.logging.log(traceback.format_exc(), "error")
            return False
        self.logging.log("Posted meme to instagram", "info")

    def processGifv(self, meme, current_filename):
        file_path = f"./photosAndGifs/{current_filename}.mp4"
        print(".gifv")
        # replace the .gif extension with .mp4
        url = meme.url.replace(".gifv", ".mp4")
        try:
            response = requests.get(url, headers={"User-Agent": "MyBot"}, verify=False)
            img_data = response.content
        except Exception:
            self.logging.log(traceback.format_exc(), "error")
            return False
        try:
            with open(f"./photosAndGifs/{current_filename}.mp4", "wb") as f:
                f.write(img_data)
        except:
            self.logging.log(traceback.format_exc(), "error")
            return False
        realpath = Path(file_path)
        return {"filestr": file_path, "Path_path": realpath}

    def processImage(self, meme, current_filename):
        file_extension = str(meme.url).split(".")[-1]
        print(file_extension)
        file_path = f"./photosAndGifs/{current_filename}.jpg"
        try:
            response = requests.get(
                meme.url, headers={"User-Agent": "MyBot"}, verify=False
            )
        except:
            self.logging.log(traceback.format_exc(), "error")
            return False
        img_data = response.content
        try:
            with open(file_path, "wb") as f:
                f.write(img_data)
            image = Image.open(file_path)
        except:
            self.logging.log(traceback.format_exc(), "error")
            return False
        new_image = image.convert("RGB")
        new_image.save(file_path)
        realpath = Path(file_path)
        return {"filestr": file_path, "Path_path": realpath}

    def processGif(self, meme, current_filename):
        print(".gif")
        try:
            response = requests.get(
                meme.url, headers={"User-Agent": "MyBot"}, verify=False
            )
            img_data = response.content
        except:
            self.logging.log(traceback.format_exc(), "error")
            return False
        try:
            with open(f"./gifs/{current_filename}.gif", "wb") as f:
                f.write(img_data)
            file_path = gifToMp4(f"./gifs/{current_filename}.gif")
        except Exception:
            self.logging.log(traceback.format_exc(), "error")
            return False
        realpath = Path(file_path)
        return {"filestr": file_path, "Path_path": realpath}

    def processVideo(self, meme, current_filename):
        print(".mp4")
        headers = {"User-Agent": "MyBot"}
        file_path = f"./photosAndGifs/{current_filename}.mp4"
        try:
            response = requests.get(
                meme.url + "/DASH_720.mp4",
                headers=headers,
                verify=False,
            )
        except Exception:
            self.logging.log(traceback.format_exc(), "error")
            return False
        video_data = response.content
        try:
            with open(file_path, "wb") as f:
                f.write(video_data)
        except Exception:
            self.logging.log(traceback.format_exc(), "error")
            return False
        realpath = Path(file_path)
        return {"filestr": file_path, "Path_path": realpath}

    def getTopMemes(self, subreddit):
        self.logging.log("Getting top memes", "info")
        try:
            memes_subreddit = self.reddit.subreddit(subreddit)
            top_memes = memes_subreddit.top(
                limit=self.LIMIT, time_filter=self.TIME_FILTER
            )
        except Exception:
            self.logging.log(
                f"Error getting top memes: {traceback.print_exc()}", "critical"
            )
            return False
        self.logging.log("Successfully got top memes, starting to process them", "info")
        self.todays_memes = []
        for idx, meme in enumerate(top_memes):
            try:
                current_filename = (
                    f"{datetime.datetime.now().strftime('%Y-%m-%d')}-top-{idx}"
                )
                if (
                    str(meme.url).endswith(".jpg")
                    or str(meme.url).endswith(".png")
                    or str(meme.url).endswith(".jpeg")
                ):
                    if not (current_image := self.processImage(meme, current_filename)):
                        raise Exception("Error processing image")
                elif str(meme.url).endswith(".gif"):
                    if not (current_image := self.processGif(meme, current_filename)):
                        raise Exception("Error processing gif")
                elif str(meme.url).endswith(".gifv"):
                    if not (current_image := self.processGifv(meme, current_filename)):
                        raise Exception("Error processing gifv")
                else:
                    if not (current_image := self.processVideo(meme, current_filename)):
                        raise Exception("Error processing video")
                self.todays_memes.append(
                    {
                        "top": idx,
                        "title": meme.title,
                        "image": current_image["filestr"],
                        # make a variable that is todays date at 12:00am + idx + 1 * 2 hours
                        "date": datetime.datetime.now().strftime("%Y-%m-%d")
                        + "T"
                        + str((idx) * 2)
                        + ":00:00",
                        "already_posted": False,
                        "path": current_image["Path_path"],
                        "author": meme.author.name,
                        "upvotes": meme.score,
                    }
                )
            except Exception:
                self.logging.log(
                    f"Error processing meme: {traceback.print_exc()}", "error"
                )
                continue


if __name__ == "__main__":
    bot = instagramRedditBot()
    bot.mainLoop()
    schedule.every(2).hours.at(":00").do(bot.mainLoop)
    while True:
        schedule.run_pending()
        time.sleep(1)
