from natsort import natsorted
import os
from moviepy.editor import *


L =[]

for root, dirs, files in os.walk("./videos"):

    files = natsorted(files)
    for file in files:
        if os.path.splitext(file)[1] == '.mp4':
            filePath = os.path.join(root, file)
            video = VideoFileClip(filePath)
            L.append(video)

final_clip = concatenate_videoclips(L)
final_clip.to_videofile("output.mp4")
