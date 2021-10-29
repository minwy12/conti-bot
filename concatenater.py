import os, subprocess
from moviepy.editor import VideoFileClip, concatenate_videoclips

output_file = "merged.mp4"
input1 = "output_1.mp4"
input2 = "output_2.mp4"
list_file = "list.txt"
if os.path.exists(output_file):
    os.remove(output_file)

# clip_1 = VideoFileClip(input1)
# clip_2 = VideoFileClip(input2)
#
# final_clip = concatenate_videoclips([clip_1, clip_2])
# final_clip.write_videofile(output_file)

subprocess.call(['ffmpeg',
                 '-f', 'concat',
                 '-safe', '0',
                 '-i', list_file,
                 '-c', 'copy',
                 output_file])
