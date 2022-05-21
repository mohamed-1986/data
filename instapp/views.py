from django.shortcuts import render, redirect
from instapp.forms import *
from .models import Inst
from django.views.generic import TemplateView, ListView, DetailView
from django.http import HttpResponse, Http404
from django.forms import modelformset_factory
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

from django.contrib import messages

def HomeView(request):
    u = unit_selection()
    query = Inst.objects.all().order_by('date_added')
    t = type_selection()
    c = cat_selection()
    return render(request, 'index.html', {'units':u, 'added_items': query, 't':t, 'c': c})


class Search(ListView):
    model= Inst
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Inst.objects.filter(tag__exact = query.upper())
        return object_list


class Tag(DetailView):
    model = Inst
    template_name = 'tag.html'
    slug_field = 'tag'     

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the many to many relations
        context['manuals_list'] = self.get_manuals()
        context['datasheets_list'] = self.get_datasheets()
        context['manual_add_form'] = manual_add_form()
        context['c'] = cat_selection()
        context['t'] = type_selection()
        return context

    def get_manuals(self):
        obj = super().get_object()
        return obj.manual.all()

    def get_datasheets(self):
        obj = super().get_object()
        return obj.datasheet.all()

def add_ins(request):
    
    try:
        qs= request.GET['unit']
        type = request.GET['type']
        cat = request.GET['cat']
    except:
        qs = None
        type = None
        cat = None
    if request.method == 'POST':
        f = data_entry(request.POST, unit = qs, type= type, cat = cat)
        if f.is_valid():
            # Inspect the tag in order not to save it again:
            t = f.cleaned_data['tag']
            # inst , created = Inst.objects.get_or_create(tag = t)
            try:
                t = Inst.objects.get(tag = t)
            except:
                t= None
            if t == None:
                messages.add_message(request, messages.INFO, 'New item is added')
                f.save()
            else:
                messages.add_message(request, messages.INFO, 'Already existing!')
                print('already exist!')
                '''
            inst , created = Inst.objects.get_or_create(tag = t)
            f = data_entry(unitunit = qs, instance= inst)
            new = f.save(commit= False)
            
            if f.cleaned_data['pid']:
                new.pid = f.cleaned_data['pid']
            if f.cleaned_data['wire']:
                new.wire = f.cleaned_data['wire']
            if f.cleaned_data['manual']:
                new.manual.add(f.cleaned_data['manual'][0].id)
            # f = data_entry( request.POST, unitunit = qs, instance = inst)
            new.save()
            f.save_m2m()'''
            # if f.cleaned_data['manual']:
                # print()
                # new_inst = my_form.save(commit=False)
                # m = my_form.cleaned_data['manual']
                # m_id =m.values_list('id')[0]
                # new_inst.manual.add(m_id)
                # my_form.save_m2m()
            # else:
            #     my_form.save()
            return redirect('/')
        else:
            return HttpResponse('invalid ')

    if request.method == 'GET':
        my_form = data_entry(unit = qs, type= type, cat = cat)
        return render(request, 'add_instr.html', {'qs': qs, 'my_form': my_form})

    

def add_manual_to_inst(request, slug):
    try:
        type = request.GET['type']
        cat = request.GET['cat']
    except:
        type = None
        cat = None

    if request.method == 'POST':
        try:
            t = Inst.objects.get(tag = slug)
        except:
            return HttpResponse('Not found tag')
        f = manual_add_form(request.POST, type= type, cat = cat, instance = t)
        old_m = t.manual.all().values_list('id')
        print(old_m)
        if f.is_valid():
            t.manual.add(*f.cleaned_data['manual'])
            t.save()
            return redirect('/')
        else:
            return HttpResponse('invalid ')

    if request.method == 'GET':
        form = manual_add_form(type= type, cat = cat)
        return render(request, 'add_manual_to_tag.html', {'form': form})


# def add_ins(request):
#     if request.method == 'POST':
#         form = data_entry_form(request.POST)  if f.cleaned_data['manual']:
#         if form.is_valid():
#             form.save()
#     else:
#         form = data_entry_form()
#         unit_form = unit_selection()
    
#     return render(request, 'add_instr.html', {"form": form, "units": unit_form})

# def tag_details(request , str):
#     context={}
#     context['tag'] = str
#     # q = Inst.objects.filter(tag = str).count()
#     q = Inst.objects.filter(tag = str).first()
#     context['item'] = q
#     mans = q.manual.all()
#     context['mans'] = mans
#     return render(request , 'tag1.html' , context)
#     return HttpResponse("the tag number is " + str)

# def pid(request, unit, tag):
#     print('unit is {} and the tag is{}'.format(unit ,tag))
#     return HttpResponse("Hello, world. You're at the Inst index page.")

