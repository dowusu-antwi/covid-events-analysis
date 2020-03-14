from execution import *
import gui
import plotting
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication

class AppStack(QtWidgets.QWidget):

    def __init__(self):
        '''
        Initializes application stack, consisting of a stack object and an
         object representing the list of elements on the stack.
        '''
        self.qapp = QApplication(sys.argv)
        super().__init__()
        stack = QtWidgets.QStackedWidget(self)
        stacklist = self.build_stacklist()
        self.stacklist_index = 0 # initialized to list beginning
        
        self.stacklist = self.resize_widget(stacklist, [0,0,1,0.05])
        self.stack = self.resize_widget(stack, [0,0.05,1,0.95])

    def build_stacklist(self):
        '''
        Builds the object representing the list of elements on the stack.

        No Inputs.

        Returns QListWidget, list of elements on the stack.
        '''
        stacklist = QtWidgets.QListWidget(self)
        stacklist.setFlow(QtWidgets.QListWidget.LeftToRight)
        stacklist.currentRowChanged.connect(self.display_page)
        return stacklist

    def display_page(self, index):
        '''
        Event handler for switching between pages on the stack.
        
        Inputs:
         index (integer): represents which page is currently displayed.
        '''
        self.stack.setCurrentIndex(index)

    def add_to_stack(self, page, name):
        '''
        Adds page to stack and stack list objects, incrementing the index for
         the next object to be placed on the stack.

        Inputs:
         page (QWidget): a page to add to the stack,
         name (string): a unique indicator for the corresponding page.
        '''
        self.stack.addWidget(page)
        self.stacklist.insertItem(self.stacklist_index, name)
        self.stacklist_index += 1

    def get_screen_resolution(self):
        '''
        Gets the current display screen resolution, in pixels.

        No Inputs.

        Returns list of width and height resolution dimensions, in pixels.
        '''

        desktop = QtWidgets.QDesktopWidget()
        width = desktop.screenGeometry().width()
        height = desktop.screenGeometry().height()
        return [width, height]

    def resize_widget(self, widget, dimensions):
        '''
        Sets the geometry of a widget, by ratio of the window screen
         dimensions (e.g., width = 0.8 -> 80% of the screen width).

        Inputs:
         widget (QtWidget object): pyqt widget to be resized,
         dimensions (list): dimensions for widget to be resized to, each in
                            terms of a ratio of the corresponding window
                            dimension.

        Returns resized widget.
        '''
        screen_width, screen_height = self.get_screen_resolution()
        x_ratio, y_ratio, width_ratio, height_ratio = dimensions

        x_position = x_ratio*screen_width
        y_position = y_ratio*screen_height
        width = width_ratio*screen_width
        height = height_ratio*screen_height

        widget.setGeometry(QtCore.QRect(x_position, y_position, width, height))
        return widget

if __name__ == "__main__":
    
    app_stack = AppStack()
    visuals = {0: 'Media v. Twitter Frequency Comparison', 
               1: 'Cumulative Twitter Frequency',
               2: 'Keyword Matching'}
    
    SEED_APPLICATION = False

    main_app = gui.App(SEED_APPLICATION)
    figure, axes = plotting.plot_seed(visuals[0])
    canvas = main_app.embed_figure(figure, [0, 0, 0.8, 0.85])
    keywords = cumulative_news_words
    main_app.embed_data_selector(keywords, [0.8, 0, 0.2, 0.85],
    			 canvas, visuals[0]) 
    app_stack.add_to_stack(main_app, 'Frequency Correlation')   
 
    main_app = gui.App(SEED_APPLICATION)
    figure, axes = plotting.plot_seed(visuals[1])
    canvas = main_app.embed_figure(figure, [0,0,0.965,0.9])
    app_stack.add_to_stack(main_app, 'Cumulative Frequency')

    main_app = gui.App(SEED_APPLICATION)
    figure, axes = plotting.plot_seed(visuals[2])
    canvas = main_app.embed_figure(figure, [0,0,0.8,0.85])
    main_app.embed_data_selector(news_sources, [0.8, 0, 0.2, 0.85],
                                 canvas, visuals[2])
    app_stack.add_to_stack(main_app, 'Matches')

    app_stack.showMaximized()
    sys.exit(app_stack.qapp.exec_())
