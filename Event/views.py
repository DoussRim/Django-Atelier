from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.views.generic import *
from .forms import AddForm
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def index(request):
    return HttpResponse("Bonjour")
def affiche(request,classe):
    # contexte={"c":classe}
    return render(request,"Event/affiche.html",
                  {"c":classe})
# Méthode avec QuerySets
@login_required(login_url="login")
def ListEvt(request):
    evt=Event.objects.all()
    # Affichage via HttpResponse
    # resultat="----".join(e.title for e in evt)
    # return HttpResponse(resultat)
    # Affichage via render() templates
    return render(request,'Event/AfficheEvt.html',{'e':evt})
# Méthode via generic class
class ListEvtGeneric(LoginRequiredMixin,ListView):
    model = Event
    context_object_name='e'
    #On garde le temlate par défaut event_list.html
    # fields="__all__"
    template_name = "Event/AfficheEvt.html"#un nouveau Template
    ordering=['-event_date']
def Detail(request,title):
    event=Event.objects.get(title=title)#QuerySet
    return render(request,"Event/Detail.html",{'t':event})

def AjoutEvt(request):
    if request.method== "GET":
        form = AddForm()
        return render(request,'Event/Ajout.html',
                      {'form':form})
    if request.method=="POST":
        form = AddForm(request.POST,request.FILES)
        if form.is_valid():
            new_evt=form.save(commit=False)
            new_evt.save()
            return HttpResponseRedirect(reverse('Aff'))
        else:
            return render(request,'Event/Ajout.html',
                          {'form':form, "msg_erreur":"Erreur lors de l'ajout d'un evt"})
class Ajout(CreateView):
    model=Event
    form_class=AddForm
    # fields='__all__'
    template_name='Event/Ajout.html'
    # template_name='Event/event_form.html'
    #contexte
    success_url=reverse_lazy("Aff")
class DetailGeneric(DetailView):
    model=Event
    # context_object_name='t'
    template_name='Event/Detail.html'
    