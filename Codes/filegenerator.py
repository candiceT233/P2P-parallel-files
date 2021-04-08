import random
import string
import os

TMB=2097152
EMB=8388608
STMB=16777216
TTMB=33554432

#directories=input("Enter direcotry: ")
#directories = list(directories.split(" "))
directories = ['p1']
#filesize=input("Filesizes in bytes: ")
#filesize=list(filesize.split(" "))
filesize=['33554432']
#filenum=input("Number of files for each size: ")
filenum = 10
#useprefix=input("Use directory prefix for file name? [y/n]").lower()
useprefix='n'

for dir in directories:
    for num in range(0,filenum):
        for size in filesize:
            size_str = str(size)
            if size == '8388608':
                size_str = '8MB'
            elif size == '16777216':
                size_str = '16MB'
            elif size == '2097152':
                size_str='2MB'
            elif size == '33554432':
                size_str='32MB'

            if useprefix == 'y':
                filename= dir+'-'+size_str+'-'+str(num+1)+'.txt'
            else:
                filename= size_str+'-'+str(num+1)+'.txt'

            letters = string.ascii_letters
            content = ''.join(random.choice(letters) for i in range(int(size)))
            if not os.path.exists(dir):
                os.mkdir(dir)

            f=open(f'{dir}/{filename}','w')
            f.write(content)
            f.close()
