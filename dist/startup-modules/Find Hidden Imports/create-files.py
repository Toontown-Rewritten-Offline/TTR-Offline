import os
from fnmatch import fnmatch

file = open("files.py", 'a')

toontown = '../../../'
direct = '../../../../Nuitka-Python/output/Lib/site-packages/direct'
pattern = "*.py"
no_include = ['__init__', 'import dist.']

for path, subdirs, files in os.walk(toontown):
    for name in files:
        if fnmatch(name, pattern):
            filelist = os.path.join(path, name)
            filelist = filelist.replace(toontown, 'import ')
            filelist = filelist.replace('.py', '')
            filelist = filelist.replace("\\", ".")
            if filelist.find(no_include[0]) == -1:
                if filelist.find(no_include[1]) == -1:
                    print(filelist)
                    file.writelines(filelist + '\n')
            else:
                print(filelist[:-9])
                file.writelines(filelist[:-9] + '\n')

for path, subdirs, files in os.walk(direct):
    for name in files:
        if fnmatch(name, pattern):
            filelist = os.path.join(path, name)
            filelist = filelist.replace(os.path.dirname(direct) + '/', 'import ')
            filelist = filelist.replace('.py', '')
            filelist = filelist.replace("\\", ".")
            if filelist.find(no_include[0]) == -1:
                if filelist.find(no_include[1]) == -1:
                    print(filelist)
                    file.writelines(filelist + '\n')
            else:
                print(filelist[:-9])
                file.writelines(filelist[:-9] + '\n')