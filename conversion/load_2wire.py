# This code takes all files in the folders of 2 wires data path 
# and convert it to a json file in order to "django manage.py loaddata pid.json"
# to create pid.json file in order to prepare the data to be loaded as initial model values.



import json , os
from os.path import isfile, join, basename
mypath = 'C:/Users/moham/instdb/data/TwoWire'

folders =  [folder for folder in os.listdir(mypath) if not isfile(join(mypath, folder))]


#Return array of path for all files by itering through all folders located in the given mypath
# Returned path ex. 'TwoWire\\06\\PT-006.dwg' one item in list.
arr = []
for folder in folders:
    single_folder_path = join(mypath , folder)
    arr.extend([join('TwoWire' , folder , file) for file in os.listdir(single_folder_path) if isfile(join(mypath , folder, file))])


to_json = []
count = 0
for i in arr:
    name = basename(i).split('.')[0]
    unit = i.split('\\')[1]

    item = [{"model": "instapp.TwoWire", 
    "fields": {"tag": unit + '-' + name  , 
                "unit": unit,
                "upload": i }}]
    to_json.extend(item)
    count +=1

# print(to_json)
with open('conversion/wires.json', 'w') as f:
    json.dump(to_json, f, indent=5)


print('{} files added to the json'.format(count))