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
        return ''

def cumulative_frequency(visual):
    '''
    Plots cumulative keyword frequency, with random data, to be updated later.
    '''
    keywords = list(cleaning.word_frequency)
    xdata, ydata = get_data(visual, keywords)
    plt.figure()
    print(xdata)
    print(ydata)
    for data in ydata:
        axes = sns.lineplot(xdata, data)
    axes.set_title(('Cumulative Twitter Keyword Frequency (Keyword: %s)' 
                    % keyword.upper()))
    axes.set_xlabel('Daily Bins')
    axes.set_ylabel('Twitter Keyword Frequency (Cumulative)')
    figure = plt.gcf()
    return figure, axes

def correlate_frequency(visual):
    '''
    Plots four graphs using subplot, with random scatter and line data, to be
     later updated.
    '''
    media = ['Verge', 'NYTimes', 'BBC', 'CNN']
    keyword = 'coronavirus'

    nRows, nCols = 2, 2
    plt.figure()
    figure, axes = plt.subplots(nRows, nCols, figsize=(7,7), sharex=True)
    figure.suptitle('Media Source v. Twitter, Keyword Frequency', fontsize=20)
    for index, media_source in enumerate(media):
        # Retrieves seed data (scatter and line) and plots
        xdata, ydata = get_data(visual, keyword, media_source)
        scatter_xdata, line_xdata = xdata
        scatter_ydata, line_ydata = ydata

        axis = axes.flatten()[index] if len(media) > 1 else axes
        line_axis = sns.lineplot(line_xdata, line_ydata, ax=axis)
        scatter_axis = sns.scatterplot(scatter_xdata, scatter_ydata, 
                                       ax=axis, s=40)

        # Updates axis title/labels
        axis.set_title((media_source + ' v. Twitter Keyword Frequency, Keyword:'
                        + ' ' + keyword.upper()))
        axis.set_xlabel(media_source + ' Keyword Frequency (Daily Bins)')
        axis.set_ylabel('Twitter Keyword Frequency (Daily Bins)')
    return figure, axes

def matches(visual):
    plt.figure()
    keyword = 'coronavirus'
    media_sources = ['the-verge', 'bloomberg']
    xdata, ydata = get_data(visual, keyword, media_sources)
    axes = plt.hist(xdata, [data for data in ydata])

def update_plot(visual, keyword, axes, canvas):
    '''
    Updates plot, given keyword associated with data to update with.

    Inputs:
     keyword (string): string representing which data to get,
     axes (numpy array): array of axes objects.
    '''
    # Iterates through axes, gets scatter collections and lines
    axes_list = axes.flatten() if type(axes) != list else axes
    for axis in axes_list:
        collections = axis.collections
        lines = axis.lines

        # Gets new data associated with new keyword, for given media (get from 
        #  title)
        title = axis.get_title()
        media_source = title.split(' ')[0]
        xdata, ydata = get_data(visual, keyword, media_source)

        # Clear axis, get max for new dataset, set new axis limits
        scatter_xdata, line_xdata = xdata
        scatter_ydata, line_ydata = ydata
        #axis.clear()
        xmax = max([max(scatter_xdata), max(line_xdata)])+2
        ymax = max([max(scatter_ydata), max(line_ydata)])+2
        axis.set_xlim([-2, xmax+2])
        axis.set_ylim([-2, ymax+2])
        print(scatter_xdata)
        print(scatter_ydata)

        # Plot new axis data, scatter and line
        #axis.scatter(scatter_xdata, scatter_ydata)
        #axis.plot(line_xdata, line_ydata)
        collection = collections[0]
        line = lines[0]
        offsets = [[x,y] for x,y in zip(scatter_xdata, scatter_ydata)]
        collection.set_offsets(offsets)
        line.set_xdata(line_xdata)
        line.set_ydata(line_ydata)

        # update title and axes labels
        axis.set_title((media_source + ' v. Twitter Keyword Frequency, '
                        'Keyword: ' + keyword.upper()))
        axis.set_xlabel(media_source + ' Keyword Frequency (Daily Bins)')
        axis.set_ylabel('Twitter Keyword Frequency (Daily Bins)')

    canvas.draw()

    # lists: axes.collections, axes.lines
    # line.s/get_x/ydata()
    # collection.s/get_offsets([[a,b],[c,d],...])
    # axes.plot(), axes.scatter()
    
    #axes = canvas.figure.axes[0]
    #axes.scatter(xdata, ydata)
    #axes.set_title(title)
    #canvas.draw()

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
        keyword, media_source = args
        scatter_xdata, scatter_ydata = (cleaning.word_frequency[keyword], 
                                        cleaning.word_frequency_news[keyword])
        print(len(scatter_xdata),len(scatter_ydata))
        intercept, coefficient = train_regressor(scatter_xdata, scatter_ydata)
        line_xdata = scatter_xdata
        line_ydata = [float(intercept) + float(coefficient)*x for x in range(len(line_xdata))]
        return (scatter_xdata, line_xdata), (scatter_ydata, line_ydata)
    if visual == 'Cumulative Twitter Frequency':
        keywords = args[0]
        xdata = list(cleaning.tweets_dates)
        ydata = [cleaning.word_frequency[keyword] for keyword in keywords]
        #xdata, ydata = range(60), [get_rand_line(60) for i in range(5)]
        return xdata, ydata
    if visual == 'Keyword Matching':
        xdata = list(cleaning.shared_dates)
        news_sources = list(cleaning.tweets_news_matches.keys())
        ydata = [cleaning.tweets_news_matches[source] for source in cleaning.news_sources]
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
