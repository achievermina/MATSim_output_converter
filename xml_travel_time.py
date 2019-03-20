import xml.etree.ElementTree as ElementTree
from xml_convert import XmlListConfig
from xml_convert import XmlDictConfig


import xmltodict
import pprint
import json
import pandas as pd
import numpy as np


### read data


tree = ElementTree.parse('/Users/mina/Documents/NYU/BUILT/Matsim_Intermodal_comparison/raw/BUILT.40.experienced_plans.xml')
root = tree.getroot()
xmldict = XmlDictConfig(root)


full_data = []
act = ['Home','Secondary','Work','University','School']
data=[]


for row in xmldict['person']:
    full_data.append(row['id'])
    full_data.append(row['plan']['activity'])


#full_data

    ###make the data to tuples to make dataFRAME

id_data = []
activity_data = []



for row in xmldict['person']:
    id_data.append(row['id'])
    activity_data.append(row['plan']['activity'])


data_tuples = list(zip(id_data, activity_data))
#data_tuples



    #make a DataFrame

df = pd.DataFrame(data_tuples, columns=['id','activity'])
#df
print("dataframe succeed")


act = ['Home', 'Secondary', 'Work', 'University', 'School']

new_list = []
index_list = pd.DataFrame(columns=['id'])
activity_list = pd.DataFrame(columns=['type', 'link', 'start_time', 'end_time', 'activity'])

## len(df.iloc[i]['activity']) occurs error when there is only one activity
### b/c its length is 4
### activity 가 하나일때 문제가 생김 - 일단 뺌 len =4 인것
print("activity extracting start")


df['activity'] = df['activity'].astype(list)

for i in range(0, 3500):  #len(df)
    activity_len = len(df.iloc[i]['activity'])

    for j in range(0, activity_len):

        # print(activity_len)

        if (activity_len != 4) and (df.iloc[i]['activity'][j]['type'] in act):
            # print(i,j,df.iloc[i]['activity'][j]['type'])

            ###make a index list
            index_list = index_list.append({'id': df.iloc[i]['id']}, ignore_index=True)
            # print(df.iloc[i]['id'])

            ###add activity to list
            new_list.append(df.iloc[i]['activity'][j])
            # print(new_list)

            ### append list to DataFrame
            activity_list = activity_list.append(new_list, ignore_index=True)
            new_list.clear()

print("activity extract succeed")
###merge index list and activity list

df_merged = pd.concat([index_list, activity_list], axis=1)
df_merged.head()

print("merge succeed")


df_merged['start_time']=pd.to_datetime(df_merged['start_time'])
df_merged['end_time']=pd.to_datetime(df_merged['end_time'])



### check travel time
trave_time = pd.DataFrame(columns={'id', 'travel_time'})

for i in range(0, len(df_merged) - 1):
    if (df_merged.iloc[i]['id'] == df_merged.iloc[i + 1]['id']):
        diff = pd.Timedelta(df_merged.iloc[i]['end_time'] - df_merged.iloc[i + 1]['start_time']).seconds / 3600
    else:
        diff = np.nan

    trave_time = trave_time.append([{'id': df_merged.iloc[i]['id'], 'travel_time': diff}], ignore_index=True)

print("travel time calculation succeed")

### merge

df_final =  pd.concat([df_merged, trave_time['travel_time']], axis=1)
#df_final

    ###group by id for travel_time

travel_time_comparison = df_final.groupby(['id']).sum()
#travel_time_comparison


    ### export excel file

travel_time_comparison.to_excel("forty_iteration_final.xlsx")
#df_merged.to_csv("sample2.csv",sep='\t', encoding='utf-8')

print("all process succeed")

