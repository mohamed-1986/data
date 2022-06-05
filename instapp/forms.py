from unicodedata import category
from django.forms import ModelForm, Form
from .models import *
from django import forms

class data_entry(ModelForm):
    class Meta:
        model = Inst
        fields = ['tag' , 'description', 'pid' , 'manual', 'wire', 'datasheet', 'scaff']
    def __init__(self, *args, **kwargs):
        get_unit = kwargs.pop('unit', None)
        get_typ = kwargs.pop('type', None)
        get_cat = kwargs.pop('cat', None)
        if get_unit != ('na' or None):
            Q_PID = Pid.objects.filter(unit= get_unit)
            Q_wire = TwoWire.objects.filter(unit= get_unit)
            Q_ds = Datasheet.objects.filter(unit= get_unit)
        else:
            Q_PID = Pid.objects.all()
            Q_wire = TwoWire.objects.all()
            Q_ds = Datasheet.objects.all()

        if get_typ != ('na' or None) and get_cat != ('na' or None):
            Q_man = Manual.objects.filter(type = get_typ, category = get_cat)
        elif get_typ != ('na' or None) and get_cat == ('na' or None):
            Q_man = Manual.objects.filter(type = get_typ)
        elif get_typ == ('na' or None) and get_cat != ('na' or None):
            Q_man = Manual.objects.filter(category = get_cat)
        else:
            Q_man = Manual.objects.all()

        super(data_entry, self).__init__(*args, **kwargs)
        self.fields['pid'] =forms.ModelChoiceField(queryset= Q_PID, required=False)
        self.fields['wire']=forms.ModelChoiceField(queryset= Q_wire, required=False)
        self.fields['datasheet']=forms.ModelMultipleChoiceField(queryset= Q_ds, required=False)
        self.fields['manual'] = forms.ModelMultipleChoiceField(queryset= Q_man ,required = False)
        # self.fields['wire'].required = False

    def save(self):
        instance = forms.ModelForm.save(self)
        # instance.manual.clear()
        instance.manual.add(*self.cleaned_data['manual'])
        return instance



class manual_add_form(ModelForm):
    class Meta:
        model = Inst
        fields = ['manual']
    def __init__(self, *args, **kwargs):
        get_typ = kwargs.pop('type', None)
        get_cat = kwargs.pop('cat', None)
       
        if get_typ != ('na' or None) and get_cat != ('na' or None):
            Q_man = Manual.objects.filter(type = get_typ, category = get_cat)
        elif get_typ != ('na' or None) and get_cat == ('na' or None):
            Q_man = Manual.objects.filter(type = get_typ)
        elif get_typ == ('na' or None) and get_cat != ('na' or None):
            Q_man = Manual.objects.filter(category = get_cat)
        else:
            Q_man = Manual.objects.all()

        super(manual_add_form, self).__init__(*args, **kwargs)
        self.fields['manual'] = forms.ModelMultipleChoiceField(queryset= Q_man ,required = False)
        # self.fields['wire'].required = False

    # def save(self):
    #     instance = forms.ModelForm.save(self)
    #     instance.manual.add(*self.cleaned_data['manual'])
    #     return instance

'''
    def save(self, commit=True):
        # Get the unsave Pizza instance
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           # This is where we actually link the pizza with toppings
           instance.manual.clear()
           instance.manual.add(*self.cleaned_data['manual'])
        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance

'''
# class Inst(models.Model):
#     tag = models.SlugField(verbose_name="Tag Number" , max_length=30)
#     description = models.TextField(max_length=500, blank =True)
#     pid = models.ForeignKey( Pid, blank =True, on_delete=models.CASCADE )              # One To Many
#     manual = models.ManyToManyField(Manual,  related_name='manual' ,blank=True  )      # Many To Many
#     wire = models.OneToOneField(TwoWire ,null =True, on_delete=models.CASCADE,blank=True )       #One To One
#     datasheet = models.ManyToManyField(Datasheet, related_name= 'datasheets' , blank=True) # Many To Many
#     scaff = models.BooleanField(default= False)

# class data_entry_form(Form):
#     tag = forms.SlugField(max_length=30)
#     description = forms.CharField(widget=forms.Textarea)
#     pid = forms.ModelChoiceField( queryset=Pid.objects.filter(unit='06') )              # One To Many
    # manual = forms.ModelMultipleChoiceField(Manual,  related_name='manual' ,blank=True  )      # Many To Many
    # wire = forms.ModelChoiceField(TwoWire ,null =True, on_delete=models.CASCADE,blank=True )       #One To One
    # datasheet = forms.ModelMultipleChoiceField(Datasheet, related_name= 'datasheets' , blank=True) # Many To Many
    # scaff = forms.BooleanField(default= False)




class unit_selection(Form):
    unit_choice.insert(0,('na' , 'No filter'))
    unit = forms.CharField(label='Select unit', widget=forms.Select(choices=unit_choice)) #Pid.objects.all())) #



class type_selection(Form):
    manual_type.insert(0 , ('na' , 'No filter'))
    type = forms.CharField(label='Select type', widget=forms.Select(choices=manual_type))


class cat_selection(Form):
    manual_category.insert(0 , ('na' , 'No filter'))
    cat = forms.CharField(label='Select cat', widget=forms.Select(choices=manual_category))

class manual_filter(Form):
    def __init__(self, *args, **kwargs):
        get_typ = kwargs.pop('type', None)
        get_cat = kwargs.pop('cat', None)
    
        m_list = Manual.objects.all()
        w_list = forms.CharField(label = 'filter_of_manual', widget=forms.Select(choices=m_list))



