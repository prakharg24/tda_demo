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

cps_choices = [('ppcs', 'PPCS'), ('agc', 'AGC')]
protection_choices = [(True, 'Enable'), (False, 'Disable')]
mitigation_choices = [(True, 'Enable'), (False, 'Disable')]
class TDAForm(forms.Form):
    system = forms.ChoiceField(widget=forms.RadioSelect, choices=cps_choices, label="Cyber Physical System")
    protection = forms.ChoiceField(widget=forms.RadioSelect, choices=protection_choices, label="Attack Detection and Classification")
    mitigation = forms.ChoiceField(widget=forms.RadioSelect, choices=mitigation_choices, label="Attack Mitigation")
    tda_value = forms.IntegerField(label="TDA Value")
    tda_location = forms.IntegerField(label="TDA Location")

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
    form = TDAForm(request.POST)
    # print(form)
    load_data()
    if form.is_valid():
        print(form.cleaned_data)
        create_graphs(form.cleaned_data)
        if(form.cleaned_data["protection"]=="True"):
            context = {'form' : form, 'protection':True}
        else:
            context = {'form' : form, 'protection':False}
        template = loader.get_template('polls/index.html')
        output = template.render(context, request)
        return HttpResponse(output)

    template = loader.get_template('polls/index.html')
    context = {'form': form, 'protection':False}
    output = template.render(context, request)
    return HttpResponse(output)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
