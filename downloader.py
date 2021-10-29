import os, sys
import subprocess
import pytube
from moviepy.editor import VideoFileClip, AudioFileClip

working_dir = "/Users/owen_min/git_repository/contibot"
video_prefix = "video_"
video_postfix = ".mp4"
audio_prefix = "audio_"
audio_postfix = ".mp3"
output_prefix = "output_"


def download(video_links):
    total_cnt = len(video_links)
    cnt = 0
    result_list = []

    for video_link in video_links:
        cnt += 1
        yt = pytube.YouTube(video_link)
        print("[", cnt, "/", total_cnt, "] Title:", yt.title)
        second = yt.length % 60
        minute = int(yt.length / 60 % 60)
        print("Video length:", yt.length, "sec ->", minute, "min", second, "sec")

        # print("Video codec:")
        # for target in yt.streams.filter(mime_type="video/mp4"):
        #     print("\t", target)
        # print("Audio codec:")
        # for target in yt.streams.filter(mime_type="audio/mp4"):
        #     print("\t", target)
        # continue

        video_name = video_prefix + str(cnt) + video_postfix
        audio_name = audio_prefix + str(cnt) + audio_postfix
        output_name = output_prefix + str(cnt) + video_postfix
        if os.path.exists(video_name):
            os.remove(video_name)
        if os.path.exists(audio_name):
            os.remove(audio_name)
        if os.path.exists(output_name):
            os.remove(output_name)

        video = yt.streams.filter(mime_type="video/mp4", video_codec="avc1.42001E").order_by('resolution').desc().first()
        audio = yt.streams.filter(mime_type="audio/mp4").order_by('abr').desc().first()
        print("Download target:")
        print("\tVideo:", video)
        print("\tAudio:", audio)
        if video is None or audio is None:
            print("No matching target!")
            break
        video.download(output_path=working_dir, filename=video_name)
        audio.download(output_path=working_dir, filename=audio_name)
        print("Download complete!\n")

        subprocess.call(['ffmpeg',
                         '-i', os.path.join(working_dir, video_name),
                         '-i', os.path.join(working_dir, audio_name),
                         output_name])

        os.remove(video_name)
        os.remove(audio_name)

        result_list.append(output_name)
        print("Conversion complete\n")

    return result_list

if __name__=='__main__':
    print("Start")

    links = ["https://youtu.be/v6EXq6fZXNI", "https://youtu.be/0aHuT5XM3yY", "https://youtu.be/3OJl8u8-eRY", "https://youtu.be/s0aYNrVCcrM"]
    download_list = download(links)
    print("Download list:", download_list)

    print("End")
