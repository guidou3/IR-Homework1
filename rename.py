import os
import subprocess

def rename_file(path):
    ext = path[-3:]
    if ext == ".0Z":
        os.rename(path, path[:-3] + '_0.Z')
    elif ext == ".1Z":
        os.rename(path, path[:-3] + '_1.Z')
    elif ext == ".2Z":
        os.rename(path, path[:-3] + '_2.Z')
    else:
        pass
			
for root, dirs, files in os.walk("data/TIPSTER/TREC_VOL4/FR94"):
	print(root)
	# print(dirs)
	print(files)
	for name in files:
		ext = name[-3:]
		path = root + '/' + name
		if ext == ".0Z":
			os.rename(path, path[:-3] + '_0.Z')
		elif ext == ".1Z":
			os.rename(path, path[:-3] + '_1.Z')
		elif ext == ".2Z":
			os.rename(path, path[:-3] + '_2.Z')
		else:
			continue
	