from cleaning import *

# Getting news data
path = os.getcwd()
fname = path + '/news_data/'

# Getting tweets data
tweets_header = ['text', 'timestamp']
sample_data_folder = 'tweets_2.19.5AM'
tweets_df = read_csv(path+'/data', tweets_header, 'tweets')
tweets_df = split_time(tweets_df, 'timestamp')

news_header = ['source', 'title_text', 'Time_stamp']
news_df = read_csv(path+'/news_data', news_header)
news_df = split_time(news_df, 'Time_stamp')


news_sources = list(news_df['source'].unique())
news_dates = news_df['Time_stamp'].unique()
tweets_dates = sorted(list(tweets_df['timestamp'].dropna().unique()))
news_words = set()
tweets_words = set()



## Initial dictionaries for building datastructures necessary for plot seeding.
TOP_COUNT = 20
PAIRS_INDICATOR = False
NEWS_INDICATOR = True
news_word_frequency = {source: dict() for source in news_sources}
for source in news_sources:
    for date in news_dates:
        record_filter = ((news_df['source'] == source) &
                         (news_df['Time_stamp'] == date))
        filtered_records = news_df[record_filter]
        top_K_words = get_top_K_words(filtered_records['title_text'], TOP_COUNT,
                                      NEWS_INDICATOR)
        news_word_frequency[source][date] = top_K_words
        news_words.update(get_words(top_K_words))

aggregate_news_word_frequency = {}
for date in news_dates:
    record_filter = news_df['Time_stamp'] == date
    filtered_records = news_df[record_filter]
    top_K_words = get_top_K_words(filtered_records['title_text'], TOP_COUNT,
                                  NEWS_INDICATOR)
    aggregate_news_word_frequency[date] = top_K_words

NEWS_INDICATOR = False
start = time.time()
tweets_word_frequency = {}
for date in tweets_dates:
    record_filter = tweets_df['timestamp'] == date
    filtered_records = tweets_df[record_filter]
    top_K_words = get_top_K_words(filtered_records['text'], TOP_COUNT, 
                                  NEWS_INDICATOR)
    tweets_word_frequency[date] = top_K_words
    tweets_words.update(get_words(tweets_word_frequency[date]))


## Correlation Plot
shared_dates = sorted(list(set(tweets_dates) & set(news_dates)))
shared_words = list(set(tweets_words) & set(news_words))


NEWS_INDICATOR = True
top_K_words = get_top_K_words(news_df['title_text'], TOP_COUNT, 
                              NEWS_INDICATOR)
SORT = True
cumulative_news_words = get_words(top_K_words, SORT)

shared_words_frequency = {'tweets': {word: [] for word in cumulative_news_words}, 
                          'news': {word: [] for word in cumulative_news_words}}

for word in cumulative_news_words:
    for date in shared_dates:
        # Updates tweets shared word frequencies...
        shared_frequencies = shared_words_frequency['tweets']
        word_frequency_pairs = tweets_word_frequency[date]
        word_frequencies = get_words(word_frequency_pairs)
        shared_frequencies[word].append(word_frequencies.get(word,0))

        # Updates news shared words frequencies...
        shared_frequencies = shared_words_frequency['news']
        word_frequency_pairs = aggregate_news_word_frequency[date]
        word_frequencies = get_words(word_frequency_pairs)
        shared_frequencies[word].append(word_frequencies.get(word,0))

## Cumulative Tweets Frequencies Plot
cumulative_tweets_frequency = {word: [] for word in tweets_words}
for word in tweets_words:
    for date in tweets_dates:
        word_frequency_pairs = tweets_word_frequency[date]
        word_frequencies = get_words(word_frequency_pairs) 
        cumulative_tweets_frequency[word].append(word_frequencies.get(word,0))


## Top K Matches Plot
keyword_matches = {source: [] for source in news_sources}
TOP_K = 20
SORT = True
for source in news_sources:
    matches = keyword_matches[source]
    for date in shared_dates:
        # First, get top K tweets words
        word_frequency_pairs = tweets_word_frequency[date]
        sorted_words = get_words(word_frequency_pairs, SORT)
        tweets_top_words = sorted_words[:TOP_K]

        # Next, get top K news words
        word_frequency_pairs = news_word_frequency[source][date]
        sorted_words = get_words(word_frequency_pairs, SORT)
        news_top_words = sorted_words[:TOP_K]

        # Get number shared between the two
        number_shared = len(set(tweets_top_words) & set(news_top_words))
        matches.append(number_shared)

NEWS_INDICATOR = False
top_K_words = get_top_K_words(tweets_df['text'], TOP_COUNT, 
                              NEWS_INDICATOR)
SORT = True
cumulative_tweets_words = get_words(top_K_words, SORT)
