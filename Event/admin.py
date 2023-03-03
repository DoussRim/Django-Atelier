from django.contrib import admin,messages
# from Event.models
from.models import *
from Person.models import Person
from datetime import datetime
# Register your models here.
class ParticipationsAdmin(admin.StackedInline):
    model = Event_Participation
    extra=0
@admin.register(Person)
class SearchPerson(admin.ModelAdmin):
    search_fields=['username']
class DateListFilter(admin.SimpleListFilter):
    title= 'Event Date'
    parameter_name='event_date'
    def lookups(self, request, model_admin):
        return (
            ('Past Events',('Past Events')),
            ('Upocoming Events',('Upocoming Events')),
            ('Today Events', ('Today Events'))
        )
    def queryset(self, request, queryset):
        if self.value()=='Past Events':
            return queryset.filter(event_date__lt=datetime.now())
        if self.value()=='Upocoming Events':
            return queryset.filter(event_date__gt=datetime.now())
        if self.value()=='Today Events':
            return queryset.filter(event_date__exact=datetime.now())
def set_True(ModelAdmin,request,queryset):
    req=queryset.update(state=True)
    if req==1:
        message ="1 event was "
    else:
        message=f"{req} events were"
    messages.success(request,
                    message="%s successfully acceptes" %message)
set_True.short_description="Accept"
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    def set_false(self,request,queryset):
        req=queryset.filter(state=False)
        if(req.count()>0):
            messages.error(request, f"{req.count()} events are already marked Refused")
        else:
            req_update=queryset.update(state=False)
            if req_update==1:
                message ="1 event was "
            else:
                message=f"{req_update} events were"
            messages.success(request,
                    message="%s successfully marked refused" %message)
    set_false.short_description="Refused"
    list_display=('title','description',
                  'nbe_participant',
                  'state',
                  'image',
                  'event_date',
                  'creation_date',
                  'update_date',
                  'organizer','evt_participation')
    def evt_participation(self,obj):
        return obj.participation.count()
    actions=[set_True,set_false]
    list_per_page=2
    list_filter=('title',DateListFilter)
    fieldsets = (
        ('A propos', {
            "fields": ('title','description','image'),
        }),
        ('Date',{"fields":('event_date','creation_date','update_date')
        }),
        ('Others',{
            "fields":('category','state','nbe_participant')
        }),
        ('Personal',{
            "fields":('organizer',)
        })
    )
    
    readonly_fields=['creation_date','update_date']
    inlines=(ParticipationsAdmin,)
    autocomplete_fields=['organizer']
    ordering=['event_date']
    
# admin.site.register(Event,EventAdmin)