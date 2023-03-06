from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.views.generic import *
from .forms import AddForm
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
# Create your views here.
def index(request):
    return HttpResponse("Bonjour")
def affiche(request,classe):
    # contexte={"c":classe}
    return render(request,"Eventx/affiche.html",
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
    # queryset=Event.objects.filter(state=True)
    # def get_query(self):
    #     return Event.objects.filter(state=True)
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
def Participate(request,evt_id):
    object=Event_Participation()
    object.person=Person.objects.get(cin=request.user.cin)
    object.event=Event.objects.get(pk=evt_id)
    if Event_Participation.objects.filter(
        person=object.person,event=object.event).count()==0:
        object.save()
        # total=nbe_participant+1
        Event.objects.filter(pk=evt_id).update(
            nbe_participant=F('nbe_participant')+1
        )
    else:
        return HttpResponse(
            f"You're already participating in the event {object.event.title}")
    return redirect('Aff')
def cancel(request, id):
    evt=Event.objects.get(id=id)
    person=Person.objects.get(cin=request.user.cin)
    if Event_Participation.objects.filter(person=person,event=evt).count()!=0:
        Event_Participation.objects.get(person=person,event=evt).delete()
        evt.nbe_participant-=1
        evt.save()
    return redirect('Aff')
class Delete(DeleteView):
    model=Event
    success_url=reverse_lazy('Aff')
class Update(UpdateView):
    model=Event
    form_class=AddForm
    template_name='Event/Ajout.html'
    
        
    