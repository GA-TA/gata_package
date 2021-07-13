import logging

__all__ = ['set_log']

def set_log(name, setLevel = 10):
	"""
	Arguments
	========= 
		name: 
			Recommended value = __name__ . Using such value you'll know where the programm was running.
		setLevel: int. 
			Values according logging.setLevel = 0 (not set) - 10 (debug)- 20 (info)- 
												30 (warning)- 40 (error)- 50 (critical)
	Return
	=========
		logger instance
	"""

	logger = logging.getLogger(name)
	logger.setLevel(setLevel)

	formatmain = logging.Formatter('%(asctime)s:%(name)s:%(message)s') 

	file_log = logging.FileHandler('log.txt')
	file_log.setLevel(logging.INFO)
	file_log.setFormatter(formatmain)

	logger.addHandler(file_log)

	return logging.getLogger(name)