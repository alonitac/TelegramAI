import time
from yt_dlp import YoutubeDL
import os 

def search_download_youtube_video(video_name, num_results=1):
    """
    This function downloads the first num_results search results from Youtube
    :param video_name: string of the video name
    :param num_results: integer representing how many videos to download
    :return: list of paths to your downloaded video files
    """
    results = []
    with YoutubeDL() as ydl:
        videos = ydl.extract_info(f"ytsearch{num_results}:{video_name}", download=False)['entries']
        
        file_exists = False

        for video in videos:
            for file in os.listdir():
                if file == ydl.prepare_filename(video):
                    file_exists = True
                    break

            results.append({
                'filename': ydl.prepare_filename(video),
                'video_id': video['id'],
                'title': video['title'],
                'url': video['webpage_url']
            })
        
        if file_exists == False:
            videos = ydl.extract_info(f"ytsearch{num_results}:{video_name}", download=True)['entries']


    return results
