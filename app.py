import telebot
from utils import search_download_youtube_video
from loguru import logger


class Bot:

    def __init__(self, token):
        self.bot = telebot.TeleBot(token, threaded=False)
        self.bot.set_update_listener(self._bot_internal_handler)

        self.current_msg = None

    def _bot_internal_handler(self, messages):
        """Bot internal messages handler"""
        for message in messages:
            self.current_msg = message
            self.handle_message(message)

    def start(self):
        """Start polling msgs from users, this function never returns"""
        logger.info(f'{self.__class__.__name__} is up and listening to new messages....')
        logger.info('Telegram Bot information')
        logger.info(self.bot.get_me())

        self.bot.infinity_polling()

    def send_text(self, text):
        self.bot.send_message(self.current_msg.chat.id, text)

    def send_text_with_quote(self, text, message_id):
        self.bot.send_message(self.current_msg.chat.id, text, reply_to_message_id=message_id)

    def is_current_msg_photo(self):
        return self.current_msg.content_type == 'photo'

    def download_user_photo(self, quality=0):
        """
        Downloads photos sent to the Bot to `photos` directory (should be existed)
        :param quality: integer representing the file quality. Allowed values are [0, 1, 2, 3]
        :return:
        """
        if self.current_msg.content_type != 'photo':
            raise RuntimeError(f'Message content of type \'photo\' expected, but got {self.current_msg["content_type"]}')

        file_info = self.bot.get_file(self.current_msg.photo[quality].file_id)
        pic_file = self.bot.download_file(file_info.file_path)

        # TODO save `data` as a photo in `file_info.file_path` path
        with open('myapp/%s' % self.current_msg.photo[quality].file_id,'wb') as new_file:
            new_file.write(pic_file)

    def handle_message(self, message):
        """Bot Main message handler"""
        logger.info(f'Incoming message: {message}')
        self.send_text(f'Your original message: {message.text}')


class QuoteBot(Bot):
    def handle_message(self, message):
        if not message.text.startswith('noQuote'):
            self.send_text_with_quote(message.text, message_id=message.message_id)


class YoutubeBot(Bot):
    def handle_message(self, message):
        """Results = json.loads(search_download_youtube_video(message.text))
         self.send_text(f"Video(s) URL: {Results['url']}") """
        if self.is_current_msg_photo():
            self.download_user_photo()
        elif message.text.startswith('getvid'):
            self.send_text(f'Video URL: {search_download_youtube_video(message.text[6:])}')


    pass


if __name__ == '__main__':
    with open('.telegramToken') as f:
        _token = f.read().rstrip()

    my_bot = YoutubeBot(_token)
    my_bot.start()


