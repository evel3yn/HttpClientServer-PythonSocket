# Name: Simin Wen
# VID: wens3
import socket
import sys
import os
from urllib.parse import urlparse
from time import gmtime, strftime


# functions
# get the middle string, actually the URL
def getMidStr(d, startStr, endStr):
    startIndex = d.index(startStr)
    if startIndex >= 0:
        startIndex += len(startStr)
        endIndex = d.index(endStr)
        return d[startIndex:endIndex]

# return the response of the GET request
# param:
#   getRequestPath: URL of client request
#   direc: directory from server paramater
def responseGetRequest(getRequestPath, direc):
    o = urlparse(getRequestPath)
    # if the file is existed in the directory
    if os.path.exists(direc) and os.path.isfile(direc):
        # path without '/' and the blank in the end
        subO = o.path[1:-1]
        # if file is in the directory
        if subO in direc:
            msgSendtoClient = "HTTP/1.1 200 OK\n"
            # Date
            t = strftime("%a, %d %b %Y %H:%M:%S %Z", gmtime())
            msgSendtoClient += "Data: " + t + "\n"
            # Server
            msgSendtoClient += "Server: " + "SiminWen" + "\n"
            # rewrite the D:/abc.txt to D:\\abc.txt (to absolute path)
            absdir = os.path.abspath(direc)
            # able to read large file
            fd = ""
            with open(absdir, 'r') as f:
                for line in f:
                    fd += line
            # content length
            msgSendtoClient += "Content-Length:" + str(len(fd)) + "\n"
            msgSendtoClient += "\r\n\r\n"
            msgSendtoClient += fd
            mi = 234

        else:
            msgSendtoClient = "HTTP/1.1 404 Not Found\r\n\r\n"
            msgSendtoClient += "Not Found"
            # Date
            t = strftime("%a, %d %b %Y %H:%M:%S %Z", gmtime())
            msgSendtoClient += "Data: " + t + "\n"
            # Server
            msgSendtoClient += "Server: " + "SiminWen" + "\n"
            # content length
            msgSendtoClient += "Content-Length: 0" + "\n"
            msgSendtoClient += "\r\n\r\n"
    return msgSendtoClient


def responseHeadRequest(getRequestPath, direc):
    o = urlparse(getRequestPath)
    # if the file is existed in the directory
    if os.path.exists(direc) and os.path.isfile(direc):
        # path without '/' and the blank in the end
        subO = o.path[1:-1]
        # if file is in the directory
        if subO in direc:
            m = "HTTP/1.1 200 OK\n"
            # Date
            t = strftime("%a, %d %b %Y %H:%M:%S %Z", gmtime())
            m += "Data: " + t + "\n"
            # Server
            m += "Server: " + "SiminWen" + "\n"
            # rewrite the D:/abc.txt to D:\\abc.txt (to absolute path)
            absdir = os.path.abspath(direc)
            # able to read large file
            fd = ""
            with open(absdir, 'r') as f:
                for line in f:
                    fd += line
            # content length
            m += "Content-Length:" + str(len(fd)) + "\n"
            m += "\r\n\r\n"

        else:
            m = "HTTP/1.1 404 Not Found\r\n\r\n"
            # Date
            t = strftime("%a, %d %b %Y %H:%M:%S %Z", gmtime())
            m += "Data: " + t + "\n"
            # Server
            m += "Server: " + "SiminWen" + "\n"
            # content length
            m += "Content-Length: 0" + "\n"
            m += "\r\n\r\n"
    return m


# system param
port = sys.argv[1]
directory = sys.argv[2]
# instantiate a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the IP and port
server_add = ('localhost', int(port))
sock.bind(server_add)
# listen to at most 1 client at the same time
sock.listen(1)
# infinite loop
while True:
    connection, addr = sock.accept()
    try:
        data = connection.recv(1024)
        data = data.decode('UTF-8', 'strict')
        if data:
            # send the request info
            requestType = data[0:data.find(" ")]
            # is GET or HEAD
            if requestType == "GET":
                ret = responseGetRequest(getMidStr(data, 'GET ', 'HTTP/1.1'), directory)
            elif requestType == "HEAD":
                ret = responseHeadRequest(getMidStr(data, 'HEAD ', 'HTTP/1.1'), directory)
            else:
                ret = msgSendtoClient = "HTTP/1.1 503 Service Unavailable"
            ret = ret.encode('UTF-8')
            connection.sendall(ret)
    finally:
        connection.close()
