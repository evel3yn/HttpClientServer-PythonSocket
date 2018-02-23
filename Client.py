# Name: Simin Wen
# VID: wens3
import socket
import sys
from urllib.parse import urlparse
# create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# if specify the request type is HEAD
if len(sys.argv) == 3 and sys.argv[2] == 'HEAD':
    method = 'HEAD'
# if not specify request type or request type is GET
elif len(sys.argv) == 2 or sys.argv[2] == 'GET':
    method = 'GET'
# if request type is not supported
else:
    method = sys.argv[2]
# URL
o = urlparse(sys.argv[1])
# host
h = o.hostname
try:
    # converted host name to IP address
    remote_ip = socket.gethostbyname(h)

except socket.gaierror:
    # could not resolve
    sys.exit()
# Connect to remote server
sock.connect((remote_ip, o.port))
# request
message = method + " " + sys.argv[1]+" HTTP/1.1\r\nHost: " + h + "\r\n\r\n"
# send request
sock.sendall(message.encode('utf-8'))
# receive response
result = sock.recv(10000)
# decode response
result = result.decode('UTF-8', 'strict')
# close socket
sock.close()
print(result)

