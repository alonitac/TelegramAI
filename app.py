import telebot
from loguru import logger
import time
from utils import search_download_youtube_video


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

    def send_welcome(message):
        bot.reply_to(message, "Howdy, how are you doing?")

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

    def download_user_photo(self, quality=3):
        """
        Downloads photos sent to the Bot to `photos` directory (should be existed)
        :param quality: integer representing the file quality. Allowed values are [0, 1, 2, 3]
        :return:
        """
        self.send_text("Downloading image")
        if self.current_msg.content_type != 'photo':
            raise RuntimeError(
                f'Message content of type \'photo\' expected, but got {self.current_msg["content_type"]}')

        file_info = self.bot.get_file(self.current_msg.photo[quality].file_id)
        data = self.bot.download_file(file_info.file_path)
        filed = open(file_info.file_path, "wb")
        filed.write(data)
        filed.close()

        # TODO save `data` as a photo in `file_info.file_path` path

    def handle_message(self, message):
        """Bot Main message handler"""
        logger.info(f'Incoming message: {message}')
        self.send_text(f'Your original message: {message.text}')


class QuoteBot(Bot):
    def handle_message(self, message):
        if message.text != 'Dont quote me please':
            self.send_text_with_quote(message.text, message_id=message.message_id)


class YoutubeBot(Bot):

    def handle_message(self, message):
        if self.is_current_msg_photo():
            self.download_user_photo()


        elif "download video" in message.text.lower():
            self.send_text("Searching Video: {}".format(message.text.lower().replace('download video', '')))
            ytb = search_download_youtube_video(message.text.lower().replace('download video', ''))
            for video in ytb:
                self.send_text("Video Name: {}".format(video["filename"]))
                self.send_text("Video url: {}".format(video["url"]))
        else:
            self.send_text(f'Your original message: {message.text}')

    if __name__ == '__main__':
        with open('.telegramToken') as f:
            _token = f.read()

        my_bot = Bot(_token)
        my_bot.start()