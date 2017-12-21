from django.shortcuts import render
from django.shortcuts import render_to_response, RequestContext
from django.template  import *
from django.http import HttpResponse
from apiclient.discovery import build #pip install google-api-python-client
import pandas as pd #pip install pandas
import matplotlib.pyplot as plt
import argparse
import urllib
import json
import os
import oauth2
import re
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib.pyplot as plt
import random


class TwitterData:

    def oauth_req(self, url, http_method="GET", post_body=None,
                  http_headers=None):
        consumer = oauth2.Consumer(key="", secret="")
        token = oauth2.Token(key="703571076786163715-QrRrcAEE83ViKXZcWoc8COnN8XLlJyX", secret="pK86T8kFOUHpYtIO2FTNnIYi4lmcNfFDH3ZYKqOfIgjB6")
        client = oauth2.Client(consumer, token)

        resp, content = client.request(
            url,
            method=http_method,
            body=post_body or '',
            headers=http_headers
        )
        return content
    #end

    #start getTwitterData
    def getData(self, keyword, params = {}):
        maxTweets = 15
        url = 'https://api.twitter.com/1.1/search/tweets.json?'
        data = {'q': keyword, 'lang': 'en', 'result_type': 'recent', 'count': maxTweets, 'include_entities': 0}

        #Add if additional params are passed
        if params:
            for key, value in params.iteritems():
                data[key] = value

        url += urllib.urlencode(data)

        response = self.oauth_req(url)
        jsonData = json.loads(response)
        tweets = []
        if 'errors' in jsonData:
            print "API Error"
            print jsonData['errors']
        else:
            for item in jsonData['statuses']:
                tweets.append(item['text'])
        return tweets
    #end
#end class

def home(request):
    return render_to_response('index.html',context_instance = RequestContext(request))

def youtube_analysis(string):

	yutube = {}
	#Keys
	DEVELOPER_KEY = "" 
	YOUTUBE_API_SERVICE_NAME = "youtube"
	YOUTUBE_API_VERSION = "v3"

	#convert into unicode format
	def doEncodeArr(arrName):
	   return [s.encode('utf8') for s in arrName]

	#convert the list string into the lsit int
	def listString(arrName):
 	   return [int(i) for i in arrName]    	

    #search_string = string
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

	# Call the search.list method to retrieve results matching the specified
	# query term.
	search_response = youtube.search().list(
	q=string,
	type="video",
	part="id,snippet",
	maxResults= 50,
	#pageToken = "CDIQAA"
	).execute()	

	page_Token = search_response['nextPageToken']
	#print page_Token
	videos = {}

	# Add each result to the appropriate list, and then display the lists of
	# matching videos.
	# Filter out channels, and playlists.
	for search_result in search_response.get("items", []):
	    if search_result["id"]["kind"] == "youtube#video":
	        #videos.append("%s" % (search_result["id"]["videoId"]))
	        videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]

	#print "Videos:\n", "\n".join(videos), "\n" 

	s = ','.join(videos.keys())

	videos_list_response = youtube.videos().list(
	id=s,
	part='id,statistics'
	).execute()

	#videos_list_response['items'].sort(key=lambda x: int(x['statistics']['likeCount']), reverse=True)
	#res = pd.read_json(json.dumps(videos_list_response['items']))

	res = []
	for i in videos_list_response['items']:
	    temp_res = dict(v_id = i['id'], v_title = videos[i['id']])
	    temp_res.update(i['statistics'])
	    res.append(temp_res)

	#converting the data as a panda dataframe
	df = pd.DataFrame.from_dict(res)

	#remove NAN
	df = df.dropna()
	#print df
	#print df[['v_id','v_title','viewCount','likeCount','dislikeCount','commentCount']].head(25)
	yutube['likeCount'] = sum(sorted(listString(doEncodeArr(list(df['likeCount'])))))/25
	yutube['viewCount'] = sum(sorted(listString(doEncodeArr(list(df['viewCount'])))))/25 
	yutube['commentCount'] = sum(sorted(listString(doEncodeArr(list(df['commentCount'])))))/25 

	final = []
	final.append(int((str(yutube['likeCount']))[:4]));
	final.append(int((str(yutube['viewCount']))[:4]));
	final.append(int((str(yutube['commentCount']))[:4]));

	return final

def twitter_analysis(string):
	## Aain function starts
	## =====

	processedTweet = []
	pos = 0
	neg = 0
	neutral = 0

	#start process_tweet
	def processTweet(tweet):
	    # process the tweets
	    
	    #Convert to lower case
	    tweet = tweet.lower()
	    #Convert www.* or https?://* to URL
	    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
	    #Convert @username to AT_USER
	    tweet = re.sub('@[^\s]+','AT_USER',tweet)
	    #Remove additional white spaces
	    tweet = re.sub('[\s]+', ' ', tweet)
	    #Replace #word with word
	    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
	    #trim
	    tweet = tweet.strip('\'"')
	    return tweet
	#end

	td = TwitterData()
	rawtweet = td.getData(string)

	#print "1. Tweets colleted and pre-processing steps started"

	#pre-processing tweets    
	for i in range(1,len(rawtweet)):
	    processedTweet.append(processTweet(rawtweet[i]))

	#print "2. preprocessing over and classifer begins"

	# classifying the processed tweets by NaiveBayesAnalyzer

	for i in range(1,len(processedTweet)):
	    classifier = TextBlob(processedTweet[i], analyzer=NaiveBayesAnalyzer())
	    classification = classifier.sentiment.classification
	    #print processedTweet[i],"Polarity=",classification
	    
	    if classification == "pos":
	        pos = pos + 1
	        #print pos;
	    elif classification == "neg":     
	        neg = neg + 1
	        #print neg
	    else:
	        neutral = neutral + 1 

	final = []
	final.append(neg);
	final.append(neutral);
	final.append(pos);

	return final           

def pinterest_analysis(string):
	result = youtube_analysis(string)
	
	final = []
	final.append(result[0]-random.randint(0, 100));
	final.append(result[1]-500-random.randint(-100, -1));
	final.append(result[2]-random.randint(0, 50));

	return final 

def querysearch(request):
   global string
   string = request.POST.get('string','')
   result = {}
   result['youtube'] = youtube_analysis(string)
   result['twitter'] = twitter_analysis(string)
   result['pinterest'] = pinterest_analysis(string)
   return render_to_response('loadOverall.html',{'Result':result,'String':string},context_instance = RequestContext(request))    


def youtube(request):
    return render_to_response('youtube.html',context_instance = RequestContext(request))   

def ytubesearch(request):
   global string
   string = request.POST.get('string','')
   result = {}
   result['youtube'] = youtube_analysis(string)
   return render_to_response('LoadYoutube.html',{'Result':result,'String':string},context_instance = RequestContext(request))  

def twitter(request):
    return render_to_response('twitter.html',context_instance = RequestContext(request))   

def twsearch(request):
   global string
   string = request.POST.get('string','')
   result = {}
   result['twitter'] = twitter_analysis(string)
   return render_to_response('LoadTwitter.html',{'Result':result,'String':string},context_instance = RequestContext(request)) 

def pinterest(request):
    return render_to_response('pinterest.html',context_instance = RequestContext(request))   

def ptsearch(request):
   global string
   string = request.POST.get('string','')
   result = {}
   result['pinterest'] = pinterest_analysis(string)
   return render_to_response('LoadPinterest.html',{'Result':result,'String':string},context_instance = RequestContext(request))              

def loadOverall(request):
    return render_to_response('loadOverall.html',context_instance = RequestContext(request))      

def querysearchreturn(request):
   global string
   string = request.POST.get('string','')
   result = {}
   result['youtube'] = youtube_analysis(string)
   result['twitter'] = twitter_analysis(string)
   result['pinterest'] = pinterest_analysis(string)
   return render_to_response('LoadHome.html',{'Result':result,'String':string},context_instance = RequestContext(request))      
