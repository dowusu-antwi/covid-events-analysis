import cleaning
import random
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy
import time

'''
Functions to generate and update seaborn plots.
'''

plt.switch_backend('Qt5Agg')

##############################################################################

def plot_seed(visual):
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
    keywords = cleaning.tweets_words
    xdata, ydata = get_data(visual, keywords)
    plt.figure()
    for data in ydata:
        axes = sns.lineplot(xdata, data)
    plt.legend(cleaning.cumulative_tweets_words)
    axes.set_title('Cumulative Twitter Keywords Frequency')
    axes.set_xlabel('Daily Bins')
    axes.set_ylabel('Twitter Keyword Frequency (Cumulative)')
    axes.set_xticklabels([str(x)[:10] for x in xdata], rotation=45, horizontalalignment="center")
    figure = plt.gcf()
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
    '''
    figure = plt.figure()
    news_source = 'bloomberg'
    xdata, ydata = get_data(visual, news_source)
    axes = sns.lineplot(xdata, ydata, label=news_source)
    #sns.barplot(...)
    axes.set_title('Keyword Matching')
    axes.set_xticklabels([str(x)[:10] for x in xdata], rotation=45, horizontalalignment="center")
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
        axes.plot(xdata, ydata, label=keyword)
        axes.set_title('Keyword Matching (News Source: %s)' % keyword.upper())
        axes.set_xticklabels([str(x)[:10] for x in xdata], rotation=45, horizontalalignment="center")
        axes.set_xlabel('Date')
        axes.set_ylabel('Number of Matches (Among the Top %s Keywords)' % cleaning.TOP_K)
        canvas.draw()

    else:
        # Iterates through axes, gets scatter collections and lines
        #collections = axis.collections
        #lines = axis.lines
        
        # Gets new data associated with new keyword, for given media (get from 
        #  title)
        scatter_xdata, scatter_ydata = get_data(visual, keyword)
        
        # Clear axis, get max for new dataset, set new axis limits
        axes = axes[0]
        axes.clear()
        #xmax = max([max(scatter_xdata), max(line_xdata)])+2
        #ymax = max([max(scatter_ydata), max(line_ydata)])+2
        #axis.set_xlim([-2, xmax+2])
        #axis.set_ylim([-2, ymax+2])
        #print(scatter_xdata)
        #print(scatter_ydata)
        
        # Plot new axis data, scatter and line
        
        axes.scatter(scatter_xdata, scatter_ydata)
        #collection = collections[0]
        #line = lines[0]
        #offsets = [[x,y] for x,y in zip(scatter_xdata, scatter_ydata)]
        #collection.set_offsets(offsets)
        #line.set_xdata(line_xdata)
        #line.set_ydata(line_ydata)
        
        # update title and axes labels
        axes.set_title('Correlate Frequency of Keywords in Tweets and News Titles')
        axes.set_xlabel('Twitter Keyword Frequency (Daily Bins)')
        axes.set_ylabel('News Keyword Frequency (Daily Bins)')

        canvas.draw()

        # lists: axes.collections, axes.lines
        # line.s/get_x/ydata()
        # collection.s/get_offsets([[a,b],[c,d],...])
        # axes.plot(), axes.scatter()
        
        #axes = canvas.figure.axes[0]
        #axes.scatter(xdata, ydata)
        #axes.set_title(title)
        #canvas.draw()

'''
Correlation
xdata: shared_words_frequency['tweets'][keyword]
ydata: shared_words_frequency['news'][keyword]

Cumulative
xdata: shared_dates
ydata: cumulative_tweets_frequency[keyword]

Match Plot
xdata: shared_dates
ydata: keyword_matches
'''

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
        tweets_frequency = cleaning.shared_words_frequency['tweets']
        news_frequency = cleaning.shared_words_frequency['news']

        scatter_xdata, scatter_ydata = (tweets_frequency[keyword],
                                        news_frequency[keyword])
        return scatter_xdata, scatter_ydata
    if visual == 'Cumulative Twitter Frequency':
        keywords = args[0]
        xdata = cleaning.tweets_dates
        tweets_frequency = cleaning.cumulative_tweets_frequency
        ydata = [tweets_frequency[keyword] for keyword in keywords]
        return xdata, ydata
    if visual == 'Keyword Matching':
        news_source = args[0]
        xdata = cleaning.shared_dates
        ydata = cleaning.keyword_matches[news_source]
        return xdata, ydata

def get_rand_data(xsize, ysize):
    return ([index for index in range(xsize)], 
            [index + random.random()*15 for index in range(ysize)])

def get_rand_line(xsize):
    return [index + random.random()*10 for index in range(xsize)]

def train_regressor(xdata, ydata):
    '''
    Learns a linear regression model on a set of training data.

    Input:
     xdata (list of integers): independent variable values,
     ydata (list of integers): dependent variable values.

    Returns parameters for a learned regression model.
    '''

    regressor = LinearRegression()
    regressor.fit(numpy.array(xdata).reshape(-1,1), numpy.array(ydata).reshape(-1,1))
    return regressor.intercept_, regressor.coef_ 

############################################################################### 
def live_plot():
    # Plot seed graph
    plt.figure()
    xdata = [0]
    ydata = [0]
    axes = sns.lineplot(xdata,ydata)
    marker_axes = sns.scatterplot(xdata,ydata,marker='x')
    axes.set_xlim([0,25])
    axes.set_ylim([0,25])
    canvas = plt.gcf().canvas
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()

    axes.set_title('Real-time Plotting')
    axes.set_xlabel('Time')
    axes.set_ylabel('Value')
  
    # Begin iteration, wait for 1 second
    x, y = xdata[::-1][0], ydata[::-1][0]
    while(True):
        plt.pause(0.05)
        # Generate new data point
        x, y = x+1, y+1+random.randrange(-1000,1100)/1000

        # Update marker
        marker = marker_axes.collections[0]
        marker.set_offsets([[x, y]])

        # Update graph
        line = axes.lines[0]
        ydata = line.get_ydata()
        xdata = line.get_xdata()
        new_xdata = list(xdata) + [x]
        new_ydata = list(ydata) + [y]
        line.set_xdata(new_xdata)
        line.set_ydata(new_ydata)
        _, y_lim = axes.get_ylim()
        _, x_lim = axes.get_xlim()
        axes.set_xlim([0,max(y_lim, max(new_ydata)+5, 25)])
        axes.set_ylim([0,max(x_lim, max(new_xdata)+1, 25)])
        canvas.draw()
   
def plot_seaborn(data, keyword):
    '''
    Plots data in a seaborn figure.

    x_data (list): independent variable axis data points,
    y_data (list or list of lists): dependent variable axis data points,
    multi_dependent_variables (boolean): indicates whether to expect multiple 
                                         y-axis data sets.

    Returns figure with plotted data.
    '''

    # Sets a global theme
    sns.set(style='darkgrid')

    # Generates data for plotting:
    # 1. date-keyword-frequency
    #keyword_frequency = {}
    #xdata = sorted([date for date in data])
    #for date in xdata:
    #    for keyword in data[date]:
    #        if keyword in keyword_frequency:
    #            keyword_frequency[keyword].append(data[date][keyword])
    #        else:
    #            keyword_frequency[keyword] = [data[date][keyword]]

    ## Generates a scatter plot
    #for keyword in keyword_frequency:
    #    ydata = keyword_frequency[keyword]
    #    figure = sns.lineplot(x=xdata, y=ydata, label=keyword)
    #figure.set_title('Keywords vs. Frequency')
    #figure.set_xticklabels(xdata, rotation=45, horizontalalignment='center')
    
    # 2. twitter frequency v. media frequency
    twitter_data, media_data = data
    source_frequencies = {'twitter': [], 'media': []}
    for date in twitter_data.keys() & media_data.keys():
        twitter_frequency = twitter_data[date][keyword]
        media_frequency = media_data[date][keyword]
        source_frequencies['twitter'].append(twitter_frequency)
        source_frequencies['media'].append(media_frequency)

    xdata = source_frequencies['twitter']
    ydata = source_frequencies['media']
    axes = sns.scatterplot(x=xdata, y=ydata, s=40)
    figure = axes.get_figure()
    axes.set_xlabel('News Keyword Frequency')
    axes.set_ylabel('Twitter Keyword Frequency')
       
    title = ('Twitter Keyword Frequency vs. News Keyword Frequency (for the '
              'keyword %s)' % keyword.upper())
    axes.set_title(title)

    # 3. Plots frequency of multiple words over time

    # Note: using the figure manager, showing plot without hanging on plt.show()
    #  has different potential methods 
    # Possible window maximizing methods:
    #  manager.frame.Maximize(True), 
    #  manager.resize(*manager.window.maxsize())
    #  manager.window.state('zoomed')
    #manager = plt.get_current_fig_manager()
    #manager.window.showMaximized()
    return figure, axes

if __name__ == "__main__":
    pass

