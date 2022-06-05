from random import choices
from django.db import models
import re , json
from django.urls import reverse
from datetime import datetime as d
# import pytz

# cairo_time = pytz.timezone('Africa/Cairo')

with open('units.json') as f:
    data = json.load(f)

unit_choice = []
for i in data['units']:
    unit_choice.append((i, i))


def re_pid(i, filename):
    return 'PID/{}/{}'.format(i.unit, filename)

# saved into:  data/PID/<unit>/filename.dwg
class Pid(models.Model):
    name = models.CharField(max_length=10, blank= True)
    unit = models.CharField(max_length=2, choices=unit_choice, default='02')
    upload = models.FileField(blank =True, upload_to=re_pid)
    
    def __str__(self):
        return 'UNIT '+self.unit + '\t' + self.name

#******************************************************************************************************
def re_manual(i, filename):
    return 'Manuals/{}/{}/{}'.format(i.category, i.type ,filename)

manual_category = [
    ('lv' , "Level"),
    ('pr', 'Pressure'),
    ('fl', 'Flow'),
    ('tm', 'Temperature'),
    ('vb', 'Vibration'),
    ('cv', 'Control valves'),
    ('of' , 'On-off valves'),
    ('mv' , 'Motorized valves'),
    ('an', 'Analyzers'),
    ('fg' , 'Fire and Gas'),
    ('na' , 'Other')
]

manual_type = [
    ('tx' , "Transmitter"),
    ('sw', 'Switch'),
    ('ga' , 'Gauge'),
    ('po' , 'Positioner'),
    ('ct' , 'Actuator'),
    ('bd' , 'Body'),
    ('ac' , 'Accessory'),
    ('na' , 'Other'),
]

# data/Manuals/<category>/<type>/filename.pdf
class Manual(models.Model):
    name = models.CharField(max_length=100)
    upload = models.FileField(blank =True, upload_to= re_manual)
    category = models.CharField(max_length= 2, choices= manual_category , default='lv')
    type = models.CharField(max_length= 2, choices= manual_type , default='tx')
    def __str__(self):
        return self.name


#*********************************************************************************************************************
def path_2wire(i, filename):
    return 'TwoWire/{}/{}'.format(i.unit, filename)

class TwoWire(models.Model):
    tag = models.CharField(max_length=30, unique=True)
    unit = models.CharField(max_length=2, choices=unit_choice, default='02')
    upload = models.FileField(blank =True, upload_to= path_2wire)

    def __str__(self):
        return self.tag

#*********************************************************************************************************************
datasheet_types = [
    ('gn' , 'Generic'),
    ('sp' ,'Specific')
]

def datasheet_path(i ,f):
    if i.type == 'sp':
        # path generated is 'Datasheet/02/02-FT-001.jpg'
        return 'Datasheet/{}/{}'.format(i.unit, f)
    else:
        # path generated is 'Datasheet/02/general/filename.jpg'
        return 'Datasheet/{}/general/{}'.format(i.unit, f)


class Datasheet(models.Model):
    name = models.CharField(max_length = 50)
    unit = models.CharField(max_length=2, choices=unit_choice, default='02')
    upload = models.FileField(blank= True, upload_to=datasheet_path)
    type = models.CharField(max_length = 2, choices = datasheet_types , default='sp')
    
    def __str__(self):
        if self.type == 'gn':            
            return 'General ' + self.name
        else:
            return self.name

#*********************************************************************************************************************

class Inst(models.Model):
    tag = models.SlugField(verbose_name="Tag Number" , max_length=30)
    description = models.TextField(max_length=500, blank =True)
    pid = models.ForeignKey( Pid, blank =True,null =True, on_delete=models.CASCADE )              # One To Many
    manual = models.ManyToManyField(Manual,  related_name='manual' ,blank=True  )      # Many To Many
    wire = models.OneToOneField(TwoWire ,null =True, on_delete=models.CASCADE,blank=True )       #One To One
    datasheet = models.ManyToManyField(Datasheet, related_name= 'datasheets' , blank=True) # Many To Many
    scaff = models.BooleanField(default= False)
    # date_added = models.DateTimeField(default=d.now(cairo_time))
    date_added = models.DateTimeField(auto_now= True )

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse( "tag_url", args= [self.tag])

    
