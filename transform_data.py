import re
import pandas as pd
import wordcloud #Makes word clouds
import numpy as np #For divergences/distances
import seaborn as sns #makes our plots look nicer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt 

stopwords = set(['a', 'also', 'an', 'and', 'are', 'as', 'at', 'be',
                 'but', 'by', 'for', 'from', 'have','has','he', 'how', 'i', 'ii', 'iii','in',
                  'in', 'is', 'it','its','it\'s','not','of','on','or',
                 's', 'so','such','that', 'the', 'their', 'this','through','to',
                 'was', 'we', 'were', 'which', 'will', 'with','yet','you'])

###############
###############
#Functions

def read_csv_files(path,list_of_col):
    import os
    import pandas as pd
    files = os.listdir(path)
    df = pd.DataFrame()
    for i in files:
        if i[-3:] == "csv":
            df_i = pd.read_csv(path+i,encoding = "ISO-8859-1",header=None)
            df = pd.concat([df, df_i],axis=0)
    df = df.dropna(axis=0)
    df.reset_index(drop=True, inplace=True)
    [df.rename(columns={i:list_of_col[i]}, inplace=True) for i in list(df.columns)]
    return df


def split_time(df,column_name):
    '''
    Split date and time-of-day
    '''
    import re
    #import datetime
    d = df[column_name].apply(lambda x : re.sub(r'[^0-9]', ' ',x).strip().split(' '))
    df['date'] = d.apply(lambda x :'-'.join(x[:3]))
    df['date']= pd.to_datetime(df['date'])
    #df['time_of_day'] = d.apply(lambda x :':'.join(x[3:]))
    df = df.drop([column_name], axis=1)
    return df

# Generate a list of words
def word_tokenize(string):
    list_ = []
    list_of_string = string.split()
    for n in list_of_string:
        #string_ = re.sub('\W#', '', n).lower()
        string_ = re.sub('\W', '', n).lower()
        string_ = re.sub('^https', '',string_)
        if len(string_)> 0 and (string_ not in stopwords):
            list_.append(string_)
    return list_
#word_tokenize(df['text'][1])


def get_top_K_hashtag(df,K=None):
    hashtags = {}
    for m in range(len(df)):
        for hash_tag in df['all_hashtags'].loc[m].split(','):
            string = hash_tag.strip(' []\'\'').lower()
            if string not in hashtags:
                hashtags[string] = 1   
            else:
                hashtags[string] += 1
    tag_counts = sorted(hashtags.items(), key = lambda x : x[1], reverse = True)
    top_K_tags = tag_counts[:K]
    return top_K_tags

def get_top_K_words(df_text,K=None,pairs=None):
    word_count = {}
    for i in df_text:
        tokens = word_tokenize(i)
        if pairs:
            for j in range(len(tokens)-1):
                word_count[(tokens[j],tokens[j+1])] = word_count.get((tokens[j],tokens[j+1]),0) + 1
        else:
            for j in range(len(tokens)):
                word_count[tokens[j]] = word_count.get(tokens[j],0) + 1
    word_counts = sorted(word_count.items(), key = lambda x : x[1], reverse = True)
    if K:
        word_counts = word_counts[:K]
    return word_counts

def filter_top_K_data(df,time = False, count = None,K=None):
    if time:
        time_period = df['time'].unique()
        dict_by_time = {}
        for i in time_period:
            df_i = df[df['time']==i].copy()
            dict_by_time[i] = get_top_K_words(df_i,K)
        return dict_by_time
    if count:
        df_count = df[df['follwers_count']>=count].copy()
        top_k_by_count = get_top_K_words(df_count,K)
        return top_k_by_count

###################################
###################################
df = read_csv_files('newsdata/',['text','time'])
df
data = read_csv_files('data/',['time','tweet_text','username','all_hashtags','followers_count'])
data

df1 = split_time(df,'time')
df2 = df1['text']
df2
top_words = get_top_K_words(df2,K=10)


#wc = wordcloud.WordCloud(background_color="white", max_words=500, width= 2000, height = 2000, 
#                         mode ='RGBA', scale=.5).generate({elem[0]:elem[1] for elem in top_30_words})
#plt.imshow(wc)
#plt.axis("off")
#plt.savefig("top_word_cloud.pdf", format = 'pdf')
