'''
Cleaning 
'''


import pandas as pd
import re 
import os


stopwords = set(['a', 'also', 'an', 'and', 'are', 'as', 'at', 'be',
                 'but', 'by', 'for', 'from', 'have','has','he', 'how', 'i', 'ii', 'iii','in',
                  'in', 'is', 'it','its','it\'s','not','of','on','or',
                 's', 'so','such','that', 'the', 'their', 'this','through','to',
                 'was', 'we', 'were', 'which', 'will', 'with','yet','you'])

stopwords_for_news = set(['wall','street','journal','washington','post', 'cnn',
                          'reuters', 'buzzfeed', 'verge','bloomberg', 'cnbc'])

def read_csv_files(path,list_of_col):
    '''
    Pass in the path of the foler of csv files, and then read certain columns 
    of all csv files into a single dataframe
    '''

    
    files = os.listdir(path)
    df = pd.DataFrame(columns=list_of_col)
    for i in files:
        if i[-3:] == "csv":
            df_i = pd.read_csv(path+i,encoding="ISO-8859-1",header=0)
            df = pd.concat([df, df_i],axis=0)
    df = df.dropna(axis=0)
    df.reset_index(drop=True, inplace=True)
    return df

def split_time(df,column_name):
    '''
    Pass in the dataframe and the column name containing the date and time,
    split date from the format of time and return the dataframe
    '''

    d = df[column_name].apply(lambda x : re.sub(r'[^0-9]', ' ',x).strip().split(' '))
    df['date'] = d.apply(lambda x :'-'.join(x[:3]))
    df = df.drop([column_name], axis=1)
    return df

def convert_hashtag_list(df,column_name):
    '''
    Convert the hashtag columns from string to list of strings 
    '''
    for i in range(len(df[column_name])):
        d = df[column_name].loc[i].split(',')
        d= [i.strip(' []\'\'').lower() for i in d]
        df[column_name].loc[i] = d
    return df


def get_top_K_hashtag(df,column_name,K=None):
    '''
    Pass in a dataframe, the column we want to get words from, number of K,
    and whether the dataframe is the news, and return the a sorted list of 
    tuples of (top K words and its counts)
    '''
    hash_dic = {}
    list_ = df[column_name].tolist() 
    for i in list_:
        for j in i:
            hash_dic[j] = hash_dic.get(j,0) + 1
    tag_counts = sorted(hash_dic.items(), key = lambda x : x[1], reverse = True)
    top_K_tags = tag_counts[:K]
    return top_K_tags



def word_tokenize(string):
    '''
    Pass in a string and convert it to list of string matching our criterion
    '''
    list_ = []
    list_of_string = string.split()
    for n in list_of_string:
        # # Distinguish WHO and who
        # string_ = re.sub('^who', '',n)
        string_ = re.sub('\W', '', string_).lower()
        string_ = re.sub('^https', '',string_)
            
        if string_ and (string_ not in stopwords): 
            if news:
                if string_ not in stopwords_for_news:
                    list_.append(string_)
            else:
                list_.append(string_)
    return list_

def get_top_K_words(df,column_name, K=None,news=False):
    '''
    Pass in a dataframe, the column we want to get words from, number of K,
    and whether the dataframe is the news,and return the a sorted list of 
    tuples of (top K words and its counts)
    '''
    df_text = df[column_name]
    word_count = {}
    for i in df_text:
        tokens = word_tokenize(i,news)
        for j in range(len(tokens)):
            word_count[tokens[j]] = word_count.get(tokens[j],0) + 1
    word_counts = sorted(word_count.items(), key = lambda x : x[1], reverse = True)
    if K:
        word_counts = word_counts[:K]
    return word_counts


######Execution


df = read_csv_files('newsdata/mar_news/',['title_text','Time_stamp','source'])
df1 = split_time(df,'Time_stamp')
get_top_K_words(df['title_text'],K=30,news=True)

data = read_csv_files('data/',['timestamp','tweet_text','username','all_hashtags','followers_count'])
data1 = split_time(data,'timestamp')
data2 =convert_hashtag_list(data1,'all_hashtags')
get_top_K_words(df1['title_text'],K=30,news=True)




















