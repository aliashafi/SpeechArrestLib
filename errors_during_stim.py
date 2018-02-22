import os
import csv
import numpy as np
import pandas as pd
import glob

'''
Maansi Desai & Alia Shafi, November/December 2017 
Project: Speech Arrest 

This script reads in all csv files (one per patient) which contains data on stimulation time (onset and offset), error time (onset and off set), 
error type, and columns which record the presence of stimulation (denoted at Y). 
This script then performs a series of basic computations:
1) extracts the total number of each error type across ALL files 
2) identifies the times across all patients for which stimulation onset occurs "x amount" of milliseconds/seconds post trial and generated an error
3) outputs all relevant information into a csv file 
'''

#import all csv files
directoryPath = ('/Users/alia/Desktop/csv/*.csv')
files = glob.glob(directoryPath) 

#initialize variables for counting output 
patient_ID = 0
errorON = 0
errorOFF = 0
stimON = 0
stimOFF = 0
stimdur = 0
stim_latency = 0
error_latency = 0
patient = []

#create a df
frame = pd.DataFrame()
list_ = []

#read through csv files and import data
for read in files:
	reader = pd.read_csv(read,index_col=None, header=0, encoding = "ISO-8859-1")
	patient = read[-7:-4]

	# reader = reader[reader.stim == 'Y']
	# reader = reader[reader.error == 'motor']
	# reader = reader[reader.error != 'noplot']

#Extract what you need into dataframe
#	Need: pt ID		ErrorON		ErrorOFF	stimON		stimOFF		stimdur		stim latency	Error Lat. (this # will be negative, take only rows with - values)
	reader['during_stim_pos'] = reader['stim_onset'].astype(float) - reader['s_onset'].astype(float)
	reader['during_stim_neg'] = reader['s_onset'].astype(float) - reader['stim_offset'].astype(float)
	reader['stim_effect'] = reader['s_offset'].astype(float) - reader['stim_onset'].astype(float)
	reader['ptID'] = patient
	reader['num_error'] = reader['Unnamed: 14']
	# print(reader['ptID'])
	# print(reader)
	print(reader['Unnamed: 14'])
	for data in range(0,len(reader)):
		if data > 0:
			# print(reader['s_onset'][data-1])
			reader['onebefore_s_onset'].astype(float)
			reader['onebefore_s_onset'][data] = reader['s_onset'][data-1]
		else:
			reader['onebefore_s_onset'] = 0.0

	for data in range(0,len(reader)):
		if data > 0:
			# print(reader['s_onset'][data-1])
			reader['onebefore_s_offset'].astype(float)
			reader['onebefore_s_offset'][data] = reader['s_offset'][data-1]
		else:
			reader['onebefore_s_offset'] = 0.0

	reader['oneafter_s_onset'] = 0.0
	reader['oneafter_s_offset'] = 0.0
	for data in range(0,len(reader)-1):
		reader['oneafter_s_onset'][data] = reader['s_onset'][data+1]

	for data in range(0,len(reader)-1):
		reader['oneafter_s_offset'].astype(float)
		reader['oneafter_s_offset'][data] = reader['s_offset'][data+1]

	for data in range(0,len(reader)):
		if data > 1:
			# print(reader['s_onset'][data-1])
			reader['twobefore_s_onset'].astype(float)
			reader['twobefore_s_onset'][data] = reader['s_onset'][data-2]
		else:
			reader['twobefore_s_onset'] = 0.0

	for data in range(0,len(reader)):
		if data > 1:
			# print(reader['s_onset'][data-1])
			reader['twobefore_s_offset'].astype(float)
			reader['twobefore_s_offset'][data] = reader['s_offset'][data-2]
		else:
			reader['twobefore_s_offset'] = 0.0

	frame = frame.append(reader)


# print(reader[''])

#get rid of columns that will not be used in final output file
#del frame['stim_loc']
# del frame['stim']

##Replacing all blanks with 0
# frame['error'].fillna(0, inplace=True)
# frame['stim_loc'].fillna(0, inplace=True)
# frame['Unnamed: 14'].fillna(0, inplace=True)

print(frame['Unnamed: 14'])
#create column on a conditional based on given parameters
frame["during_stim_for_pos"] = np.where(frame["during_stim_pos"] > 0, 'yes', 'no')
frame["during_stim_for_neg"] = np.where(frame["during_stim_neg"] < 0, 'yes', 'no')
# frame = frame[frame.error == 'motor']
##for noplot
# frame = frame[frame.timePlot != 'noplot']


#output column names in new csv file with extracted info
frame = frame.reindex_axis(("ptID", "s_onset", "s_offset", "s_dur", "stim_onset", "stim_offset", "error", "Unnamed: 14", "during_stim_for_pos", "during_stim_for_neg", "stim_loc", "stim", "stim_effect", "onebefore_s_onset", 'onebefore_s_offset', 'twobefore_s_onset', 'twobefore_s_offset', 'oneafter_s_onset', 'oneafter_s_offset', "motor_subtype", "mov_subtype"), axis=1)
# frame = frame.dropna()



#At the end of the for loop, write data to csv files (make sure to append)
frame.to_csv('output.csv')


