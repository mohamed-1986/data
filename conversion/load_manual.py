# This code takes all files in the folders of manuals data path 
# and convert it to a json file in order to "django manage.py loaddata manuals.json"
# to create manuals.json file in order to prepare the data to be loaded as initial model values.

import json , os
from os.path import isfile, join, basename
mypath = 'C:/Users/moham/instdb/data/Manuals'

# Target path "Manuals\\<category>\\<type>\\name.pdf" 
# ex:   "Manuals\\pr\\tx\\forxboro.pdf"
to_json = []
counter = 0
# Select only folders from the given path return all category folder names
cat_folders =  [folder for folder in os.listdir(mypath) if not isfile(join(mypath, folder))]

for cat_folder in cat_folders:
    type_folders =  [folder for folder in os.listdir(join(mypath, cat_folder)) if not isfile(join(mypath, cat_folder, folder))]
    
    for typ_folder in type_folders:
        all_manual_files = [fn for fn in os.listdir(join(mypath, cat_folder, typ_folder)) if isfile(join(mypath, cat_folder, typ_folder, fn))]
        
        for man in all_manual_files:
            # print('the path is Manuals\\{}\\{}\\{}'.format(cat_folder, typ_folder, man))
            # the path is Manuals\fl\tx\Foxboro_dp.pdf
            item = [{"model": "instapp.Manual",
                    "fields": {
                    "name" : man,
                    "upload" : join('Manuals', cat_folder, typ_folder, man),
                    "category" : cat_folder,
                    "type" : typ_folder
                }
            }]
            to_json.extend(item)
            counter += 1


with open('manuals.json', 'w') as f:
    json.dump(to_json, f, indent=5)
