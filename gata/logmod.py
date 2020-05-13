import logging

__all__ = ['set_log']

def set_log(name):
	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)

	formatmain = logging.Formatter('%(asctime)s:%(name)s:%(message)s') 

	file_log = logging.FileHandler('log.txt')
	file_log.setLevel(logging.INFO)
	file_log.setFormatter(formatmain)

	#error_log = logging.FileHandler('log.txt')
	#error_log.setLevel(logging.WARNING)
	#error_log.setFormatter(formatmain)

	logger.addHandler(file_log)
	#logger.addHandler(error_log)
	return logging.getLogger(name)