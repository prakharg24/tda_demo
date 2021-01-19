from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.template import loader
from django.template import RequestContext
from .models import Question
from django import forms
from .datareader import create_graphs, load_data

cps_choices = [('ppcs', 'Power Plant Control System'), ('agc', 'Automatic Generation Control')]
protection_choices = [(True, 'Enable'), (False, 'Disable')]
mitigation_choices = [(True, 'Enable'), (False, 'Disable')]
curr_system = None

class SystemForm(forms.Form):
    system = forms.ChoiceField(widget=forms.RadioSelect, choices=cps_choices, label="Cyber Physical System")

class PPCSTDAForm(forms.Form):
    # system = forms.ChoiceField(widget=forms.RadioSelect, choices=cps_choices, label="Cyber Physical System", initial='ppcs')
    # protection = forms.ChoiceField(widget=forms.RadioSelect, choices=protection_choices, label="Attack Detection and Classification")
    # mitigation = forms.ChoiceField(widget=forms.RadioSelect, choices=mitigation_choices, label="Attack Mitigation")
    tda_value = forms.IntegerField(label="TDA Value (s)", max_value=50, min_value=0)
    tda_location = forms.IntegerField(label="TDA Launch Time", max_value=1200, min_value=800)

class AGCTDAForm(forms.Form):
    # system = forms.ChoiceField(widget=forms.RadioSelect, choices=cps_choices, label="Cyber Physical System", initial='agc')
    # protection = forms.ChoiceField(widget=forms.RadioSelect, choices=protection_choices, label="Attack Detection and Classification")
    # mitigation = forms.ChoiceField(widget=forms.RadioSelect, choices=mitigation_choices, label="Attack Mitigation")
    tda_value = forms.IntegerField(label="TDA Value (s)", max_value=10, min_value=0)
    tda_location = forms.IntegerField(label="TDA Launch Time", max_value=220, min_value=100)

# def index(request):
#     sum = 1 + 2
#     return_str = "<h1>Hello, world.</h1> You're at the polls index : " + str(sum)
#     return HttpResponse(return_str)
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    output = template.render(context, request)
    return HttpResponse(output)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    template = loader.get_template('polls/detail.html')
    context = {
        'question': question,
    }
    output = template.render(context, request)
    return HttpResponse(output)

def track(request):
    global curr_system

    form = SystemForm(request.POST)
    formppcs = PPCSTDAForm(request.POST)
    formagc = AGCTDAForm(request.POST)
    # print(form)
    load_data()
    if ('goback' not in request.POST) and (form.is_valid() or formppcs.is_valid() or formagc.is_valid()):
        ## Choose the correct system
        if(form.is_valid()):
            curr_system = form.cleaned_data["system"]
        elif(formppcs.is_valid()):
            curr_system = 'ppcs'
        elif(formagc.is_valid()):
            curr_system = 'agc'

        ## Choose proper form
        if(curr_system=="ppcs"):
            form2 = formppcs
        elif(curr_system=="agc"):
            form2 = formagc
        if(form2.is_valid()):
            # form2.cleaned_data["system"] = form.cleaned_data["system"]
            attack_details = create_graphs(form2.cleaned_data, curr_system)
            attack_details['form'] = form2
            attack_details['protection'] = True
            attack_details['ppcs'] = (curr_system=="ppcs")
            # context = {'form' : form2, 'protection':True}
            template = loader.get_template('polls/protection.html')
            output = template.render(attack_details, request)
            return HttpResponse(output)
        else:
            context = {'form': form2, 'protection':False, 'ppcs':(curr_system=="ppcs")}
            template = loader.get_template('polls/protection.html')
            output = template.render(context, request)
            return HttpResponse(output)

    template = loader.get_template('polls/system.html')
    context = {'form': form}
    output = template.render(context, request)
    return HttpResponse(output)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
