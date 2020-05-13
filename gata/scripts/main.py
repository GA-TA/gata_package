""" ========== Genetic Aplications: Table Adapter (GA:TA) =========

This software was developed thanks to finantial support from CONICET (Argentina)

Authors (alphabetical order): del Palacio, S.; Di Santo, P.; Gamboa Lerena, M. M.
Contact: unlpbiotec@gmail.com

Thanks to Federico Lopez Armengol for helping us with the meta structure and Github usage

Latest upload: May 2020

"""

import sys
import os
#import logging
import numpy as np
import pandas as pd
from gata.readtable import Data
from gata.R_structure import R
from gata.Arlequin_structure import Arlequin
from gata.Structure_structure import Structure
from gata.logmod import set_log
#set debug level
#logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
#formatmain = logging.Formatter('%(asctime)s:%(name)s:%(message)s') 
#file_log = logging.FileHandler('log.txt')
#file_log.setLevel(logging.DEBUG)
#file_log.setFormatter(formatmain)
#logger.addHandler(file_log)

'''Call the class to read the input table and store information'''
#read the table and return a data with many atributes

# Condition that no argument equals to producing all outputs (currently 3 tables)

logger = set_log(__name__)
if len(sys.argv) == 3:
	logger.info('Setting...')
	argum = set(sys.argv[1].lower())
	file = sys.argv[2]
	logger.info('Loading file {}'.format(file))
	data = Data(file)
	logger.info('Loading done.')
else:
	logger.info('Setting...')
	argum = 'ras'
	file = sys.argv[1]
	logger.info('Loading file {}'.format(file))
	data = Data(file) 

if data.info:
	logger.info('{0} file contains {1} individuals: {2} women and {3} men.'.format(file, data.total_MenWomen, data.n_women, data.n_men))
	logger.info('The sheet has {0} subpopulations, each one with {1} individuals'.format(data.totalPopulations, data.n_each_population))
	logger.info('Number of markers: {0}. Marker names: {1}'.format(data.n_markers, data.markers))
	logger.info('Women per subpopulation {0}'.format( str(data.women4subpop)))
	logger.info('Men per subpopulation {0}'.format(data.men4subpop))
	logger.info('Filevalues dimensions {0}'.format(np.shape(data.fileValues)))

if 'r' in argum:
	logger.info('R: Converting format')
	R(data)
	logger.info('R: Done.')
if 'a' in argum: 
	logger.info('Arlequin: Converting format')
	Arlequin(data)
	logger.info('Arlequin: Done.')
if 's' in argum:
	logger.info('Converting Structure format')
	Structure(data)
	logger.info('Structure: Done.')


#if not 'r' in argum or not 'a' in argum or not 's' in argum: 
#	raise ValueError('You have to specify r (for R), a (for Arlequin) or s (for Structure) parameter.')


