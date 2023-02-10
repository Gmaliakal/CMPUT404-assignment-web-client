#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse


def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    # def shutdown(self):
    #     self.socket.shutdown(socket.SHUT_RDWR) # shut down the server
    #     #self.socket.close()

    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()


    def requestrecieve(self,request):

        # send and recieve the request #
        self.sendall(request)
        information = self.recvall(self.socket)
        self.close()

        # return code and response
        code = int(information.split(" ")[1])
        body = information.split("\r\n\r\n")[1]

        return code,body



    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('#utf-8')


    def GET(self, url, args=None):
        body = None
        o = urlparse(url);
        path = o.path
        try:
            port = int(o.netloc.split(":")[1])
        except:
            port = 80

        try:
            host = o.netloc.split(":")[0] 
        except:
            host = o.netloc


       # connect to host
        try:
            self.connect(host,port)
             # request header for get method
            if path != "":
                request = "GET " + path + " HTTP/1.1\r\nHOST:"+host+"\r\nContent-Encoding: gzip\r\nConnection: close\r\nAccept: application/json\r\n\r\n"
            else:
                #path = str(/)
                request = "GET / HTTP/1.1\r\nHOST:" + host + "\r\nContent-Encoding: gzip\r\nConnection: close\r\nAccept: application/json\r\n\r\n"

            code, body = self.requestrecieve(request)
            # # send and recieve the request #
            # self.sendall(request)
            # information = self.recvall(self.socket)
            # self.close()
            #
            #
            #
            # # return code and response
            # code = int(information.split(" ")[1])
            # body = information.split("\r\n\r\n")[1]

        except:
            code = 404

        return HTTPResponse(code, body)


    def POST(self, url, args=None):
        # code = 500
        # body = ""

        port = 80
        code = 500
        body = None
        path = "/"

        o = urlparse(url);


        try:
            port = int(o.netloc.split(":")[1])
        except:
            port = 80

        try:
            host = o.netloc.split(":")[0] 
        except:
            host = o.netloc
            
        path = o.path
        #host = o.hostname

    
      
       # connect to host #
        try:
            self.connect(host,port)

            # Formatting the arguments as part of the body of the post request
            if args is not None:
                argslen = len(args)
                i=1
                query=""
                for key in args:
                    if argslen!=i:
                        query = query + str(key) + "=" + str(args[key]) + "&"
                    else:
                        query = query + str(key) + "=" + str(args[key])
                    i += 1
                querylen = str(len(query))


                request = "POST "+ path + " HTTP/1.1\r\nHOST: " + host + "\r\n"+"Content-Type: application/x-www-form-urlencoded\r\nContent-Encoding: gzip\r\nConnection: close\r\nAccept: application/json\r\nContent-Length: " + querylen + "\r\n\r\n" + query
            else:
                request = "POST " + path + " HTTP/1.1\r\nHOST: " + host + "\r\n" + "Content-Type: application/x-www-form-urlencoded\r\nContent-Encoding: gzip\r\nConnection: close\r\nAccept: application/json\r\nContent-Length: " + "0" + "\r\n\r\n"


            code,body=self.requestrecieve(request)
            # # send and recieve the request #
            # self.sendall(request)
            # information = self.recvall(self.socket)
            # self.close()
            #
            # # return code and response
            #
            # code = int(information.split(" ")[1])
            # body = information.split("\r\n\r\n")[1]

        except:
            code = 404

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if command == "POST":
            return self.POST( url, args )
        else:
            return self.GET( url, args )


if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if len(sys.argv) <= 1:
        help()
        sys.exit(1)
    elif len(sys.argv) == 3:
        print(client.command(sys.argv[2], sys.argv[1]))
    else:
        print(client.command(sys.argv[1]))
