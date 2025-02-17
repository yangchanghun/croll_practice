import pandas
from googleapiclient.discovery import build
import time

A = time.time()

# url_id = ['KH_pqxS5Qkc','PGFoX6szxxU','3s3G4iKVHDY','dpL7rB7Uh3A','jVKQjQyOjYk','oiLIcWcVzOM','HpySIRXYLqw','R-TNddvIJt0','e8-mlZKtjG8','ooWegesHKwY']
url_id = ['KH_pqxS5Qkc']

def croll_youtube(i):
    api_key = 'API키입력력'
    video_id = i
    comments = list()
    api_obj = build('youtube', 'v3', developerKey=api_key)
    response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100).execute()
    while response:
        for item in response['items']:
            if len(comments) >200:
                break
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([comment['textDisplay'], comment['authorDisplayName'], comment['publishedAt'], comment['likeCount']])
    
            if item['snippet']['totalReplyCount'] > 0:
                for reply_item in item['replies']['comments']:
                    reply = reply_item['snippet']
                    comments.append([reply['textDisplay'], reply['authorDisplayName'], reply['publishedAt'], reply['likeCount']])
    
        if 'nextPageToken' in response:
            response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, pageToken=response['nextPageToken'], maxResults=100).execute()
        else:
            break
    df = pandas.DataFrame(comments)
    df.to_excel(f'results{video_id}.xlsx', header=['comment', 'author', 'date', 'num_likes'], index=None)

for i in url_id:
    croll_youtube(i)

B = time.time()

print(B-A)