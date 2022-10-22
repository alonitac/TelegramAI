import time
from yt_dlp import YoutubeDL
import mysql.connector
from os import environ
'''mydb = mysql.connector.connect(
    host=environ.get('MYSQL_IP'),
    user=environ.get('MYSQL_ROOT_USER'),
    password=environ.get('MYSQL_ROOT_PASSWORD'))'''


def search_download_youtube_video(video_name, num_results=1,user_id=0,download=False):
    """
    This function downloads the first num_results search results from Youtube
    :param video_name: string of the video name
    :param num_results: integer representing how many videos to download
    :return: list of paths to your downloaded video files
    """
    results = []
    with YoutubeDL() as ydl:
        videos = ydl.extract_info(f"ytsearch{1}:{video_name}", download=False)['entries']
        print(videos[0], 'type', type(videos[0]))
        for format in videos[0]['formats']:
            if format['format_id'] == '22' or format['format_id'] == '18':
                print(f'Download Video:\n{format["url"]}')
                return format["url"]
                    #mycursor = mydb.cursor()
'''                sql_query = "INSERT INTO users (user_bot_id,search_phrase,link_view,link_download) " \
                            "VALUES (%s, %s, %s, %s)"
                    values = (user_id,video_name,videos[0]['webpage_url'],format["url"])
                    mycursor.execute(sql,val)
                    mydb.commit()
                    #mycursor.rowcount
                data_dict = {'title':videos[0]['title'],'view':videos[0]['webpage_url'],'download':format["url"]}'''
'''    
        for video in videos:
            print(f'VIEW:\n{video["webpage_url"]}\nDownload:\n{video}')
            return
            results.append({
                'filename': ydl.prepare_filename(video),
                'video_id': video['id'],
                'title': video['title'],
                'url': video['webpage_url']
            })
            print(f'VIEW:\n{video["webpage_url"]}\nDownload:\n{video["formats"][20]}')
        '''

#search_download_youtube_video('hello')