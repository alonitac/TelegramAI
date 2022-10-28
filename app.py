"""
        By: Ilya Polonsky
        For: INT College
        Chat Bot on the basis of Telegram telebot
        Designed for Linux and Docker container with Docker-compose configuration.
        bot name IP0810.
        The code designed to recieve an text from the user, find it in youtube and return to the user downloadable
        link with synchronised audio and video.
        the link contain video not less then 360p.
        The code designed with multiple handlers based on commands:
        /help - Responses with text explaining the bot
        /start - Responses with text explaining the bot
        /quote - Sets the desired method of messaging from the bot as reply mode --> every message will be a reply
                 to the user's input
        /noquote - Sets the desired method of messaging from the bot as NO Reply mode.
        Code designed to work with SQL Database (configured with sqlite but can be migrated to any database)
            user_bot table:
                            USER_BOT_ID TEXT --> user's id
                            VIEW_URL TEXT --> youtube url - NOT DOWNLOADABLE
                            DOWNLOAD_URL TEXT --> long url DONLOADABLE
                            PHOTO_ROOT TEXT --> photo root NOT IN USE, YET
                            SEARCH_PHRASE TEXT --> search phrase from user

            user_data table:
                            USER_BOT_ID TEXT --> user's id
                            REPLY --> 0/1 Whether user chose to have a reply mode or not
            all bot's actions measured with time and users recievs a time it took in every request.
            TODOs list all the updates that will increase code's functionality and security.
"""

import telebot, sqlite3, utils, os, uuid, datetime
from loguru import logger
api = os.environ.get('API')
img_path = '/img'
bot = telebot.TeleBot(api)
sql_path = '/db_data/bot_sql.db3'
logger.info(f'{__name__} Bot instance created')
dbconnect = sqlite3.connect(sql_path, check_same_thread=False)
logger.info(f'{__name__} Database connected')
pointer = dbconnect.cursor()
pointer.execute('CREATE TABLE IF NOT EXISTS user_bot (USER_BOT_ID TEXT,VIEW_URL TEXT,DOWNLOAD_URL TEXT'
                ',PHOTO_ROOT TEXT, SEARCH_PHRASE TEXT)')
pointer.execute('CREATE TABLE IF NOT EXISTS user_data (USER_BOT_ID TEXT,REPLY TEXT)')


def user_reply_check(user_id):
    '''
        Function that checks the use's prefered mode Reply or Not
        :param user_id:
        :return: boolean
    '''
    logger.info(f"{__name__} Check Reply or not User's preference in user_data table")
    result = pointer.execute('''SELECT REPLY FROM user_data WHERE USER_BOT_ID=?''', (str(user_id),)).fetchone()
    if not result:
        pointer.execute('''INSERT INTO user_data (USER_BOT_ID,REPLY) VALUES(?,?)''', (str(user_id), 'true',))
        dbconnect.commit()
        return True
    else:
        if result[0] == '1':
            logger.info(f"{__name__} User's prefernce is reply")
            return True
        else:
            logger.info(f"{__name__} User's prefernce is not reply")
            return False


def database_check(text_to_search, user_id, photo_root=''):
    '''
    function that checks if the input text is in database that saves search time
    and prevents additional requests with utils.
    :param text_to_search:
    :param user_id:
    :param photo_root:
    :return: string
    '''
    logger.info(f"{__name__} Check id search phrase exists in database")
    sql_query = f'''SELECT DOWNLOAD_URL FROM user_bot WHERE SEARCH_PHRASE=?;'''
    result = pointer.execute(sql_query, (text_to_search,)).fetchone()
    if result:
        return result[0]
    else:
        logger.info(f"{__name__} Search phrase doesn't exist in database, the data inserted")
        sql_query = (f'''INSERT INTO user_bot 
        (USER_BOT_ID,VIEW_URL,DOWNLOAD_URL,PHOTO_ROOT, SEARCH_PHRASE) VALUES(?,?,?,?,?)''')
        links = utils.search_download_youtube_video(text_to_search)
        logger.info(f"{__name__} Recieved data from youtube")
        data = (user_id, links['youtube_url'], links['download_url'], photo_root, text_to_search)
        pointer.execute(sql_query, data)
        dbconnect.commit()
        return links['download_url']


@bot.message_handler(commands=['start', 'help', 'START', 'HELP'])
def help_start_commands(message):
    '''
    Function handles commands start and help
    :param message: object message from Telegram
    :return: Function send messages to user within bot
    '''
    start_time = datetime.datetime.now()
    logger.info(f"{__name__} Response to help/start command")
    # TODO adding try and except
    bot.send_message(chat_id=message.chat.id, text=f'Hello {message.from_user.username}\nThe supported inputs are:'
                                                  f' Text and Photos.\nYou type a text and will recieve a link\n'
                     f'to a video from youtube that you can\neasily to save on your device.\nI will only send you a HQ '
                                                  f'videos, otherwise you shall recieve\n'
                                                  f'No video with a decent quality available\n'
                                                  f'\nOnce you send a photo it will be downloaded and saved.\n'
                     f'For help use /help command.\n'
                     f'By default all the message from me are in reply mode\nHowever, If you wish\n'
                     f'to have message from me to be in not reply mode,'
                                                  f' use /noqoute command\nand /qoute command\nreturn the default.'
                                                  f'\nIt took:{datetime.datetime.now() - start_time}')


@bot.message_handler(commands=['noqoute', 'NOQOUTE'])
def noqoute_on(message):
    '''
    Function handles commands noquite command
    :param message: object message from Telegram
    :return: Function send messages to user within bot
    '''
    start_time = datetime.datetime.now()
    logger.info(f"{__name__} NoReply set")
    # TODO adding try and except
    pointer.execute('''UPDATE user_data SET REPLY=false WHERE USER_BOT_ID=?''', (str(message.from_user.id),))
    dbconnect.commit()
    # TODO adding try and except
    bot.send_message(chat_id=message.chat.id, text=f'Dear {message.from_user.username}\n'
                     f'Qoute Mode is OFF\nIt took:{datetime.datetime.now() - start_time}')


@bot.message_handler(commands=['qoute', 'QOUTE'])
def qoute_on(message):
    '''
    Function handles commands quite command
    :param message: object message from Telegram
    :return: Function send messages to user within bot
    '''
    start_time = datetime.datetime.now()
    logger.info(f"{__name__} Replay set")
    # TODO adding try and except
    pointer.execute('''UPDATE user_data SET REPLY=true WHERE USER_BOT_ID=?''', (str(message.from_user.id),))
    dbconnect.commit()
    # TODO adding try and except
    bot.reply_to(message, f'Dear {message.from_user.username}\n'
                 f'Qoute Mode is ON\nIt took:{datetime.datetime.now() - start_time}')


@bot.message_handler(content_types=['audio', 'document', 'sticker', 'video', 'video_note', 'voice', 'location',
                                    'contact', 'new_chat_members', 'left_chat_member', 'new_chat_title',
                                    'new_chat_photo', 'delete_chat_photo', 'group_chat_created',
                                    'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id',
                                    'migrate_from_chat_id', 'pinned_message', 'web_app_data'])
def not_relevant(message):
    '''
    Function handles all content types except photo and text.
    :param message: object message from Telegram
    :return: Function send messages to user within bot
    '''
    start_time = datetime.datetime.now()
    logger.info(f"{__name__} Response to all the content types except text or photo")
    if user_reply_check(message.from_user.id):
        # TODO adding try and except
        bot.reply_to(message, 'Sorry, but at this point of time\nthis type of enterence is not supported.')
    else:
        # TODO adding try and except
        bot.send_message(chat_id=message.chat.id, text=f'Sorry, but at this point of time\nthis typ'
                                                       f'e of enterence is not supported.\n'
                                                       f'It took:{datetime.datetime.now() - start_time}')


@bot.message_handler(content_types=['photo'])
def download_photo(message):
    '''
    Function handles photo content type message. Donloads a photo and stores it in
    {img_path}/{message.from_user.id}/{message.from_user.id}_UUID.jpg
    :param message: object message from Telegram
    :return: Function send messages to user within bot
    '''
    start_time = datetime.datetime.now()
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    img = f'{img_path}/{message.from_user.id}'
    if not os.path.exists(img):
        os.makedirs(img)
    file_name = f'{message.from_user.id}_{str(uuid.uuid4())}.jpg'
    # TODO adding try and except
    with open(r"{path}/{filename}.jpg".format(path=img, filename=f'{file_name}',
                                              user_id=message.from_user.id), 'wb') as new_file:
        new_file.write(downloaded_file)
    logger.info(f"{__name__} Photo downloaded to {img} as {file_name}")
    if user_reply_check(message.from_user.id):
        # TODO adding try and except
        bot.reply_to(message, f'Your photo:\nfileId:{fileID}\nFile Info:{file_info}\n'
                              f'saved with an Unique name in jpg format\nIt took'
                              f':{datetime.datetime.now() - start_time}')
    else:
        # TODO adding try and except
        bot.send_message(chat_id=message.chat.id,
                         text=f'Your photo:\nfileId:{fileID}\nFile Info:{file_info}\n'
                              f'saved with an Unique name in jpg format\nIt took'
                              f':{datetime.datetime.now() - start_time}')

# TODO adding regex validation for input preventing injections.
# TODO adding parsing of the input from special charachters along with right and left trims.
# TODO adding validation preventing code with white space input or another abnormal input.


@bot.message_handler(content_types=['text'])
def text_message(message):
    '''
    Function handles text content type message. invokes a function database_check.
    :param message: object message from Telegram
    :return: Function send messages to user within bot
    '''
    start_time = datetime.datetime.now()
    logger.info(f"{__name__} Main text content type handle executing")
    if user_reply_check(message.from_user.id):
        # TODO adding try and except
        bot.reply_to(message, f'{database_check(message.text,message.from_user.id)}\n'
                              f'It took: {datetime.datetime.now() - start_time}')
    else:
        # TODO adding try and except
        bot.send_message(chat_id=message.chat.id, text=f'{database_check(message.text,message.from_user.id)}\n'
                                                       f'It took: {datetime.datetime.now() - start_time}')


def main():
    # TODO adding try and except
    '''
    :return: No return
    Function main activates bot polling
    '''
    bot.polling()


if __name__ == '__main__':
    main()
