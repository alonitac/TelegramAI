from app import YoutubeBot



token = open(".telegramToken").read()

YB = YoutubeBot(token = token)
YB.start()




