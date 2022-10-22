from pythonping import ping
import sys
with open('/img/file.txt', 'w') as sys.stdout:
    print(f'GOOGLE PING\n{ping("8.8.8.8")}')
    print(f'SQL PING\n{ping("192.168.20.200")}')