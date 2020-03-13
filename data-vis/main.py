#!/usr/bin/env python3

'''
Main application starter for data visualization.
'''

## Hard-coded Data Visualization Types
VISUALS = {0: 'Frequency Comparison'
           1: 'Keyword Matches'
           2: 'Keyword Frequency'
           3: 'Keyword Frequency, Live Plotting'}

def build_start_page():
    '''
    ...
    '''
    # Creates '...' text and 'Launch' button
    title = QtWidgets.QLabel(app)
    title.setText('Main Application')
    font = QtGui.QFont('Arial', 30, QtGui.QFont.Bold)
    title.setFont(font)
    launch_button = QtWidgets.QPushButton('Launch', app)

    # Positions text in the center, with button just below it
    app.resize_widget(title, [0.415,0.1,0.8,0.2])
    app.resize_widget(launch_button, [0.45,0.3,0.1,0.05])

    # Connects button to application page launcher (clearing the current text
    #  and button widgets from the page afterwards)
    button.clicked.connect(lambda: [button.setParent(None), 
                                    title.setParent(None)])

def build_application_pages():
    '''
    ...
    '''


def main():
    '''
    Runs the necessary subroutines to create and initialize the application: 
     1. Creates the start page,
     2. Creates the pages for each data visualization type,
     3. Maximizes the final window.
    '''

    ## Create the start page,
    app = build_start_page()

    ## Creates the pages for each visual,
    for index in VISUALS:
        visual = VISUALS[index]

    ## Maximizes the final window.
    app.showMaximized()

if __name__ == "__main__":
    main()
    
