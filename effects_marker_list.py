import os
import sys
import pandas as pd
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk

# Get file path to the effects list text file.
def get_file_path():
    user_info.destroy()
    my_file_types = [('text files', '.txt')]
    user_filepath = tk.filedialog.askopenfilename(parent = user_input_window, \
                title = 'Please choose an effect list file:', filetypes = my_file_types, \
                initialdir=os.path.expanduser('~/Desktop'))
    make_marker_list(user_filepath)

# Takes the file given by user along with the users parameters to create a new markers list.
def make_marker_list(filepath):
    user_input_window.destroy()
    effects_list = []   # Empty list that will be filled with matching effect name from user given file.
    
    # Split file name and file path to create the new file name in the same location.
    effects_file_path = os.path.dirname(filepath)
    marker_file_name = os.path.basename(filepath).split('.', 1)[0] + '-' + effect_name.get() + '.txt'
    marker_file_path = os.path.join(effects_file_path, marker_file_name)

    # Dummy proofs non input entry from users.
    if(marker_name.get() == ''):
        marker_name.set('Marker')
    if(effect_name.get() == ''):
        effect_name.set('No effect was given')
    # Opens file and checks for effect name in each line from file.
    with open(filepath) as fp:
        for line in fp:
            if effect_name.get().lower() in line.lower():
                effects_list.append(line.lstrip())

    # If effects were found create a dataframe from information gathered from file of effects.
    if(len(effects_list) > 0):
        marker_list = []
        for effect in effects_list:
            marker_list.append(effect.split('    '))

        marker_df = pd.DataFrame(marker_list)  
        marker_df.columns = ['track', 'color', 'start_tc', 'end_tc', 'comment'] # Rename columns to appropriate name.
        marker_df.loc[:, 'marker_name'] = marker_name.get()
        marker_df.loc[:, 'color'] = marker_colors[marker_choice.get()]
        # Reorder columns to correct order for Media Composer
        marker_df = marker_df[['marker_name', 'start_tc', 'track', 'color', 'comment']] 
        marker_df.sort_values('start_tc', inplace = True)   # Sort by earliest timecode
        # Remove an unwanted text from 'comment', 'track', 'start_tc' rows.
        marker_df.loc[:, 'comment'] = marker_df.loc[:, 'comment'].apply(lambda row: row.split('\n', 1)[0].lstrip())
        marker_df.loc[:, 'track'] = marker_df.loc[:, 'track'].apply(lambda row: row.replace('(', '').replace(')', ''))
        marker_df.loc[:, 'start_tc'] = marker_df.loc[:, 'start_tc'].apply(lambda row: row.lstrip())
        # Write text tab delimited file with no index or header information.
        # Media Composer doesn't need that information.
        marker_df.to_csv(marker_file_path, index = False, header = False, sep = '\t')
    else:
        return(f'No effect was found in {filepath}')

# Media Composer marker colors.
marker_colors = ['Red', 'Blue', 'Green', 'Cyan', 'Yellow', 'Magenta', 'Black', 'White']

# Create tkinter window and variables
user_input_window = tk.Tk()
user_input_window.title('Effects marker list')
user_info = tk.ttk.Frame(user_input_window)
effect_name = tk.StringVar()
effect_name.set('')
marker_choice = tk.IntVar()
marker_name = tk.StringVar()
marker_name.set('')
marker_choice.set(0)

user_info.pack()
tk.ttk.Label(user_info, text = 'Please choice a color for you markers.').grid()

# Loop to create radio button for all Media Composer marker colors.
for position, color in enumerate(marker_colors):
    tk.ttk.Radiobutton(user_info, text = color, variable = marker_choice, value = position).grid(sticky = tk.W)

tk.ttk.Label(user_info, text = 'Name of the effect you are looking for:').grid()
tk.ttk.Entry(user_info, textvariable = effect_name).grid(sticky = tk.W)
tk.ttk.Label(user_info, text = 'Please enter a name for your markers:').grid()
tk.ttk.Entry(user_info, textvariable = marker_name).grid(sticky = tk.W)
tk.ttk.Button(user_info, text = 'Cancel', command = user_input_window.destroy).grid(sticky = tk.W, row = 99, column = 0)
tk.ttk.Button(user_info, text = 'Okay', command = get_file_path).grid(sticky = tk.W, row = 99, column = 1)


user_input_window.mainloop()

