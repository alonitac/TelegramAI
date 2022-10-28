import telebot,sqlite3,utils,re
from utils import search_download_youtube_video
from loguru import logger
from os import environ

#dbconnect = sqlite3.connect(r'c:\Users\Ilya Polonsky\Desktop\users9.db3')
#pointer = dbconnect.cursor()
#pointer.execute('CREATE TABLE IF NOT EXISTS user_bot (USER_BOT_ID TEXT,VIEW_URL TEXT,DOWNLOAD_URL TEXT)')

bot = telebot.TeleBot('5683443990:AAHvz0aQwW8ZI92KqIEnxw-6hh2jxy_6MDw') # creating a instance
dbconnect = sqlite3.connect(r'c:\Users\Ilya Polonsky\Desktop\users9.db3')
pointer = dbconnect.cursor()
pointer.execute('CREATE TABLE IF NOT EXISTS user_bot (USER_BOT_ID TEXT,VIEW_URL TEXT,DOWNLOAD_URL TEXT,PHOTO_ROOT TEXT, SEARCH_PHRASE TEXT)')


def database_check(text_to_search,user_id,photo_root=''):
    sql_query = (f'''SELECT * WHERE SEARCH_PHRASE = {text_to_search}''')
    result = pointer.execute(sql_query).fetchone()
    if result:
        return result[0][3]
    else:
        sql_query = (f'''INSERT INTO user_bot (USER_BOT_ID,VIEW_URL,DOWNLOAD_URL,PHOTO_ROOT, SEARCH_PHRASE) VALUES(?,?,?,?,?)''')
        links = utils.search_download_youtube_video()
        data = (user_id,links['youtube_url'], links['download_url'],photo_root,text_to_search)
        pointer.execute(sql_query,data)
        return links['download_url']


@bot.message_handler(content_types=['audio', 'document','sticker','video','video_note','voice', 'location', 'contact', 'new_chat_members', 'left_chat_member',
'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created',
'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message', 'web_app_data'])
def not_relevant(message):
    bot.reply_to(message,'Sorry, but at this point of time\nthis type of enterence is not supported.')


@bot.message_handler(content_types=['photo'])
def down_(message):
    bot.reply_to(message, 'Not Relevant')

@bot.message_handler(content_types=['text'])
def text_message(message):
    clean_text = message.text
    bot.reply_to(message, database_check(clean_text))


def main():
    bot.polling() # looking for message


if __name__ == '__main__':
    main()
