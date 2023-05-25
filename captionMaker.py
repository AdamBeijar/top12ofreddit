from pathlib import Path
import json
import random
import emoji


def makeCaption(meme):
    hashtags = getHashtags()
    caption = f"""{meme['title']}

top {meme["top"]+1} in r/memes on {meme["date"].split("T")[0]} made by {meme['author']} with {meme['upvotes']} upvotes
\U0001F525 follow @top12ofreddit for more \U0001F525


\U0001F534
\U0001F534
\U0001F534
Tags dont mind these:
"""
    for hashtag in hashtags:
        caption += f"{hashtag} "
    return caption


def getHashtags():
    # get the hashtags from the json file
    json_hashtags = json.load(open("hashtags.json"))["hashtags"]
    # choose 30 random hashtags
    while len(json_hashtags) > 30:
        json_hashtags.pop(random.randint(0, len(json_hashtags) - 1))
    return json_hashtags


if __name__ == "__main__":
    memes = [
        {
            "title": "Flat earthers can't explain this",
            "image": "photosAndGifs/2023-05-16-top-0.mp4",
            "date": "2023-05-16T0:00:00",
            "aleady_posted": False,
            "path": Path("photosAndGifs/2023-05-16-top-0.mp4"),
            "author": "Karvis_art",
            "upvotes": 42921,
        },
        {
            "title": "Poor guy",
            "image": "photosAndGifs/2023-05-16-top-1.mp4",
            "date": "2023-05-16T2:00:00",
            "aleady_posted": False,
            "path": Path("photosAndGifs/2023-05-16-top-1.mp4"),
            "author": "PowerfulOperation8",
            "upvotes": 42441,
        },
        {
            "title": "Down horrendously.",
            "image": "photosAndGifs/2023-05-16-top-2.mp4",
            "date": "2023-05-16T4:00:00",
            "aleady_posted": False,
            "path": Path("photosAndGifs/2023-05-16-top-2.mp4"),
            "author": "thepositivepandemic",
            "upvotes": 20800,
        },
        {
            "title": "Therapy hOur!",
            "image": "photosAndGifs/2023-05-16-top-3.mp4",
            "date": "2023-05-16T6:00:00",
            "aleady_posted": False,
            "path": Path("photosAndGifs/2023-05-16-top-3.mp4"),
            "author": "Kakaroshitto",
            "upvotes": 19015,
        },
        {
            "title": "villains were different",
            "image": "photosAndGifs/2023-05-16-top-4.mp4",
            "date": "2023-05-16T8:00:00",
            "aleady_posted": False,
            "path": Path("photosAndGifs/2023-05-16-top-4.mp4"),
            "author": "nineties_nostalgia",
            "upvotes": 11271,
        },
        {
            "title": "We were lied to all these years!",
            "image": "./photosAndGifs/2023-05-16-top-5.jpg",
            "date": "2023-05-16T10:00:00",
            "aleady_posted": False,
            "path": Path("photosAndGifs/2023-05-16-top-5.jpg"),
            "author": "IdkWhatImEvenDoing69",
            "upvotes": 8407,
        },
        {
            "title": "What's better?",
            "image": "./photosAndGifs/2023-05-16-top-6.jpg",
            "date": "2023-05-16T12:00:00",
            "aleady_posted": False,
            "path": Path("photosAndGifs/2023-05-16-top-6.jpg"),
            "author": "fambestera",
            "upvotes": 7769,
        },
        {
            "title": "AI has come a very long way",
            "image": "./photosAndGifs/2023-05-16-top-7.jpg",
            "date": "2023-05-16T14:00:00",
            "aleady_posted": False,
            "path": Path("photosAndGifs/2023-05-16-top-7.jpg"),
            "author": "DrathNur",
            "upvotes": 6778,
        },
        {
            "title": "It really starting to be too much",
            "image": "./photosAndGifs/2023-05-16-top-8.jpg",
            "date": "2023-05-16T16:00:00",
            "aleady_posted": False,
            "path": Path("photosAndGifs/2023-05-16-top-8.jpg"),
            "author": "HotSoupInYourAss",
            "upvotes": 6807,
        },
        {
            "title": "Back in my day, Reese's tasted way better",
            "image": "./photosAndGifs/2023-05-16-top-9.jpg",
            "date": "2023-05-16T18:00:00",
            "aleady_posted": False,
            "path": Path("photosAndGifs/2023-05-16-top-9.jpg"),
            "author": "TheRealOcsiban",
            "upvotes": 4994,
        },
        {
            "title": "sometimes your greatest enemy is yourself",
            "image": "./photosAndGifs/2023-05-16-top-10.jpg",
            "date": "2023-05-16T20:00:00",
            "aleady_posted": False,
            "path": Path("photosAndGifs/2023-05-16-top-10.jpg"),
            "author": "InfiniteX5",
            "upvotes": 4265,
        },
        {
            "title": "It do be like that",
            "image": "photosAndGifs/2023-05-16-top-11.mp4",
            "date": "2023-05-16T22:00:00",
            "aleady_posted": False,
            "path": Path("photosAndGifs/2023-05-16-top-11.mp4"),
            "author": "Specific-Pea2293",
            "upvotes": 4121,
        },
    ]
    for idx, meme in enumerate(memes):
        makeCaption(meme, idx)
