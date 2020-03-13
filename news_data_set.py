#!/usr/bin/env python
# coding: utf-8

# In[2]:


from newsapi import NewsApiClient
import json
import csv
import pandas as pd
newsapi = NewsApiClient(api_key='2fd12bd819ec4bd79434f7b150f0d4ba')
dates = []
for i in range(18,30):
    date = '2020-02-' + str(i)
    dates.append(date)

media_list = ['cnn', 'cnbc','reuters', 'the-wall-street-journal','bloomberg','the-washington-post','the-verge','vice-news','buzzfeed']


# In[3]:


def get_news(media_name):
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


# In[4]:


for s in media_list:
    x = get_news(s)
    with open(str(s) + 'news_data.csv', 'w') as csv_file:
        newswriter = csv.writer(csv_file)
        newswriter.writerow(['title_text', 'Time_stamp','source'])
        for arti in x:
            for k in arti['articles']:
                newswriter.writerow([k['title'], k['publishedAt'], s])


# In[ ]:


for i in range(1,10):
    date = '2020-03-0'+str(i)
    dates.append(date)
for i in range(10,16):
    date = '2020-03-' + str(i)
    dates.append(date)


# In[ ]:





# In[ ]:




