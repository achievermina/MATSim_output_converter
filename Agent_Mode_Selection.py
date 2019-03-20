import xml.etree.ElementTree as ElementTree
from xml_convert import XmlListConfig
from xml_convert import XmlDictConfig


import xmltodict
import pprint
import json
import pandas as pd
import numpy as np


## File directory
fileDirectory = '/Users/mina/Documents/NYU/BUILT/Matsim_Intermodal_comparison/raw/'
outputName = 'sample'


xmlDataParsint(fileDirectory,0)

## ADD file

tree = ElementTree.parse(fileDirectory)
root = tree.getroot()
xmldict = XmlDictConfig(root)

print(xmldict)