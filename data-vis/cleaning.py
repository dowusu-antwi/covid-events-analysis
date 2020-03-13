import seaborn as sns
import pandas as pd
import re 
import os
import time
import matplotlib.pyplot as plt
plt.switch_backend('Qt5Agg')

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
        if file_is_csv(absolute_path):

            # Renames the columns that should be saved to the dataframe, and
            #  removes every other column.
            df_i = pd.read_csv(absolute_path, encoding='ISO-8859-1', header=0)
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

def split_time(df, column):
    '''
    Converts time stamp values to year-month-day pandas datetime objects.
    '''

    # strip to year, month, day; then convert to datetime
    convert = lambda x: x[:10] if type(x) == str else float('nan')
    #convert = lambda x: '-'.join(re.sub(r'[^0-9]',' ',str(x)).strip().split(' ')[:3])
    df[column] = pd.to_datetime(df[column].apply(convert))
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

# Getting tweets data
print("Getting tweets data...")
tweets_header = ['text', 'timestamp', 'hashtags']
start = time.time()
sample_data_folder = 'tweets_2.19.5AM'
tweets_df = read_csv(path+'/data', tweets_header, 'tweets')
print("VM runtime (tweets): %s" % (time.time() - start))
start = time.time()
tweets_df = split_time(tweets_df, 'timestamp').drop_duplicates()
print("VM runtime (split time): %s" % (time.time() - start))

# Getting news data
print("Getting news data...")
news_header = ['source', 'title_text', 'Time_stamp']
start = time.time()
news_df = read_csv(path+'/news_data', news_header)
print("VM runtime (news): %s" % (time.time() - start))
start = time.time()
news_df = split_time(news_df, 'Time_stamp')
print("VM runtime (split time): %s" % (time.time() - start))

news_sources = news_df['source'].unique()
news_dates = news_df['Time_stamp'].unique()
tweets_dates = tweets_df['timestamp'].dropna().unique()
news_words = set()
tweets_words = set()

def get_words(word_frequency_pairs, sort=False):
    if sort:
        return [word for word in word_frequency_pairs]
    return {word: frequency for word, frequency in word_frequency_pairs}

## Initial dictionaries for building datastructures necessary for plot seeding.
print("Building news word frequency dictionary...")
start = time.time()
news_word_frequency = {source: dict() for source in news_sources}
for source in news_sources:
    for date in news_dates:
        record_filter = ((news_df['source'] == source) &
                         (news_df['Time_stamp'] == date))
        filtered_records = news_df[record_filter]
        TOP_COUNT = 15
        PAIRS_INDICATOR = False
        NEWS_INDICATOR = True
        top_K_words = get_top_K_words(filtered_records['title_text'], TOP_COUNT,
                                      PAIRS_INDICATOR, NEWS_INDICATOR)
        news_word_frequency[source][date] = top_K_words
        news_words.update(get_words(top_K_words))

print("VM runtime (news dict): %s" % (time.time() - start))

aggregate_news_word_frequency = {date: dict()}
for date in news_dates:
    record_filter = news_df['Time_stamp'] == date
    filtered_records = news_df[record_filter]
    TOP_COUNT = 15
    PAIRS_INDICATOR = False
    NEWS_INDICATOR = True
    top_K_words = get_top_K_words(filtered_records['title_text'], TOP_COUNT,
                                  PAIRS_INDICATOR, NEWS_INDICATOR)
    aggregate_news_word_frequency[date] = top_K_words

print("Building tweets word frequency dictionary...")
start = time.time()
tweets_word_frequency = {date: dict() for date in tweets_dates}
for date in tweets_dates:
    record_filter = tweets_df['timestamp'] == date
    filtered_records = tweets_df[record_filter]
    TOP_COUNT = 15
    PAIRS_INDICATOR = False
    NEWS_INDICATOR = False
    top_K_words = get_top_K_words(filtered_records['text'], TOP_COUNT, 
                                  PAIRS_INDICATOR, NEWS_INDICATOR)
    tweets_word_frequency[date] = top_K_words
    tweets_words.update(get_words(tweets_word_frequency[date]))
print("VM runtime (news dict): %s" % (time.time() - start))

## Correlation Plot
print("Building shared (between news and tweets) word frequency dictionary...")
start = time.time()
shared_dates = sorted(list(set(tweets_dates) & set(news_dates)))
shared_words = set(tweets_words) & set(news_words)
shared_words_frequency = {'tweets': {word: [] for word in tweets_words}, 
                          'news': {word: [] for word in news_words}}
shared_frequencies = shared_words_frequency['tweets']
for word in shared_words:
    for date in shared_dates:
        # Updates tweets shared word frequencies...
        word_frequency_pairs = tweets_word_frequency[date]
        word_frequencies = get_words(word_frequency_pairs)
        if word in word_frequencies:
            shared_frequencies[word].append(word_frequencies[word])
        else:
            shared_frequencies[word].append(0)

        # Updates news shared words frequencies...
        word_frequency_pairs = news_word_frequency[date]
        word_frequencies = get_words(word_frequency_pairs)
        if word in word_frequencies:
            shared_frequencies[word].append(word_frequencies[word])
        else:
            shared_frequencies[word].append(0)
print("VM runtime (shared): %s" % (time.time() - start))

## Cumulative Tweets Frequencies Plot
print("Building cumulative tweets word frequency dictionary..." )
start = time.time()
cumulative_tweets_frequency = {word: [] for word in tweets_words}
for word in tweets_words:
    for date in tweets_dates:
        word_frequency_pairs = tweets_word_frequency[date]
        word_frequencies = get_words(word_frequency_pairs)
        if word in word_frequencies:
            cumulative_tweets_frequency[word].append(word_frequencies[word])
        else:
            cumulative_tweets_frequency[word].append(0)        
print("VM runtime (cumulative): %s" % (time.time()-start))

## Top K Matches Plot
keyword_matches = []
TOP_K = 10
SORT = True
for date in shared_dates:
    
    # First, get top K tweets words
    word_frequency_pairs = tweets_word_frequency[date]
    sorted_words = get_words(word_frequency_pairs, SORT)
    tweets_top_words = sorted_words[:TOP_K]

    # Next, get top K news words
    word_frequency_pairs = aggregate_news_word_frequency[date]
    sorted_words = get_words(word_frequency_pairs, SORT)
    news_top_words = sorted_words[:TOP_K]

    # Get number shared between the two
    number_shared = len(set(tweets_top_words) & set(news_top_words))
    keyword_matches.append(number_shared)

tweets_news_matches = {source: [] for source in news_sources}

total_news_words = set()
for source in news_sources:
    for date in shared_dates:
        if date in tweets_word_frequency:
            daily_tweets_words = set(get_words(tweets_word_frequency[date]).keys())
            daily_news_words = set(get_words(news_word_frequency[source][date]).keys())
            news_words.update(news_words)
            match_count = len(news_words & tweets_words)
            tweets_news_matches[source].append(match_count)

word_frequency_news = {word:[] for word in total_news_words}
for word in total_news_words:
    for date in shared_dates:
        count = 0
        for source in news_sources:
            word_frequency_pairs = news_word_frequency[source][date]
            word_to_frequency = get_words(word_frequency_pairs)
            if word in word_to_frequency:
                count += word_to_frequency[word]
        word_frequency_news[word].append(count)
################################################################################
#for source in media_sources:
#    sns.lineplot(list(shared_dates), tweets_news_matches[source])

    


#We can read csv files of Mar and Feb respectively, and to compare them.
