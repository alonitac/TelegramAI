from yt_dlp import YoutubeDL
from loguru import logger


def search_download_youtube_video(video_name, num_results=1,user_id=0,download=False):
    with YoutubeDL() as ydl:
        logger.info(f"{__name__}YoutubeDL from Util initiated")
        videos = ydl.extract_info(f"ytsearch{1}:{video_name}", download=False)['entries']
        for format in videos[0]['formats']:
            if format['format_id'] == '22' or format['format_id'] == '18':
                return {'download_url':format["url"],'youtube_url':videos[0]['webpage_url']}
