""" ========== Genetic Aplications: Table Adapter (GA:TA) =========

This software was developed thanks to finantial support from CONICET (Argentina)

Authors (alphabetical order): del Palacio, S.; Di Santo, P.; Gamboa Lerena, M. M.
Contact: unlpbiotec@gmail.com

Thanks to Federico Lopez Armengol for helping us with the meta structure and Github usage

Latest upload: May 2020

"""

import sys
import os
import numpy as np
import pandas as pd
from gata.readtable import Data
from gata.R_structure import R
from gata.Arlequin_structure import Arlequin
from gata.Structure_structure import Structure

'''Call the class to read the input table and store information'''
#read the table and return a data with many atributes

# Condition that no argument equals to producing all outputs (currently 3 tables)
if len(sys.argv) == 3:
	argum = set(sys.argv[1].lower())
	data = Data(sys.argv[2])
else:
	argum = 'ras'
	data = Data(sys.argv[1]) 

if data.info:
	print('{0} file contains {1} individuals: {2} women and {3} men.'.format(
	argum, data.total_MenWomen, data.n_women, data.n_men))
	print('The sheet has {0} subpopulations, each one with {1} individuals'.format(data.totalPopulations, data.n_each_population))
	print('Number of markers: {0}. Marker names: {1}'.format(data.n_markers, data.markers))
	#print np.shape(data.markers)
	print('Women per subpopulation', data.women4subpop)
	print('Men per subpopulation', data.men4subpop)
	print('Filevalues dimensions', np.shape(data.fileValues))

if 'r' in argum:
	R(data)

if 'a' in argum: 
	Arlequin(data)

if 's' in argum:
	Structure(data)

#if not 'r' in argum or not 'a' in argum or not 's' in argum: 
#	raise ValueError('You have to specify r (for R), a (for Arlequin) or s (for Structure) parameter.')


