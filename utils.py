import time
from yt_dlp import YoutubeDL


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

        for video in videos:
            results.append({
                'filename': ydl.prepare_filename(video),
                'video_id': video['id'],
                'title': video['title'],
                'url': video['webpage_url']
            })

    return results
