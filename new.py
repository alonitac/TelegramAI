from pythonping import ping
import sys
import os
import mysql.connector
from mysql.connector import errorcode

try:
  cnx = mysql.connector.connect(
  host="192.168.20.200",
  user="ilya",
  password="ilya",
  auth_plugin='mysql_native_password'
)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    m=f"Something is wrong with your user name or password {err.errno}"
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    m=f"Database does not exist {err.errno}"
  else:
    print(err)
else:
  cnx.close()

with open('/img/file.txt', 'w') as sys.stdout:
    print(f'FROM ENV\n{os.environ.get("MYSQL_IP")}\n{os.environ.get("MYSQL_ROOT_USER")}\n'
          f'{os.environ.get("MYSQL_ROOT_PASSWORD")}\n{os.environ.get("API")}\n')
    print(f'GOOGLE PING\n{ping("8.8.8.8")}')
    print(f'SQL PING\n{ping("192.168.20.200")}')
    print(mysql.connector.Error)
#    print(f'FROM SQL\n{mycursor.fetchone()}')