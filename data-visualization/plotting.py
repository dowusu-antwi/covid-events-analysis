from transformation import *
import seaborn as sns
import matplotlib.pyplot as plt
'''
Functions to generate and update seaborn plots.
'''

plt.switch_backend('Qt5Agg')

def plot_seed(visual):
    '''
    Plots the initial figure, to be embedded into the GUI.
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
    figure = plt.figure()
    for keyword, data in zip(keywords, ydata):
        axes = sns.lineplot(xdata, data, label=keyword)
    plt.legend(keywords)
    axes.set_title('Cumulative Twitter Keywords Frequency')
    axes.set_xlabel('Date')
    axes.set_ylabel('Twitter Keyword Frequency (Cumulative)')
    axes.set_xticks(xdata)
    axes.set_xticklabels(xdata, rotation=30, horizontalalignment="right")
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
    news_sources = ['bloomberg']
    xdata, ydata = get_data(visual, news_sources)
    for news_source, data in zip(news_sources, ydata):
        axes = sns.lineplot(xdata, data, label=news_source)
    axes.set_title('Keyword Matching')
    axes.set_xticklabels([str(x)[:10] for x in xdata], rotation=30,
                         horizontalalignment="right")
    axes.set_xlabel('Date')
    axes.set_ylabel('Number of Matches')
    return figure, axes


def update_plot(visual, data_selector, axes, canvas):
    '''
    Updates plot, given keyword associated with data to update with.

    Inputs:
     keyword (string): string representing which data to get,
     axes (numpy array): array of axes objects.
    '''
   
    if visual == 'Keyword Matching':
        news_sources = data_selector
        xdata, ydata = get_data(visual, news_sources)
        axes = axes[0]
        axes.clear()
        for data, news_source in zip(ydata, news_sources):
            axes.plot(xdata, data, label=news_source)
        axes.legend(news_sources)
        news_plot_title = ', '.join([news_source.upper() 
                                     for news_source in news_sources])
        axes.set_title(('Keyword Matching (News Source(s): %s)' 
                        % news_plot_title))
        axes.set_xticklabels(xdata, rotation=30, horizontalalignment="right")
        axes.set_xlabel('Date')
        axes.set_ylabel('Number of Matches with Tweets Keywords (Among the Top'
                        ' %s Keywords)' % TOP_K)
        canvas.draw()
    elif visual == 'Media v. Twitter Frequency Comparison':
        # Gets new data associated with new keyword, for given media (get from 
        #  title)
        keyword = data_selector[0]
        scatter_xdata, scatter_ydata = get_data(visual, keyword)
        
        # Clear axis, get max for new dataset, set new axis limits
        axes = axes[0]
        axes.clear()
        # Plot new scatter data
        axes.scatter(scatter_xdata, scatter_ydata)
        # update title and axes labels
        axes.set_title(('Correlate Frequency of Keywords in Tweets and News'
                        ' Titles'))
        axes.set_xlabel('Twitter Keyword Frequency (Daily Bins)')
        axes.set_ylabel('News Keyword Frequency (Daily Bins)')
        canvas.draw()
    elif visual == 'Cumulative Twitter Frequency':
        keywords = data_selector
        xdata, ydata = get_data(visual, keywords)
        axes = axes[0]
        xlabel = axes.get_xlabel()
        ylabel = axes.get_ylabel()
        title = axes.get_title()
        axes.clear()
        for data, keyword in zip(ydata, keywords):
            axes.plot(xdata, data, label=keyword)
        axes.legend(keywords)
        axes.set_title(title)
        axes.set_xlabel(xlabel)
        axes.set_ylabel(ylabel)
        axes.set_xticklabels(xdata, rotation=30, horizontalalignment="right")
        canvas.draw()

        
def get_data(visual, selector_variable):
    '''
    Gets data associated with the given media source and keyword.

    Inputs:
     visual (string): represents which visualization method to get data for,
     selector_variable (string or list): 

    Returns two list, x-axis and y-axis data respectively.
    '''
    if visual == 'Media v. Twitter Frequency Comparison':
        keyword = selector_variable
        tweets_frequency = shared_words_frequency['tweets']
        news_frequency = shared_words_frequency['news']
        scatter_xdata, scatter_ydata = (tweets_frequency[keyword],
                                        news_frequency[keyword])
        return scatter_xdata, scatter_ydata
    if visual == 'Cumulative Twitter Frequency':
        keywords = selector_variable
        xdata = [str(date)[:10] for date in tweets_dates]
        ydata = [cumulative_tweets_frequency[keyword] for keyword in keywords]
        return xdata, ydata
    if visual == 'Keyword Matching':
        news_sources = selector_variable
        xdata = [str(date)[:10] for date in shared_dates]
        ydata = [keyword_matches[source] for source in news_sources]
        return xdata, ydata
