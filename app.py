import telebot,sqlite3,utils
from utils import search_download_youtube_video
from loguru import logger
from os import environ

#dbconnect = sqlite3.connect(r'c:\Users\Ilya Polonsky\Desktop\users9.db3')
#pointer = dbconnect.cursor()
#pointer.execute('CREATE TABLE IF NOT EXISTS user_bot (USER_BOT_ID TEXT,VIEW_URL TEXT,DOWNLOAD_URL TEXT)')

class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token, threaded=False)
        self.bot.set_update_listener(self._bot_internal_handler)
        self.current_msg = None
        self.dbname = environ.get('DB_NAME')

    def _bot_internal_handler(self, messages):
        """Bot internal messages handler"""
        for message in messages:
            self.current_msg = message
            self.handle_message(message)

    def start(self):
        """Start polling msgs from users, this function never returns"""
        print(environ.get('MYSQL_IP'),environ.get('MYSQL_ROOT_USER'),
           environ.get('MYSQL_ROOT_PASSWORD'), environ.get('API'))
        logger.info(f'{self.__class__.__name__} is up and listening to new messages....')
        logger.info('Telegram Bot information')
        logger.info(self.bot.get_me())
        self.send_text('Hi,\nI am a bot that part of INT Devops 2022')
        self.bot.infinity_polling()

    def send_text(self, text):
        self.bot.send_message(self.current_msg.chat.id, text)

    def send_text_with_quote(self, text, message_id):
        '''self.bot.send_message(self.current_msg.chat.id, text, reply_to_message_id=message_id)'''
        self.bot.send_message(self.current_msg.chat.id, text, reply_to_message_id=message_id)

    def is_current_msg_photo(self):
        return self.current_msg.content_type == 'photo'

    def download_user_photo(self, quality=0):
        """
        Downloads photos sent to the Bot to `photos` directory (should be existed)
        :param quality: integer representing the file quality. Allowed values are [0, 1, 2, 3]
        :return:
        image = update.message.photo[-1]
		path = '{1}download/{0}.jpg'.format(image.file_id, qr_folder_path)
		#print(image)
		newFile = bot.getFile(image.file_id)
		newFile.download(path)
		qr = account_by_qr(path)
        """
        if self.current_msg.content_type != 'photo':
            raise RuntimeError(f'Message content of type \'photo\' expected, but got {self.current_msg["content_type"]}')
        # TODO save `data` as a photo in `file_info.file_path` path

    def handle_message(self, message):
        """Bot Main message handler"""
        logger.info(f'Incoming message: {message}')
        logger.info(f'user_id:{message.from_user.id}')
        if message.content_type == 'text':
            #query = f"SELECT link_download FROM {self.dbname} WHERE search_phrase = 'strangeshithappened'"
            #self.mycursor.execute(query)
            self.send_text(f'Your link: '
                           f'{utils.search_download_youtube_video(message.text)}')
            if '$please don\'t quote' in message.text:
                self.send_text(f'Your link: '
                               f'{utils.search_download_youtube_video(message.text, user_id=message.from_user.id)}')
            else:
                self.send_text_with_quote(utils.search_download_youtube_video(message.text,
                                                                              user_id=message.from_user.id),
                                          message_id=message.message_id)
            self.send_text(f'type: '
                           f'{self.current_msg.content_type}')



class QuoteBot(Bot):
    '''def handle_message(self, message):
        if message.text != 'Don\'t quote me please':
            self.send_text_with_quote(utils.search_download_youtube_video(message.text, user_id=message.from_user.id),
                                      message_id=message.message_id)
'''

class YoutubeBot(Bot):
    pass


if __name__ == '__main__':
    my_bot = Bot(environ.get('API'))
    my_bot.start()


