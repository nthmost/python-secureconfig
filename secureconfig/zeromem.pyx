from libc.string cimport memset

def zero(x):
	memset(<char*> x, 0, len(x))

