import h5py

class get_data_from_hdf5(object):
	def __init__(self, filename):
		self.filename = filename

	def get_data(self):
		self.read_file = h5py.File(self.filename,'r+')
		for key_ in list(self.read_file.keys()):
			keyval = self.read_file[key_][()]
			nkeyval = len(keyval)
			exec('self.'+key_+'=keyval')
			exec('self.n'+key_+'=nkeyval')

	def printit(self):
		for key_ in list(read_file.keys()):
			print('number of labels for ..' , key_ , exec('self.n'+key_))
		

