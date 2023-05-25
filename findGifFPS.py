import imageio
import os
from moviepy.editor import VideoFileClip


# make a forloop for each gif in the folder photosAndGifs
def gifToMp4(filename) -> str:
    print(filename)
    gif_name = os.path.basename(filename)
    print(gif_name)
    reader = imageio.get_reader(filename)
    gif_info = reader.get_meta_data()
    gif_fps = 1000 / gif_info["duration"]
    clip = VideoFileClip(filename)
    output_filename = "photosAndGifs/" + gif_name[:-4] + ".mp4"
    clip.write_videofile(output_filename, fps=gif_fps, codec="libx264")
    clip.close()
    reader.close()
    os.remove(filename)
    return output_filename
