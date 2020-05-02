""" ========== Genetic Aplications: Table Adapter (GA:TA) =========

$Id: readtable.py
$created: Jul 2018
$auth(alphabetical order): del Palacio, S.; Di Santo, P.; Gamboa Lerena, M. M.
$license: GPLv3 or later, see https://www.gnu.org/licenses/gpl-3.0.txt

          This is free software: you are free to change and
          redistribute it.  There is NO WARRANTY, to the extent
          permitted by law.

Contact: unlpbiotec@gmail.com
Technical contact: mgamboa@fcaglp.unlp.edu.ar

This software was developed thanks to finantial support from CONICET (Argentina)

Thanks to Federico Lopez Armengol for helping us with the meta structure and Github usage

Latest upload: July 2019

"""

import numpy as np
import pandas as pd
import os
import sys 

class Data():
	
	def __init__(self, inputTable):
		
		"""
		Input:
		----------
			. inputTable = data file name. 	
				Rows: 1 = column infomation, 2 to last = individuals, 
				Cols: 1 = population name, 2 = individual number, 3 = sex (1 = M, 2 = F), 4 = population number, 5 to last=markers 

		Return:
		----------
			A set of atributes.

			. nameColumn: column names. Type = numpy.array (strings) with shape = (4 + number of markers)  
			. fileValues: array with all the values (id, sex, pop and markers)
							Type = numpy.array, shape = (number of individuals, 4 + number of markers)
			. n_women: total number of women in the file. Type = int
			. n_men: total number of men in the file. Type = int
			. total_MenWomen: total number of individuals in the file (n_women + n_men)
			. men4subpop: number of men in each subpopulation
							Type = list (integers) with shape = (number of subpopulations)
			. women4subpop: number of women in each subpopulation 
							Type = list (integers) with shape = (number of subpopulations)
			. n_each_population: total number of individuals in each subpopulation
							Type = numpy.array (integers) with shape = (number of subpopulations)  
			. totalPopulations: number of subpopulations in the file. Type = int
			. populations: Data Info of the entire file. Type = list (arrays) with shape = (number of subpopulations)
			. n_markers: number of markers. Type = int
			. markers: name of markers. Type = numpy.array (strings) with shape = (number of markers)
		
		__init__ use Pandas for reading only one sheet of the Excel file. 

		"""
		
		self.file = inputTable

		# Convert .ods to .xlsx if needed
		if self.file.split('.')[-1] == 'ods':
			os.system('ssconvert '+ self.file + ' '+ self.file.split('.')[0]+'.xlsx')
			self.file = self.file.split('.')[0]+'.xlsx'
		
		# Load file parameters
		self.Parameters()		
		
		allFile = pd.ExcelFile(self.file)

		# Only one sheet admited  
		if len(allFile.sheet_names) > 1: 
			raise ValueError('The program does not support more than 1 sheet')
		elif len(allFile.sheet_names) == 1: 
			sheet0 = allFile.sheet_names[0]

		# Read THE sheet and create a sheetData atribute with all the info of the file
		self.sheetData = allFile.parse(sheet0)
		# create column name and column values 
		self.nameColumn, self.fileValues = self.sortData()
		self.n_women, self.n_men, self.total_MenWomen = self.WoMen() 	
		self.men4subpop, self.women4subpop, self.n_each_population, self.totalPopulations,self.populations = self.Populations()
		self.n_markers, self.markers = self.Markers()

	def Parameters(self):
			
		"""
		Hardcoded parameters for testing table generic_table.xlsx

		info == [boolean] print some info of the input file
		ColSexType  == [int] column with 1 or 2 (man or woman)
		ColPopNum == [int] column with number of population
		ColIndNum == [int] column with number of each individual (or name)
		ColMarkBegin == [int] column in which markers start
		
		outputNameR == [str] prefix output name
		
		ARLQINDEX == [int] same kind of sex for Arlequin
		MARKER == [int] set marker param for the table
		outputNameArlq == [str] prefix output name
		
		STRWom == [float] Structure women param for filling
		STRMen == [float] Structure men param for filling
		outputNameStr == [str] prefix output name
		
		"""

		self.info = True

		self.IsMan = 1
		self.IsWoman = 2
		self.ColPopName = 0 
		self.ColIndNum = 1
		self.ColSexType = 2
		self.ColPopNum = 3
		self.ColMarkBegin = 4

		self.outputNameR = self.file.split('/')[-1].split('.')[0] + '_R'
	
		self.ARLQINDEX = 1 #same type of sex for Arlequin
		self.MARKER = -9
		self.outputNameArlq = self.file.split('/')[-1].split('.')[0] + '_Arlequin'

		self.STRWom = 0.5
		self.STRMen = 1.0
		self.outputNameStr = self.file.split('/')[-1].split('.')[0] + '_Structure'

		self.outputExtensionFile = '.xlsx'

	def sortData(self):

		"""
		return: 
		----------
		columnName, columnValues
		"""

		columnName=[]
		for each in self.sheetData.columns:
			columnName.append(each)
		columnValues = []
		for each in self.sheetData.values:
			columnValues.append(each)

		return np.array(columnName), np.array(columnValues)

	
	def WoMen(self):

		"""
		ColSexType  == column with the 1 or 2 (man or woman)

		return: 
		----------
		number of women, men and total individuals in the file
		
		"""

		countWomen = 0
		countMen = 0

		for each in self.fileValues.T[self.ColSexType]:
			if each == 2:
				countWomen += 1
			elif each == 1:
				countMen += 1

		return countWomen/2, countMen, countWomen/2 + countMen 

	def Populations(self):

		"""
		ColSexType  == column with the 1 or 2 (man or woman)
		ColPopNum == column with number of population
		return: 
		-----------
		total number of populations in the spreadsheet

		"""
		countWomen = []
		countMen = []
		
		#init counters

		countWomen_i = 0
		countMen_i = 0
		
		# initialize the first subpopulation 
		# pop_index = array with the population tags
		# sex_index = array with the sex values

		sex_index, pop_index = self.fileValues.T[self.ColSexType], self.fileValues.T[self.ColPopNum]
		index = pop_index[0]

		# store women and men for each population. shape(popul) = (number of populations,...)
		popul = []

		# count for each subpopulation
		aux=[]
		for i,each in enumerate(pop_index):
			
			# auxiliar for saving number of men and women for one population
			if each == index and sex_index[i] == 2:
				#count women
				countWomen_i += 1
				aux.append(self.fileValues[i])
			elif each == index and sex_index[i] == 1:
				#count men
				countMen_i += 1
				aux.append(self.fileValues[i])
			# partial saving of women and men populations: if i<len() continue, else save the last population
			if i < len(pop_index)-1 and pop_index[i+1] == index + 1:
				index += 1    
				countWomen.append(int(countWomen_i/2))
				countMen.append(int(countMen_i))
				countWomen_i=0
				countMen_i = 0
				popul.append(aux)
				aux = []
			elif i == len(pop_index)-1:
				countWomen.append(int(countWomen_i/2))
				countMen.append(int(countMen_i))
				popul.append(aux)

		total_subpop = np.array(countWomen)+np.array(countMen)
		number_subpop = len(total_subpop)
		
		return countMen, countWomen, total_subpop, number_subpop, popul

	def Markers(self):

		"""
		ColMarkBegin == column where begins the markers

		return: 
		---------
		number of markers

		"""

		return len(self.fileValues.T[self.ColMarkBegin:]), self.nameColumn.T[self.ColMarkBegin:]


