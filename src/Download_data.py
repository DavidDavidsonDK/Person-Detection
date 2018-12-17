import os
import zipfile
try:
    from urllib.request  import urlopen
except ImportError:
    from urllib2 import urlopen


def download_data(url):

	u = urlopen(url)
	data = u.read()
	u.close()
	os.chdir('..')
	path = 'data/raw/'

	with open(path + 'citycams_1.zip', "wb") as f :
		f.write(data)
	zip_ref = zipfile.ZipFile(path+'citycams_1.zip', 'r')
	zip_ref.extractall(path)
	zip_ref.close()
	os.remove(path+'citycams_1.zip')

if __name__ == '__main__':
	url = "https://www.dropbox.com/s/qnod3rlulabdjv8/citycams_1.zip?dl=1" 
	print('Downloading ...')
	download_data(url)
	print('Done.')