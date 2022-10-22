import sqlite3
dbconnect = sqlite3.connect(r'c:\Users\Ilya Polonsky\Desktop\users9.db3')
pointer = dbconnect.cursor()
pointer.execute('CREATE TABLE IF NOT EXISTS user_bot (USER_BOT_ID TEXT,VIEW_URL TEXT,DOWNLOAD_URL TEXT)')
value1 = 'xczxc9777xczxczxcxzczxczxc7779999465465464654999'
value2 = '55555zqqqqqz654654654zzz'
value3 = 'xxcxcxzczxcxx66465465454654654'
query = ("INSERT INTO user_bot values (?,?,?)")
#pointer.execute(query,[value1,value2,value3])
#dbconnect.commit()
results = pointer.execute("SELECT * FROM user_bot WHERE VIEW_URL = 'uuu'").fetchall()
for y in results:
    print(y,type(results))
if not results:
    print('EMPTY')
pointer.close()
