""" ========== Genetic Aplications: Table Adapter (GA:TA) =========

$Id: tools.py
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
import unidecode as ucd

def SingleMenTable(popname):

	"""
	This method will change the number in PopName in the output mens table.
	Parameter:
	----------
	popname: array with the population name (the number)
	Return:
	----------
	popname: array with the population name number reseted (from 1, 01, 001, etc.. depends the number of digits)

	"""

	namecol = popname.T[0]
	ndim = len(namecol)
	
	# Number of digits
	digits = len(str(ndim))

	print(digits)
	count = 1

	for i in np.arange(0,len(namecol)):
		
		if namecol[i] != ' ':
			string = ucd.unidecode(namecol[i])
			string = string[:-digits] + str(count).zfill(digits)
			#namecol[i] = unicode(string)
			namecol[i] = string
		else:
			string = namecol[i-1]
			popname.T[1][i] = 1	
			string = string[:-digits] + str(count).zfill(digits)
			#namecol[i] = unicode(string)
			namecol[i] = string

		count+=1
	
	popname.T[0] = namecol

	return popname

