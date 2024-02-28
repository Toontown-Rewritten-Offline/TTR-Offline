import os
from fnmatch import fnmatch

file = open("files.py", 'a')

root = '../../../'
pattern = "*.py"
no_include = ['__init__', 'import dist.']

for path, subdirs, files in os.walk(root):
    for name in files:
        if fnmatch(name, pattern):
            filelist = os.path.join(path, name)
            filelist = filelist.replace('../../../', 'import ')
            filelist = filelist.replace('.py', '')
            filelist = filelist.replace("\\", ".")
            if filelist.find(no_include[0]) == -1:
                if filelist.find(no_include[1]) == -1:
                    print(filelist)
                    file.writelines(filelist + '\n')