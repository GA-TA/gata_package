""" ========== Genetic Aplications: Table Adapter (GA:TA) =========

$Id: Arlequin_structure.py
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
from gata.readtable import Data as Drt
import gata.tools as tl

class Arlequin(object):

	""" Arlequin structure. It returns men and women format for Arlequin."""

	def __init__(self, Data):

		if not isinstance(Data,Drt):
			raise ValueError("The file has not {} format. Call gata.readtable.Data('{}') \
				".format(Drt.__module__, Data))

		if not Data:
			raise ValueError('Data must be specified')

		# Take subpopulation 1:
		subpop1_w = Data.women4subpop
		subpop1_m = Data.men4subpop
		
		self.women = []
		self.men = []
		self.onlymenfile = [] # this array will be to renumber the popname for the men output file 

		# Define Arlequin markers type
		self.marker_mod = []
		# The first two columns are indivudual number (reset for each subpopulation) and population number, then markers
		self.marker_mod.append(str('IND'))
		self.marker_mod.append(str('POP'))

		for each in Data.markers:
			self.marker_mod.append(str(each).strip())

		# self.header is only for safer programming, but it will not be in the output file
		self.header = ''
		for i in self.marker_mod:
			self.header = self.header + '{:7s}\t'.format(i)

		for i, each_pop in enumerate(Data.populations):
			auxPop = self.ArlequinType(Data, each_pop, Data.men4subpop[i])
			self.women.append(auxPop[0])
			self.men.append(auxPop[1])

			newaux = np.copy(auxPop[1])
			# Reset count number for men's file (and only for that file) starting from 01
			self.onlymenfile.append(newaux)
			self.onlymenfile[i] = tl.SingleMenTable(self.onlymenfile[i])

		#for ie in self.men:
		#	print(ie)
		self.data = []
		for i in range(len(self.women)):
			self.data.append(np.concatenate((self.women[i], self.men[i]), axis = 0) ) 
		
		self.data = np.concatenate(self.data, axis = 0)

		self.men = np.concatenate(self.men, axis = 0)

		self.women = np.concatenate(self.women, axis = 0)

		self.onlymenfile = np.concatenate(self.onlymenfile, axis = 0)
		# Save data to a file
		self.Output(Data)

	def Output(self, Data):

		#Save data to a file
		OutputArlqDF = pd.DataFrame(self.data)
		Writer = pd.ExcelWriter(Data.outputNameArlq + Data.outputExtensionFile)
		OutputArlqDF.to_excel(Writer, sheet_name = 'Sheet1', na_rep = ' ', index = False, header = False)
		Writer.save()

		OutputArlqDFMen = pd.DataFrame(self.onlymenfile)
		WriterMen = pd.ExcelWriter(Data.outputNameArlq + 'Men' + Data.outputExtensionFile)
		OutputArlqDFMen.to_excel(WriterMen, sheet_name = 'Sheet1', na_rep = ' ', index = False, header = False)
		WriterMen.save()

		OutputArlqDFWomen = pd.DataFrame(self.women)
		WriterWomen = pd.ExcelWriter(Data.outputNameArlq + 'Women' + Data.outputExtensionFile)
		OutputArlqDFWomen.to_excel(WriterWomen, sheet_name = 'Sheet1', na_rep = ' ', index = False, header = False)
		WriterWomen.save()

	def ArlequinType(self, Data, pop, m4subpop):

		"""

		In this structure, women keep the same format. 
		This method works over one population. __init__() interprets all.
		
		Parameters (used from Data):
		---------
		
			ColSexType: column with the 1 or 2 (man or woman)
			ColPopNum: column with number of population
			ColIndNum: column with number of each individual
			ColMarkBegin: column where markers start
			ARLQINDEX: 1 , same kind of sex for Arlequin
			MARKER: -9 for missing data
			m4subpop: number of mens in the subpop. With this number we complete zfill(Fill)

		Return: 
		---------
		
			markersWom_forArlq: Markers for women population 
			markersMen_forArlq: Markers for men population

		"""

		# Compute number of digits of number of men
		Fill = len(str(m4subpop))

		population = pop
		PopName = population[0][Data.ColPopName]
		population_w = []
		population_m = []

		for each in population:
			if each[Data.ColSexType] == Data.IsWoman:
				population_w.append(each)
			elif each[Data.ColSexType] == Data.IsMan:
				population_m.append(each)
		
		# Checks if the male population (=fake women) is odd or even:
		if len(population_m)%2 == 0:
			pass
		elif len(population_m)%2 == 1:
			# Missing data is set to -9 (can be changed if needed)
			population_m.append([-9 for x in range(np.shape(population_m)[1])])

		markersWom_forArlq = np.empty((len(population_w),len(self.marker_mod)), dtype = object)#np.int8)
		markersMen_forArlq = np.empty((len(population_m),len(self.marker_mod)), dtype = object)

		for i in range(0,len(population_w),2):
			markersWom_forArlq[i,0] = PopName+str(population_w[i][Data.ColIndNum]).zfill(Fill)
			markersWom_forArlq[i,1] = int(Data.ARLQINDEX)
			
			markersWom_forArlq[i+1,0] = ' ' 
			markersWom_forArlq[i+1,1] = ' '
			for j in range(2, len(self.marker_mod)):
				markersWom_forArlq[i,j] = int(population_w[i][j+2])
				markersWom_forArlq[i+1,j] = int(population_w[i+1][j+2])

		count = len(population_w)/2
		
		for i in range(0,len(population_m),2):
			count += 1
			markersMen_forArlq[i,0] = PopName+str(int(count)).zfill(Fill)
			markersMen_forArlq[i,1] = int(Data.ARLQINDEX)

			markersMen_forArlq[i+1,0] = ' '
			markersMen_forArlq[i+1,1] = ' '
			
			for j in range(2, len(self.marker_mod)):
				markersMen_forArlq[i,j] = int(population_m[i][j+2])
				markersMen_forArlq[i+1,j] = int(population_m[i+1][j+2])

		return markersWom_forArlq, markersMen_forArlq




