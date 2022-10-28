from yt_dlp import YoutubeDL
from loguru import logger


def search_download_youtube_video(video_name, num_results=1, download=False):
    '''
    Function that fetches the urls of videos from youtube
    :param video_name: Search text from user
    :param num_results: number of results to show, default 1
    :param download: boolean download --> if download as a file or not
    :return: dictionary
    '''
    with YoutubeDL() as ydl:
        logger.info(f"{__name__}YoutubeDL from Util initiated")
        videos = ydl.extract_info(f"ytsearch{num_results}:{video_name}", download=download)['entries']
        for format in videos[0]['formats']:
            if format['format_id'] == '22' or format['format_id'] == '18':
                '''   
                url --> url that allows to download a file on any
                device (auto download in pc) save to galery in android
                '''
                return {'download_url': format["url"], 'youtube_url': videos[0]['webpage_url']}
