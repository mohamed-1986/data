
# This code takes all files in the folders of Pid data path 
# and convert it to a json file in order to "django manage.py loaddata pid.json"
# in another code.


import json , os
from os.path import isfile, join, basename
mypath = 'C:/Users/moham/instdb/data/pid'

pid_folders =  [folder for folder in os.listdir(mypath) if not isfile(join(mypath, folder))]

arr = []
for folder in pid_folders:
    single_folder_path = join(mypath , folder)
    arr.extend([join('pid' , folder , file) for file in os.listdir(single_folder_path) if isfile(join(mypath , folder, file))])
    # print(file)

to_json = []
count = 0
for i in arr:
    # print(basename(i).split('.')[0]  , i.split('\\')[1])
    name = basename(i).split('.')[0]
    unit = i.split('\\')[1]

    item = [{"model": "instapp.Pid", 
    "fields": {"name": name , 
                    "unit": unit,
                    "upload": join('pid' ,unit , basename(i)) }}]
    to_json.extend(item)
    count +=1

# print(to_json)
with open('conversion/pid.json', 'w') as f:
    json.dump(to_json, f, indent=5)


print('{} files added to the json'.format(count))