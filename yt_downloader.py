from pytube import Playlist
from moviepy.video.io.VideoFileClip import AudioFileClip
import os
import eyed3
import os

from eyed3.id3.tag import Tag

author = "Влади́мир Ильи́ч Ле́нин"
playlist_url = "https://www.youtube.com/playlist?list=PL6we2rCO8rrQAhj_p1EJoktNhJ0IlOUrC"
bitrate = "32k"

playlist = Playlist(playlist_url)
dir = os.path.join(
    os.getcwd(), author or playlist.owner, playlist.title)
videos = playlist.videos
padding = int(len(str(len(videos))))

if padding < 2:
    padding = 2

print("#" * 80 + f"\n\t{playlist.title} "
      + f"by {author or playlist.owner}\n" + "#" * 80)

for index, video in enumerate(videos, start=1):
    prefix = str(index).zfill(padding) + "_"
    title = "".join(c for c in video.title if c.isalnum() or c.isspace())
    print("\n" + "-" * 80
          + f"\nChapter {str(index).zfill(padding)} "
          + f"of {len(videos)}\n{title}\n" + "-" * 80)
    captions = video.captions
    for caption in [c for c in captions
                    if c.code in ('en', 'es', 'a.en', 'a.es')]:
        print(f"Downloading captions: {caption.code}")
        caption.download(title=video.title, output_path=dir,
                         filename_prefix=prefix)
        with open(os.path.join(dir, prefix + title + f" ({caption.code}).srt"), "r") as srt:
            with open(os.path.join(dir, prefix + title + f" ({caption.code}).txt"), "w") as txt:
                txt.writelines(srt.readlines()[2::4])

    mp3 = os.path.join(dir, prefix + title + ".mp3")
    if os.path.exists(mp3):
        print("Already done!")
        continue

    mp4 = os.path.join(dir, prefix + title + ".mp4")
    if not os.path.exists(mp4):
        print("Downloading from Youtube...")
        audio_stream = video.streams.filter(
            only_audio=True,
            subtype="mp4"
        ).order_by("bitrate").asc().first()

        bitrate = f"{audio_stream.bitrate}k"
        audio_stream.download(
            output_path=dir,
            filename_prefix=prefix,
            skip_existing=True
        )

        for caption in [v for k, v in video.captions.items()
                        if k in ('en', 'es', 'a.en', 'a.es')]:
            print(f"Downloading captions: {caption.code}")
            caption.download(title=video.title, output_path=dir,
                             filename_prefix=prefix)
            with open(os.path.join(dir, prefix + title + f" ({caption.code}).srt")) as srt:
                with open(os.path.join(dir, prefix + title + f" ({caption.code}).txt")) as txt:
                    txt.writelines(srt.readlines()[2::4])

    print("Conventing mp4 to mp3...")
    clip = AudioFileClip(mp4)
    clip.write_audiofile(mp3, bitrate=bitrate)
    clip.close()
    os.remove(mp4)

    print("Adding tags to mp3...")
    audiofile = eyed3.load(mp3)
    tag = Tag()
    tag.track_num = index
    tag.title = video.title[video.title.find(":") + 2:]
    tag.artist = author or playlist.owner
    tag.album = playlist.title
    tag.publisher = playlist.owner
    audiofile.tag = tag
    audiofile.tag.save()
