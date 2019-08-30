from PyQt5.QtWidgets import (QApplication, QWidget, QComboBox, QGroupBox, QFormLayout,
                             QLabel, QDialogButtonBox, QVBoxLayout, QDialog, QSpinBox, 
                             QFileDialog, QLineEdit)
from PyQt5.QtGui import QIcon
import os
import sys
import pandas as pd

# Validates given track number as well as formats for Media Composer by adding 'V'
def validate_track_number(track_name):
    try:
        temp_number = int(track_name)
    except ValueError:
        temp_number = 1
    track = 'V' + str(temp_number)
    return(track)

# Takes the file given by user along with the users parameters to create a new markers list.
def make_marker_list(user_input):
    file_path = user_input.file_path
    marker_name = user_input.marker_name.text()
    effect_name = user_input.effect_name.text()
    marker_color = user_input.marker_color.currentText()
    track_num = user_input.track_num.text()
    
    effects_list = []   # Empty list that will be filled with matching effect name from user given file.
    in_effects_list = False
    track = validate_track_number(track_num)
    
    # Split file name and file path to create the new file name in the same location.
    effects_file_path = os.path.dirname(file_path)
    marker_file_name = os.path.basename(file_path).split('.', 1)[0] + '-' + effect_name + '.txt'
    marker_file_path = os.path.join(effects_file_path, marker_file_name)

    # Dummy proofs non input entry from users.
    if(marker_name == ''):
        marker_name = 'Marker'
    if(effect_name == ''):
        effect_name = 'No effect was given'
    # Opens file and checks for effect name in each line from file.
    with open(file_path) as fp:
        for line in fp:
            if 'Effect Location Summary:' in line:
                in_effects_list = False
            if effect_name.lower() in line.lower() and in_effects_list == True:
                effects_list.append(line.lstrip())
            if '  __ TRACK __  __ START TC __  ___ END TC ___    __________ EFFECT NAME __________' in line:
                in_effects_list = True


    # If effects were found create a dataframe from information gathered from file of effects.
    if(len(effects_list) > 0):
        marker_list = []
        for effect in effects_list:
            marker_list.append(effect.split('    '))

        marker_df = pd.DataFrame(marker_list)  
        marker_df.columns = ['track', 'color', 'start_tc', 'end_tc', 'comment'] # Rename columns to appropriate name.
        marker_df.loc[:, 'marker_name'] = marker_name
        marker_df.loc[:, 'color'] = marker_color
        # Reorder columns to correct order for Media Composer
        marker_df = marker_df[['marker_name', 'start_tc', 'track', 'color', 'comment']] 
        marker_df.sort_values('start_tc', inplace = True)   # Sort by earliest timecode
        # Remove an unwanted text from 'comment', 'track', 'start_tc' rows.
        marker_df.loc[:, 'comment'] = marker_df.loc[:, 'comment'].apply(lambda row: row.split('\n', 1)[0].lstrip())
        marker_df.loc[:, 'track'] = track
        marker_df.loc[:, 'start_tc'] = marker_df.loc[:, 'start_tc'].apply(lambda row: row.lstrip())
        # Write text tab delimited file with no index or header information.
        # Media Composer doesn't need that information.
        marker_df.to_csv(marker_file_path, index = False, header = False, sep = '\t')
    else:
        return(f'No effect was found in {file_path}')

# Create the PyQt5 class object for user input.
class User_Input(QDialog):
    def __init__(self):
        super(User_Input, self).__init__()
        self.createFormGroupBox()
        
        # Create our buttons
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.showDialog)
        buttonBox.rejected.connect(self.reject)
        
        # Set our widget layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setGeometry(50, 50, 0, 0)
        self.setLayout(mainLayout)
        
        self.setWindowTitle('Marker List Info')
        
    # Main user input form    
    def createFormGroupBox(self):
        self.marker_color = QComboBox(self)
        self.track_num = QSpinBox()
        self.marker_name = QLineEdit()
        self.effect_name = QLineEdit()
        
        for color in marker_colors:
            self.marker_color.addItem(color) # Add marker colors to our drop menu
        self.track_num.setMinimum(1)
        self.track_num.setMaximum(99)
            
        self.formGroupBox = QGroupBox("Form layout")
        layout = QFormLayout()
        layout.addRow(QLabel("Marker Name:"), self.marker_name)
        layout.addRow(QLabel('Effect Name:'), self.effect_name)
        layout.addRow(QLabel("Marker Color:"), self.marker_color)
        layout.addRow(QLabel("Video Track:"), self.track_num)
        self.formGroupBox.setLayout(layout)
        self.show()
        
    # Get the file location from user 
    def showDialog(self):
        self.hide()
        fname = QFileDialog.getOpenFileName(self, 'Open File', os.path.expanduser('~/Desktop'), 'Text Files (*.txt);; All Files (*.*)')
        
        if fname[0]:
            self.file_path = fname[0]
            make_marker_list(self)

# Media Composer marker colors.
marker_colors = ['Red', 'Blue', 'Green', 'Cyan', 'Yellow', 'Magenta', 'Black', 'White']

if __name__ == '__main__':

    # app = QApplication(sys.argv)
    marker_app = QApplication.instance() # checks if QApplication already exists
    if not marker_app: # create QApplication if it doesnt exist
        marker_app = QApplication(sys.argv)
        # marker_app = QWidget.QApplication(sys.argv)
    ex = User_Input()
    marker_app.exec_()