from gata.readtable import Data
#import gata.R_structure as R
from gata.R_structure import R
import sys
file = '../generic_table.xlsx'

data=Data(file)

#print(data)

R(data)
