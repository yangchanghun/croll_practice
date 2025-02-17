import pandas
from googleapiclient.discovery import build
from multiprocessing.dummy import Pool as ThreadPool
import time
A = time.time()
url_id = ['KH_pqxS5Qkc','ZoZ7eWAe0dg','Sz1YQ4_JZZw','1nzCPoTicDI']

def croll_youtube(i):
    api_key = 'AIzaSyBDLTQxXLU4SU0WDnj9f-BhrS7smGNngo8'
    video_id = i
    comments = list()
    api_obj = build('youtube', 'v3', developerKey=api_key)
    response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100).execute()
    A = 1
    while response:
        A += 1
        for item in response['items']:
            if len(comments) >500:
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
    df.to_excel(f'results{video_id}{A}.xlsx', header=['comment', 'author', 'date', 'num_likes'], index=None)




pool = ThreadPool(12)

pool.map(croll_youtube,url_id)
pool.close()
pool.join()

B = time.time()
print(B-A)