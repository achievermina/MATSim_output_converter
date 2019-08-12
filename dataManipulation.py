import xml.etree.ElementTree as ElementTree
from xml_convert import XmlListConfig
from xml_convert import XmlDictConfig
import xmltodict
import pprint
import json
import pandas as pd
import numpy as np
from datetime import date

class MATSimOutputToDataFrame():
    def __init__(self, root):

        # Initiate activity related list object
        id_data_act = []
        activity_data = []
        start_time = []
        end_time = []
        for type_tag in root.findall('person'):
            for act in type_tag.findall('plan/activity'):
                id_data_act.append(type_tag.get('id'))  # getting id
                activity_data.append(act.get('type'))  # getting work, home
                start_time.append(act.get('start_time'))
                end_time.append(act.get('end_time'))

        # Initiate mode related list object
        id_data_mode = []
        mode_data = []
        route_data = []
        trav_time =[]
        dist_data = []
        dep_list =[]

        for type_tag in root.findall('person'):
            if len(type_tag.findall('plan/leg')) == 0:
                id_data_mode.append(type_tag.get('id'))
                mode_data.append('na')
                route_data.append('na')
                dep_list.append('na')
                trav_time.append('na')
                dist_data.append('na')

            for i, mode in enumerate(type_tag.findall('plan/leg')):
                id_data_mode.append(type_tag.get('id'))
                mode_data.append(mode.get('mode'))
                dep_hr =mode.get('dep_time')
                trav_time.append(mode.get('trav_time'))
                route = mode.find('route')
                dist_data.append(route.get('distance'))

                # Departure time is sometimes bigger than 24 when it is the next day, so we have to change them to 24hr system
                dep_time =dep_hr.split(':')
                dep_time =int(dep_time[0])
                if dep_time >24:
                    dep_time =dep_time -24
                dep_list.append(dep_time)


                if i == len(type_tag.findall('plan/leg')) - 1:
                    id_data_mode.append(type_tag.get('id'))
                    mode_data.append('N/A')
                    route_data.append('N/A')
                    dep_list.append('N/A')
                    trav_time.append('N/A')
                    dist_data.append('N/A')


        actList = list(zip(id_data_act, activity_data, start_time, end_time))
        modeList = list(zip(mode_data ,dep_list ,trav_time ,dist_data))

        df_act = pd.DataFrame(actList, columns=['id', 'activity', 'start_time', 'end_time'])
        df_mode = pd.DataFrame(modeList, columns=['mode' ,'dep_time' ,'trav_time' ,'distance'])
        df_merged = pd.concat([df_act, df_mode], axis=1)


    def getModeShare(self, df_merged):
        self.df_agent_mode = df_merged[['id']].groupby(df_merged['mode']).count()
        return self.df_agent_mode

    def getDepartureTime(self,df_merged):
        self.df_agent_deptTime = df_merged[['activity','id']].groupby(df_merged['dep_time']).count()
        return self.df_agent_deptTime

    def mergeManhattanTripID(self, df_merged, man_id ):

        df_merged['id'] = df_merged['id'].astype(int)
        df_merged2 = pd.merge(df_merged, man_id, left_on='id', right_on='id', how='left')
        df_merged2['man_nonman'] = pd.to_numeric(df_merged2['man_nonman'])
        is_man = df_merged2['man_nonman'] == 1
        df_merged2_manOnly = df_merged2[is_man]
        return df_merged2_manOnly