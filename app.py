import telebot,sqlite3,utils
from utils import search_download_youtube_video
from loguru import logger
from os import environ

#dbconnect = sqlite3.connect(r'c:\Users\Ilya Polonsky\Desktop\users9.db3')
#pointer = dbconnect.cursor()
#pointer.execute('CREATE TABLE IF NOT EXISTS user_bot (USER_BOT_ID TEXT,VIEW_URL TEXT,DOWNLOAD_URL TEXT)')
'''
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
'''
'''
text, audio, document, photo, sticker, video, video_note, voice, location, contact, new_chat_members, left_chat_member,
new_chat_title, new_chat_photo, delete_chat_photo, group_chat_created, supergroup_chat_created, channel_chat_created,
migrate_to_chat_id, migrate_from_chat_id, pinned_message, web_app_data
'''

bot = telebot.TeleBot('5683443990:AAHvz0aQwW8ZI92KqIEnxw-6hh2jxy_6MDw') # creating a instance
@bot.message_handler(content_types=['audio','voice','location'])
def not_relevant(message):
    bot.reply_to(message,'Not Relevant')
def main():
    bot.polling() # looking for message

if __name__ == '__main__':
    main()
