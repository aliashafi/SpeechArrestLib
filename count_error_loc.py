import os
import csv
import numpy as np
import pandas as pd
from collections import defaultdict, Counter 

files = ('/Users/alia/Desktop/csv/output.csv')

patientID = 0
stim_location = 0
error = 0

#create a df
frame = pd.DataFrame()
#list_ = []

#read through csv files and import data
reader = pd.read_csv(files)
frame = frame.append(reader)


#get rid of columns that will not be used in final output file
# del frame['stim_loc']
# del frame['s_onset']
# del frame['s_offset']
# del frame['s_dur']
# del frame['stim_offset']
# # del frame['during_stim_pos']
# # del frame['during_stim_neg']
# del frame['stim_effect']
# del frame['during_stim_for_neg']



#.
frame["test"] = frame['ptID'] + ' ' + frame["stim_loc"]
#
frame = frame.reindex_axis(("ptID",  "error", "during_stim_for_pos","stim_loc", "test", 'stim'), axis=1)

frame['test'].fillna(0, inplace=True)

# print(frame)
frame.to_csv('column_output_stim_loc.csv')



input_file = open('column_output_stim_loc.csv')
csv_reader = csv.reader(input_file)

data = defaultdict(list)
#data2 = defaultdict(list)

for row in csv_reader:
	data[row[5]].append(row[2])
	#data[row[6]].append(row[4])



df = pd.DataFrame.from_dict(data, orient='index')


df["count_motor"] = 0
df["count_word"] = 0
# df["count_syl"] = 0
df["other_errors"] = 0
df['total_stimulations_at_site'] = 0
df["comorbid"] = 'n'





for i in range(0,len(df)):
	for cols in df:
		if df[cols][i] == 'motor':
			df["count_motor"][i] += 1
			df['total_stimulations_at_site'][i] += 1
		if df[cols][i] == 'word':
			df["count_word"][i] += 1
			df['total_stimulations_at_site'][i] += 1
		if df[cols][i] == 'syllable':
			# df["count_syl"][i] += 1
			df['total_stimulations_at_site'][i] += 1
			df['other_errors'][i] += 1
		if df[cols][i] == '0':
			df['total_stimulations_at_site'][i] += 1
		if df[cols][i] == 'number':
			df['total_stimulations_at_site'][i] += 1
			df['other_errors'][i] += 1

df["% word"] = df["count_word"]/df['total_stimulations_at_site']
df["% motor"] = df["count_motor"]/df['total_stimulations_at_site']
df["% error"] = (df["count_motor"] + df["count_word"] + df["other_errors"])/df['total_stimulations_at_site']

for i in range(0,len(df)):
	if df["count_word"][i] != 0 and df["count_motor"][i] != 0:
		df["comorbid"][i] = 'y'

for cols in range(0,28):
	del df[cols]




df.to_csv('error_sites.csv')
#csv.write(data)
















#frame = frame.dropna()
#length = len(frame)
# print(frame['stim_loc'][2])
# frame_genius = pd.DataFrame()
# frame_genius["brain_loc"] = range(0,length)
# frame_genius["ptID"] = range(0,length)
# # frame_genius["motor_error"] = range(0,length)

# frame_genius["ptID"] = frame_genius["ptID"]*0
# frame_genius["brain_loc"] = frame_genius["brain_loc"]*0

# frame_genius["brain_loc"][1] == frame['stim_loc'][1]

# for i in range(1,length):
# 	if frame['stim_loc'][i] != frame['stim_loc'][i-1]:
# 		frame_genius["brain_loc"][i] = frame['stim_loc'][i]
# 		frame_genius["ptID"][i] = frame['ptID'][i]
	
# 	# if frame_genius["brain_loc"][i] == frame['stim_loc'][i-1]:
	

		

# 	# if frame['stim_loc'][i] != frame['stim_loc'][i-1]:
# 	# 	frame['test'] = frame['stim_loc'][i]

# print(frame_genius)

# frame.to_csv('column_output_stim_loc.csv')
#print(reader)







