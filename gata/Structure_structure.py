""" ========== Genetic Aplications: Table Adapter (GA:TA) =========

$Id: Structure_structure.py
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

class Structure():

	"""
	 Structure structure (forgive the redundancy). It returns men and women format for Structure.
	"""

	def __init__(self, Data):

		if not isinstance(Data,Drt):
			raise ValueError("The file has not {} format. Call gata.readtable.Data('{}') \
				".format(Drt.__module__, Data))

		if not Data:
			raise ValueError('Data must be specified')

		# We take subpopulation 1:
		subpop1_w = Data.women4subpop
		subpop1_m = Data.men4subpop
		
		self.women = []
		self.men = []

		# Define Structure markers type
		self.marker_mod = []
		# The first column is population number, then markers
		self.marker_mod.append(str('POP'))
		for each in Data.markers:
			self.marker_mod.append(str(each).strip())

		# self.header is only for safer programming, but it will not be in output file
		self.header = ''
		for i in self.marker_mod:
			self.header = self.header + '{:7s}\t'.format(i)

		for i, each_pop in enumerate(Data.populations):
			auxPop = self.StructureType(Data, each_pop, i)
			self.women.append(auxPop[0])
			self.men.append(auxPop[1]) 

		self.data = []
		for i in range(len(self.women)):
			self.data.append(np.concatenate((self.women[i], self.men[i]), axis = 0) ) 

		self.data = np.concatenate(self.data, axis = 0)

		self.men = np.concatenate(self.men, axis = 0)

		self.women = np.concatenate(self.women, axis = 0)

		#Save data to a file
		self.Output(Data)

	def Output(self, Data):

		#Save data to a file
		OutputStrDF = pd.DataFrame(self.data)
		Writer = pd.ExcelWriter(Data.outputNameStr + Data.outputExtensionFile)
		OutputStrDF.to_excel(Writer, sheet_name = 'Sheet1', na_rep = ' ', index = False, header = False)
		Writer.save()

		OutputStrDFMen = pd.DataFrame(self.men)
		WriterMen = pd.ExcelWriter(Data.outputNameStr + 'Men' + Data.outputExtensionFile)
		OutputStrDFMen.to_excel(WriterMen, sheet_name = 'Sheet1', na_rep = ' ', index = False, header = False)
		WriterMen.save()

		OutputStrDFWomen = pd.DataFrame(self.women)
		WriterWomen = pd.ExcelWriter(Data.outputNameStr + 'Women' + Data.outputExtensionFile)
		OutputStrDFWomen.to_excel(WriterWomen, sheet_name = 'Sheet1', na_rep = ' ', index = False, header = False)
		WriterWomen.save()


	def StructureType(self, Data, pop, l):

		"""

		In this structure, women keep the same shape. Men are fake women with a -9 row and add a third row for each individual 
		with a weight (0.5 for women 1.0 for men) 
		This method work over one populations. __init__() interprets works with all.

		Parameters:
		------------
		ColSexType  == column with the 1 or 2 (men or women)
		ColPopNum == column with number of population
		ColIndNum == column with number of each individual (or name)
		ColMarkBegin == column where markers starts

		Return: 
		------------
			markersWom_forStr:   Markers for women population
			markersMen_forStr:   Markers for men population
		"""

		population = pop
		population_w = []
		population_m = []

		for each in population:
			if each[Data.ColSexType] == Data.IsWoman:
				population_w.append(each)
			elif each[Data.ColSexType] == Data.IsMan:
				population_m.append(each)

		markersWom_forStr = np.empty((len(population_w)+int(Data.women4subpop[l]),len(self.marker_mod)), dtype = object)#object)
		markersMen_forStr = np.empty((len(population_m)+2*Data.men4subpop[l],len(self.marker_mod)), dtype = object)#object)

		count_w = 0
		for i in range(0,len(population_w),2):
			
			markersWom_forStr[count_w,0] = int(population_w[i][Data.ColPopNum]) 
			markersWom_forStr[count_w+1,0] = int(population_w[i][Data.ColPopNum])
			markersWom_forStr[count_w+2,0] = ' '#Data.MARKER

			for j in range(1, len(self.marker_mod)):
				markersWom_forStr[count_w,j] = int(population_w[i][j + Data.ColMarkBegin - 1]) #'-1' because range() starts in 1
				markersWom_forStr[count_w+1,j] = int(population_w[i+1][j + Data.ColMarkBegin - 1])
				markersWom_forStr[count_w+2,j] = Data.STRWom #np.full((1,len(Data.n_markers)), 0.5)

			count_w += 3


		count_m = 0
		for i in range(0,len(population_m)):
			
			markersMen_forStr[count_m,0] = int(population_m[i][Data.ColPopNum]) 
			markersMen_forStr[count_m+1,0] = int(population_m[i][Data.ColPopNum])
			markersMen_forStr[count_m+2,0] = ' '#Data.MARKER 

			for j in range(1, len(self.marker_mod)):
				markersMen_forStr[count_m,j] = int(population_m[i][j + Data.ColMarkBegin - 1])
				markersMen_forStr[count_m+1,j] = Data.MARKER
				markersMen_forStr[count_m+2,j] = Data.STRMen #np.full((1,len(Data.n_markers)), 1.0)

			count_m += 3

		return markersWom_forStr, markersMen_forStr






