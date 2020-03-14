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
    Creates an empty seed dataframe, and recursively finds all CSV files stored,     
    saving the contents into a dataframe with the columns specified by the
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
    df = df.drop_duplicates()
    df.reset_index(drop=True, inplace=True)
    return df


def split_time(df, column):
    '''
    Pass in the dataframe and the column name containing the date and time,
    split date from the format of time and return the dataframe
    '''

    # strip to year, month, day; then convert to datetime
    convert = lambda x: x[:10] if type(x) == str else float('nan')
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
    Pass in a string and convert it to list of string matching our criterion
    '''
    list_ = []
    if type(string) != str:
        return list_
    list_of_string = string.split()
    for n in list_of_string:
        string_ = re.sub('\W', '', n).lower()
        string_ = re.sub('^https', '',string_)
            
        if string_ and (string_ not in stopwords): 
            if news:
                if string_ not in stopwords_for_news:
                    list_.append(string_)
            else:
                list_.append(string_)
    return list_

def get_top_K_words(df_text,K=None,news=False):
    '''
    Pass in a dataframe, the column we want to get words from, number of K,
    and whether the dataframe is the news,and return the a sorted list of 
    tuples of (top K words and its counts)
    '''
    word_count = {}
    for i in df_text:
        tokens = word_tokenize(i,news)
        for j in range(len(tokens)):
            word_count[tokens[j]] = word_count.get(tokens[j],0) + 1
    word_counts = sorted(word_count.items(), key = lambda x : x[1], 
                         reverse = True)
    if K:
        word_counts = word_counts[:K]
    return word_counts

def get_words(word_frequency_pairs, sort=False):
    '''
    Pass in a list of tuples (word and frequency), and return a list of the 
    words or return a dictionary where the key is the word, the value is 
    the frequency
    '''
    if sort:
        return [word for word, frequency in word_frequency_pairs]
    return {word: frequency for word, frequency in word_frequency_pairs}
