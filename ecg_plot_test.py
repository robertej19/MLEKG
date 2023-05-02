import wfdb
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import AutoMinorLocator

import os
from math import ceil 
from PIL import Image


def plot_ECG_realistic(
        ecg, #pass as dataframe with columns named as leads
        filename):

    style = 'color'
    colors = ['black','black','black','black']#['black','red','blue','green']
    first_sec = ['I','II','III']
    second_sec = ['aVR','aVL','aVF']
    third_sec = ['V1','V2','V3']
    fourth_sec = ['V4','V5','V6']
    columns        = 4
    rows = 4 #4th row is a rhythm strip


    ecg = ecg.rename(columns={'AVR':'aVR','AVL':'aVL','AVF':'aVF'})

    # Parameters
    total_seconds  = 10 #duration of display ECG, in seconds
    sample_rate = 500 # in Hz

    # Plotting / Display parameters
    row_height     = 14
    display_factor = 1
    line_width = .7
    text_size = 9
    fig_size_hori = 1100
    fig_size_verti = 850
    y_offset = -4.5*np.array([0,1,2,3])


    ###################### Begin plotting ##########################
    if (style == 'bw'):
        color_major = (0.4,0.4,0.4)
        color_minor = (0.75, 0.75, 0.75)
        color_line  = (0,0,0)
    else:
        #color_major = (.9,0,0)
        #color_minor = (.9, 0.4, 0.4)
        color_major = (1,0,0)
        color_minor = (1, 0.7, 0.7)
    
    total_samples = total_seconds*sample_rate #Number of datapoints
    num_samples_per_section = total_samples/columns
    section_duration = total_seconds/columns

    sections = [first_sec,second_sec,third_sec,fourth_sec]
 
    #fig, ax = plt.subplots(figsize=(fig_size_hori,fig_size_verti))
    fig, ax = plt.subplots()
    
    display_factor = display_factor ** 0.5
    fig.subplots_adjust(
        hspace = 0, 
        wspace = 0,
        left   = 0,  # the left side of the subplots of the figure
        right  = 1,  # the right side of the subplots of the figure
        bottom = 0,  # the bottom of the subplots of the figure
        top    = 1
        )

    x_min, x_max = 0, total_seconds
    y_min, y_max = -row_height/4-row_height/4*rows, row_height/4

    # Red gridlines plotting
    ax.set_xticks(np.arange(x_min-.5,x_max+.5,0.2))    
    ax.set_yticks(np.arange(y_min,y_max,0.5))
    ax.minorticks_on() 
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.grid(which='major', linestyle='-', linewidth=0.35 * display_factor, color=color_major)
    ax.grid(which='minor', linestyle='-', linewidth=0.35 * display_factor, color=color_minor)

    #Set limits
    ax.set_ylim(y_min,y_max)
    ax.set_xlim(x_min-.5,x_max+.5)

    time = np.arange(num_samples_per_section) / sample_rate
    time_full = np.arange(total_samples) / sample_rate

    # Create the plots

    #Plot 2.5 seconds of each ECG lead
    for col_ind,column_section in enumerate(sections):
      for ind,lead in enumerate(column_section):
        x_start = section_duration*col_ind 
        x_end = section_duration*col_ind
        y_start = ecg[lead].iloc[0] + y_offset[ind] - 1.5
        y_end = ecg[lead].iloc[0] + y_offset[ind] -.25
        ax.plot([x_start, x_end],[y_start,y_end],
                linewidth=line_width * display_factor, color='black')
        ax.plot([x_start, x_end],[y_start+1.75,y_end+1.75],
                linewidth=line_width * display_factor, color='black')
        
                #plt.plot([x, x], [y_start, y_end])

        ax.text(section_duration*col_ind + .1, y_offset[ind] +1.8, lead, fontsize=text_size * display_factor)

        ax.plot(time+section_duration*col_ind, 
                ecg[lead].iloc[int(num_samples_per_section*col_ind):int(num_samples_per_section*(col_ind+1))].values + y_offset[ind], 
                linewidth=line_width * display_factor, color=colors[col_ind])


    # Include rhythm strip
    x_start = 0 
    x_end = 0
    y_start = ecg['II'].iloc[0] + y_offset[3] - 1.5
    y_end = ecg['II'].iloc[0] + y_offset[3] -.25
    ax.plot([x_start, x_end],[y_start,y_end],
        linewidth=line_width * display_factor, color='black')
    ax.plot([x_start, x_end],[y_start+1.75,y_end+1.75],
                linewidth=line_width * display_factor, color='black')

    ax.text(0+ .1, y_offset[3] +1.8, 'II', fontsize=text_size * display_factor)

    ax.plot(time_full, ecg['II'].iloc[0:total_samples].values + y_offset[3], linewidth=line_width * display_factor, color='black')

 
    file_name = filename+'.png'
    dpi = 300
    layout = 'tight'
    path = '/home/rober/MLECG/physionet.org/files/ptb-xl/figures/'
    intermediate_name = 'intermediate_fig.png'
    #plt.ioff()
    plt.savefig(intermediate_name, dpi = dpi, bbox_inches=layout)
    plt.close()

    # Open the image file
    image = Image.open(intermediate_name)

    width, height = image.size
    print(width, height)
    # Define the coordinates of the crop region
    left = 0.09*width
    top = 0.02*height
    right = 0.98*width
    bottom = 0.9*height

    # Crop the image using the defined region
    cropped_image = image.crop((left, top, right, bottom))

    # Save the cropped image
    cropped_image.save(path+file_name)
    #cropped_image.show()
    image.close()
    cropped_image.close()



# Create main function if name is main:
if __name__ == '__main__':

    dir_path = '/home/rober/MLECG/physionet.org/files/ptb-xl/1.0.3/records500/'


    # Get a list of all subdirectories in the directory
    subdirs = [f.path for f in os.scandir(dir_path) if f.is_dir()]

    # Print the list of subdirectories
    print("Subdirectories:")
    print(len(subdirs))
    counter = 0
    exceptions = []
    subdir_counter = 0
    for subdir in subdirs:
        print("on subdir: {}".format(subdir))
        subdir_counter += 1
        files = [os.path.join(subdir, f) for f in os.listdir(subdir) if os.path.isfile(os.path.join(subdir, f))]
        files = [f for f in files if "index" not in os.path.basename(f)]
        #remove the .hea and .dat from the file name endings:
        files = [f[:-4] for f in files]
        #remove the duplicates from the list
        files = list(dict.fromkeys(files))
        for file in files:
            try:
                filename = os.path.basename(file)
                print("on file: {}".format(file))
                print("counter: {}".format(counter))
                data  = wfdb.rdsamp(file)
                ecg_data = np.array(data[0])
                labels = data[1]['sig_name']
                df_ecg = pd.DataFrame(ecg_data, columns=labels)
                plot_ECG_realistic(df_ecg,filename)
                counter += 1

            except Exception as e:
                print(f"Exception while getting file size for {file}: {e}")
                exceptions.append(file)
        
        # Print any file names with exceptions
    if exceptions:
        print("Files with exceptions:")
        for exception in exceptions:
            print(exception)





    # data  = wfdb.rdsamp(path+filename)
    # ecg_data = np.array(data[0])
    # labels = data[1]['sig_name']

    # df_ecg = pd.DataFrame(ecg_data, columns=labels)

    # df_ecg.to_csv('df_ecg_test.csv')

    # #df = pd.read_pickle('df_ecg.pkl')

    # #run plot function
    # plot_ECG_realistic(df_ecg)
    # #plot(ecg_data.T)
