from libc.string cimport memset

def zeromem(x):
	memset(<char*> x, 0, len(x))

