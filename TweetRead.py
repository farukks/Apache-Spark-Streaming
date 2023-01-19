#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tweepy


# In[ ]:


from tweepy import Stream


# In[ ]:


import socket


# In[ ]:


import json


# In[ ]:


keys=open('C:\\twitterKeys.txt','r').read().splitlines()


# In[ ]:


consumer_key    = keys[0]
consumer_secret = keys[1]
access_token    = keys[2]
access_secret   = keys[3]


# In[ ]:


class Tweets(Stream):

    def __init__(self, *args,csocket):
        super().__init__(*args)
        self.client_socket=csocket
 
    def on_data(self, data):
        try:  
            file = json.loads( data )
            print( file['text'].encode('utf-8') )
            self.client_socket.send( file['text'].encode('utf-8') )
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


# In[ ]:


def sendData(c_socket):
    twitter_stream=Tweets(
       consumer_key, consumer_secret,access_token, access_secret,
        csocket=c_socket
    )    
    twitter_stream.filter(track=['zamgeldi'])


# In[ ]:


if __name__ == "__main__":
    s = socket.socket()         
    host = "FfarukK"     
    port = 6666            
    s.bind((host, port))       

    print("Port: %s" % str(port))

    s.listen(5)                
    c, addr = s.accept()        

    print("Received request from: " + str(addr))

    sendData(c)


# In[ ]:





# In[ ]:




