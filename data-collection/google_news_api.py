'''
Get News from 9 sources through google news api
'''

from newsapi import NewsApiClient
import csv
import pandas as pd
#Setting the google news api user key
newsapi = NewsApiClient(api_key='2fd12bd819ec4bd79434f7b150f0d4ba')
#getting the dates that are targeted to scape news from
dates = []
#The limit is getting the news 1 month back
[dates.append('2020-02-'+ str(i)) for i in range(11,30)]
#specifying the 9 targeted sources
media_list = ['cnn', 'cnbc','reuters', 'the-wall-street-journal','bloomberg',
              'the-washington-post','the-verge','vice-news','buzzfeed']


def get_news(media_name):
    '''
    Getting the news from the google news api
    '''
    all_articles = []
    for j in dates:
        one_article = newsapi.get_everything(q='coronavirus',
                                             sources= media_name,
                                             from_param= j,
                                             to= j,
                                             language='en',
                                             sort_by='popularity',
                                             page=1)
        all_articles.append(one_article)
    x = all_articles
    return x




def write_news(media_list):
    '''
    Getting the news from the targeted media source list,
    then return cvs files for each source.
    '''
    for s in media_list:
        x = get_news(s)
        with open(str(s) + 'news_data.csv', 'w', encoding="utf-8") as csv_file:
            newswriter = csv.writer(csv_file)
            newswriter.writerow(['title_text', 'Time_stamp','source'])
            for arti in x:
                for k in arti['articles']:
                    newswriter.writerow([k['title'],k['description'],
                                         k['publishedAt'], s])


##################
##Execution

write_news(media_list)
