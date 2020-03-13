import seaborn as sns
import pandas as pd
import re 
import os
import time

stopwords = set(['a', 'also', 'an', 'and', 'are', 'as', 'at', 'be',
                 'but', 'by', 'for', 'from', 'have','has','he', 'how', 'i',
                 'ii', 'iii','in', 'in', 'is', 'it','its','it\'s','not','of',
                 'on','or', 's', 'so','such','that', 'the', 'their', 'this',
                 'through','to', 'was', 'we', 'were', 'which', 'will', 'with',
                 'yet','you'])

stopwords_for_news = set(['wall','street','journal','washington','post', 'cnn',
                          'reuters', 'buzzfeed', 'verge','bloomberg', 'cnbc'])

def file_is_csv(absolute_path):
    '''
    Returns boolean representing whether or not absolute path to file is to a
     csv file.
    '''
    return absolute_path[::-1][:3][::-1] == 'csv'

def read_csv(path, df_header, data_type=None):
    '''
    Creates an empty seed dataframe, and recursively finds all CSV files stored,     saving the contents into a dataframe with the columns specified by the
     dataframe header parameter.

    Inputs:
     path (string): file path to CSV files,
     df_header (string): specifies which columns to write to the dataframe.

    Returns dataframe containing the total contents of the CSV files.
    '''
    
    df = pd.DataFrame(columns=df_header)
    return find_files(path, df_header, df, data_type)

def find_files(path, df_header, df, data_type):
    '''
    Recursively finds all CSV files stored, saving the contents into a dataframe
     with the columns specified by the dataframe header parameter.
 
    Inputs:
     path (string): file path to CSV files,
     df_header (string): specifies which columns to write to the dataframe,
     df (dataframe): recursively built dataframe containing CSV file contents.
 
    Returns dataframe containing the total contents of the CSV files.
    '''

    files = os.listdir(path)
    for filename in files:
        # Extracts the contents of CSV files, and recurses when a folder
        #  containing more CSV files is found.
        absolute_path = path + '/' + filename
        print('absolute path: %s' % absolute_path)
        if file_is_csv(absolute_path):

            # Renames the columns that should be saved to the dataframe, and
            #  removes every other column.
            print("Reading the csv...")
            df_i = pd.read_csv(str(absolute_path), header=0)
            print("Read successful.")
            if data_type == 'tweets':
                df_i_header = df_i.columns
                for column in df_i_header:
                    if 'text' in column.lower():
                        df_i.rename(columns={column: 'text'}, inplace=True)
                    elif 'time' in column.lower():
                        df_i.rename(columns={column: 'timestamp'}, inplace=True)
                    elif 'hashtag' in column.lower():
                        df_i.rename(columns={column: 'hashtags'}, inplace=True)
                extraneous_columns = set(df_i.columns) - set(df_header)
                df_i = df_i.drop(columns=list(extraneous_columns))

        elif os.path.isdir(absolute_path):
            df_i = find_files(absolute_path, df_header, df, data_type)

        df = pd.concat([df, df_i], axis=0, sort=True)

    # Removes empty rows and resets index to reflect new row count.
    df = df.dropna(axis=0)
    df.reset_index(drop=True, inplace=True)
    return df

def split_time(df,column_name):
    '''
    Split date and time-of-day
    '''

    # strip to year, month, day; then convert to datetime
    d = df[column_name].apply(lambda x : 
                              re.sub(r'[^0-9]', ' ',x).strip().split(' '))
    df['date'] = d.apply(lambda x :'-'.join(x[:3]))
    df['date']= pd.to_datetime(df['date'])
    df = df.drop([column_name], axis=1)
    return df

def convert_hashtag_list(df,column_name):
    '''
    convert the hashtag columns from string to list of strings 
    '''
    for i in range(len(df[column_name])):
        d = df[column_name].loc[i].split(',')
        d= [i.strip(' []\'\'').lower() for i in d]
        df[column_name].loc[i] = d
    return df


def get_top_K_hashtag(df,column_name,K=None):
    hash_dic = {}
    list_ = df[column_name].tolist() 
    for i in list_:
        for j in i:
            hash_dic[j] = hash_dic.get(j,0) + 1
    tag_counts = sorted(hash_dic.items(), key = lambda x : x[1], reverse = True)
    top_K_tags = tag_counts[:K]
    return top_K_tags



def word_tokenize(string, news):
    '''
    convert a string to list of words
    
    '''
    list_ = []
    list_of_string = string.split()
    for n in list_of_string:
        # Distinguish WHO and who
        string_ = re.sub('^who', '',n)
        string_ = re.sub('\W', '', string_).lower()
        string_ = re.sub('^https', '',string_)
            
        if string_ and (string_ not in stopwords): 
            if news:
                if string_ not in stopwords_for_news:
                    list_.append(string_)
            else:
                list_.append(string_)
    return list_

def get_top_K_words(df_text,K=None,pairs=False,news=False):
    word_count = {}
    for i in df_text:
        tokens = word_tokenize(i,news)
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


#def filter_top_K_data(df,time = False, count = None,K=None):
#
#### Apply filters to the data
#
#if time:
#    time_period = df['time'].unique()
#    dict_by_time = {}
#    for i in time_period:
#        df_i = df[df['time']==i].copy()
#        dict_by_time[i] = get_top_K_words(df_i,K)
#    return dict_by_time
#if count:
#    df_count = df[df['follwers_count']>=count].copy()
#    top_k_by_count = get_top_K_words(df_count,K)
#    return top_k_by_count
#


################################
#################################

######Execution


path = os.getcwd()
fname = path + '/news_data/february_news/'
useful_columns = ['text', 'timestamp', 'hashtags']
start = time.time()
#df = read_csv(path+'/data', useful_columns, 'tweets')
#print("VM runtime: %s" % (time.time() - start))
df = read_csv(path+'/news_data', useful_columns)

################################################################################
#df = read_csv_files(fname,['title_text','Time_stamp','source'])
#df1 = split_time(df,'Time_stamp')

#top_K_words_news = {source: {str(date)[:10]: None for date in df['date'].unique()} for source in df['source'].unique()}
#for source in df1['source'].unique():
#    for date in df1['date'].unique():
#        date = str(date)[:10]
#        top_K_words = get_top_K_words(df1[df1['date'] == date][df1['source'] == source]['title_text'],K=15,pairs =False,news=True)
#        top_K_words_news[source][date] = top_K_words
#
#data = read_csv_files('data/',['timestamp','tweet_text','username','all_hashtags','followers_count'])
#data1 = split_time(data,'timestamp')
#data2 =convert_hashtag_list(data1,'all_hashtags')
#top_K_words_twitter = {str(date)[:10]: None for date in data2['date'].unique()}
#for date in data2['date'].unique():
#    date = str(date)[:10]
#    top_K_words_twitter_by_date = get_top_K_words(data2[data2['date'] == date]['tweet_text'],K=15,pairs =False,news=True)
#    top_K_words_twitter[date] = top_K_words_twitter_by_date
#
#
#dates = set(top_K_words_twitter.keys()) & set(top_K_words_news['bloomberg'].keys())
#media_sources = list(df1['source'].unique())
#media_matches = {source:None for source in media_sources}
#
#for source in media_sources:
#    total_counts = []
#    for date in dates:
#        twitter_words = set([pair[0] for pair in top_K_words_twitter[date]])
#        news_words = set([pair[0] for pair in top_K_words_news[source][date]])
#        total_counts.append(len(news_words & twitter_words))
#    media_matches[source] = total_counts
#
#for source in media_sources:
#    sns.lineplot(list(dates), media_matches[source])

    


#We can read csv files of Mar and Feb respectively, and to compare them.

#####################################Archive####################################
def read_csv_files(path,list_of_col):
    '''
    read all csv files in a folder
    '''

    files = os.listdir(path)
    print("Files: %s" % files)
    print("Creating an empty data frame for the columns '%s'..." % list_of_col)
    df = pd.DataFrame(columns=list_of_col)
    print("Creating dataframe for each file and merging...")
    for i in files:
        print("Current 'file': %s" % i)
        if i[-3:] == "csv":
            print("File is a csv file, creating dataframe...")
            print("Reading in the absolute path '%s'..." % (path+i))
            df_i = pd.read_csv(path+i,encoding="ISO-8859-1", header=0)
            print("Merging with the previous dataframe...")
            df = pd.concat([df, df_i],axis=0)
            print("Dataframe merged. Continuing iteration...")
    print("Iteration complete.")
    #df = df.dropna(axis=0)
    df.reset_index(drop=True, inplace=True)
    return df

def split_time(df,column_name):
    '''
    Split date and time-of-day
    '''

    # strip to year, month, day; then convert to datetime
    d = df[column_name].apply(lambda x : 
                              re.sub(r'[^0-9]', ' ',x).strip().split(' '))
    df['date'] = d.apply(lambda x :'-'.join(x[:3]))
    df['date']= pd.to_datetime(df['date'])
    df = df.drop([column_name], axis=1)
    return df
