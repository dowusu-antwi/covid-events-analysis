from execution import *
import seaborn as sns
import matplotlib.pyplot as plt
'''
Functions to generate and update seaborn plots.
'''

plt.switch_backend('Qt5Agg')

def plot_seed(visual):
    '''
    Plots the initial figure.
    '''
    if visual == 'Media v. Twitter Frequency Comparison':
        return correlate_frequency(visual)
    if visual == 'Cumulative Twitter Frequency':
        return cumulative_frequency(visual)
    if visual == 'Keyword Matching':
        return keyword_matching(visual)


def cumulative_frequency(visual):
    '''
    Plots cumulative keyword frequency, with random data, to be updated later.
    '''
    keywords = cumulative_tweets_words
    xdata, ydata = get_data(visual, keywords)
    print(len(xdata))
    figure = plt.figure()
    for index, data in enumerate(ydata):
        axes = sns.lineplot(xdata, data, label=keywords[index])
    plt.legend(cumulative_tweets_words)
    axes.set_title('Cumulative Twitter Keywords Frequency')
    axes.set_xlabel('Daily Bins')
    axes.set_ylabel('Twitter Keyword Frequency (Cumulative)')
    axes.set_xticks(xdata)
    axes.set_xticklabels([str(x)[:10] for x in xdata], 
                         rotation=45,
                         horizontalalignment="center")
    return figure, axes


def correlate_frequency(visual):
    '''
    Plots four graphs using subplot, with random scatter and line data, to be
     later updated.
    '''
    figure = plt.figure()
    keyword = 'coronavirus'
    scatter_xdata, scatter_ydata = get_data(visual, keyword)
    nRows, nCols = 1, 1
    figure, axes = plt.subplots(nRows, nCols, figsize=(7,7), sharex=True)
    sns.scatterplot(x = scatter_xdata, y = scatter_ydata, s=40)
    plt.title('Correlate Frequency of Keywords in Tweet and News Titles')
    plt.xlabel('Twitter Keyword Frequency (Daily Bins)')
    plt.ylabel('News Keyword Frequency (Daily Bins)')
    return figure, axes


def keyword_matching(visual):
    '''
    Plots the keyword matching plot which maps the number of matches
     for the top 20 keywords from Tweets and a media source's news titles.
    '''
    figure = plt.figure()
    news_source = 'bloomberg'
    xdata, ydata = get_data(visual, news_source)
    axes = sns.lineplot(xdata, ydata, label=news_source)
    axes.set_title('Keyword Matching')
    axes.set_xticklabels([str(x)[:10] for x in xdata], 
                         rotation=45, 
                         horizontalalignment="center")
    axes.set_ylabel('Number of Matches')
    return figure, axes


def update_plot(visual, keyword, axes, canvas):
    '''
    Updates plot, given keyword associated with data to update with.

    Inputs:
     keyword (string): string representing which data to get,
     axes (numpy array): array of axes objects.
    '''
   
    if visual == 'Keyword Matching':
        xdata, ydata = get_data(visual, keyword)
        print(ydata)
        axes = axes[0]
        print(axes)
        axes.clear()
        xdata = [str(x)[:10] for x in xdata]
        axes.plot(xdata, ydata, label=keyword)
        axes.set_title('Keyword Matching (News Source: %s)' % keyword.upper())
        axes.set_xticklabels(xdata, 
                             rotation=45, 
                             horizontalalignment="center")
        axes.set_xlabel('Date')
        axes.set_ylabel('Number of Matches (Among the Top %s Keywords)' % TOP_K)
        canvas.draw()

    else:
        # Gets new data associated with new keyword, for given media (get from 
        #  title)
        scatter_xdata, scatter_ydata = get_data(visual, keyword)
        
        # Clear axis, get max for new dataset, set new axis limits
        axes = axes[0]
        axes.clear()
        # Plot new axis data, scatter and line
        axes.scatter(scatter_xdata, scatter_ydata)
        # update title and axes labels
        axes.set_title('Correlate Frequency of Keywords in Tweets and News Titles')
        axes.set_xlabel('Twitter Keyword Frequency (Daily Bins)')
        axes.set_ylabel('News Keyword Frequency (Daily Bins)')
        canvas.draw()

        
def get_data(visual, *args):
    '''
    Gets data associated with the given media source and keyword.

    Inputs:
     media_source (string): represents which media source to get data from,
     keyword (string): represents which keyword to get frequency data from.

    Returns two tuples, x-axis and y-axis data, respectively, each a tuple of 
     scatter and line data lists.
    '''
    if visual == 'Media v. Twitter Frequency Comparison':
        keyword = args[0]
        tweets_frequency = shared_words_frequency['tweets']
        news_frequency = shared_words_frequency['news']

        scatter_xdata, scatter_ydata = (tweets_frequency[keyword],
                                        news_frequency[keyword])
        return scatter_xdata, scatter_ydata
    if visual == 'Cumulative Twitter Frequency':
        keywords = args[0]
        xdata = tweets_dates
        tweets_frequency = cumulative_tweets_frequency
        ydata = [tweets_frequency[keyword] for keyword in keywords]
        return xdata, ydata
    if visual == 'Keyword Matching':
        news_source = args[0]
        xdata = shared_dates
        ydata = keyword_matches[news_source]
        return xdata, ydata
