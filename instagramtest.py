import instagrapi
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image
import os

load_dotenv()  # load the values of the environment variables from the .env file
instagram_login = str(os.getenv("instagram_username"))
instagram_password = str(os.getenv("instagram_password"))

# Login
cl = instagrapi.Client()
cl.login(instagram_login, instagram_password)

# post image "./photosAndGifs/2023-05-11-top-1.jpeg" with caption "test"
imagepath = Path("./photosAndGifs/2023-05-11-top-3.mp4")
cl.clip_upload(path=imagepath, caption="test")
