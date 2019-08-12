import xml.etree.ElementTree as ElementTree
from xml_convert import XmlListConfig
from xml_convert import XmlDictConfig
import dataManipulation
import xmltodict
import pprint
import json
import pandas as pd
import numpy as np
from datetime import date

## File directory
fileDirectory = '/Users/mina/Documents/NYU/BUILT/Matsim_Intermodal_comparison/raw/'
outputName = 'sample'
man_id = pd.read_csv('entire_man_nonman_subpopulation_id.csv')


## ADD file
xmlDataParsint(fileDirectory,0)
tree = ElementTree.parse(fileDirectory)
root = tree.getroot()
xmldict = XmlDictConfig(root)


MATSimOutputToDataFrame(root)